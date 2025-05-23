"""
sbfreader.py

SBFReader class.

Reads and parses individual NMEA, SBF and RTCM messages from any viable
data stream which supports a read(n) -> bytes method.

SBF transport layer bit format:

+--------------+---------+---------+---------+---------+-----------------+
| hdr (0x2440) |   crc   |  msgid  |  revid  | length  |     payload     |
+==============+=========+=========+=========+=========+=================+
| 16 bits      | 16 bits | 12 bits |  4 bits | 16 bits |     variable    |
+--------------+---------+---------+---------+---------+-----------------+
|                        8 bytes                       |                 |
+--------------+---------+---------+---------+---------+-----------------+


Returns both the raw binary data (as bytes) and the parsed data
(as an SBFMessage or NMEAMessage object).

- 'protfilter' governs which protocols (NMEA, SBF, RTCM) are processed
- 'quitonerror' governs how errors are handled

Created on 19 May 2025

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from logging import getLogger
from socket import socket

from pynmeagps import (
    NMEA_HDR,
    NMEAMessageError,
    NMEAParseError,
    NMEAReader,
    NMEAStreamError,
    NMEATypeError,
    SocketWrapper,
)
from pyrtcm import (
    RTCMMessageError,
    RTCMParseError,
    RTCMReader,
    RTCMStreamError,
    RTCMTypeError,
)

from pysbf2.exceptions import (
    SBFMessageError,
    SBFParseError,
    SBFStreamError,
    SBFTypeError,
)
from pysbf2.sbfhelpers import bytes2id, crc2bytes, escapeall
from pysbf2.sbfmessage import SBFMessage
from pysbf2.sbftypes_core import (
    ERR_LOG,
    ERR_RAISE,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
    SBF_HDR,
    SBF_PROTOCOL,
    VALCKSUM,
)


class SBFReader:
    """
    SBFReader class.
    """

    def __init__(
        self,
        datastream,
        validate: int = VALCKSUM,
        protfilter: int = NMEA_PROTOCOL | SBF_PROTOCOL | RTCM3_PROTOCOL,
        quitonerror: int = ERR_LOG,
        bufsize: int = 4096,
        parsing: bool = True,
        errorhandler: object = None,
    ):
        """Constructor.

        :param datastream stream: input data stream
        :param int validate: VALCKSUM (1) = Validate checksum,
            VALNONE (0) = ignore invalid checksum (1)
        :param int protfilter: NMEA_PROTOCOL (1), SBF_PROTOCOL (2),
            RTCM3_PROTOCOL (4), Can be OR'd (7)
        :param int quitonerror: ERR_IGNORE (0) = ignore errors,  ERR_LOG (1) = log continue,
            ERR_RAISE (2) = (re)raise (1)
        :param int bufsize: socket recv buffer size (4096)
        :param bool parsing: True = parse data, False = don't parse data (output raw only) (True)
        :param object errorhandler: error handling object or function (None)
        :raises: SBFStreamError (if mode is invalid)
        """
        # pylint: disable=too-many-arguments

        if isinstance(datastream, socket):
            self._stream = SocketWrapper(datastream, bufsize=bufsize)
        else:
            self._stream = datastream
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._protfilter = protfilter
        self._validate = validate
        self._parsing = parsing
        self._logger = getLogger(__name__)

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> tuple:
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as SBFMessage)
        :rtype: tuple
        :raises: StopIteration

        """

        (raw_data, parsed_data) = self.read()
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return (raw_data, parsed_data)

    def read(self) -> tuple:
        """
        Read a single NMEA, SBF or RTCM3 message from the stream buffer
        and return both raw and parsed data.

        'protfilter' determines which protocols are parsed.
        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as SBFMessage, NMEAMessage or RTCMMessage)
        :rtype: tuple
        :raises: Exception (if invalid or unrecognised protocol in data stream)
        """

        parsing = True
        while parsing:  # loop until end of valid message or EOF
            try:

                raw_data = None
                parsed_data = None
                byte1 = self._read_bytes(1)  # read the first byte
                # if not SBF, NMEA or RTCM3, discard and continue
                if byte1 not in (b"\x24", b"\xd3"):
                    continue
                byte2 = self._read_bytes(1)
                bytehdr = byte1 + byte2

                # if it's a SBF message (b'\x24\x40')
                if bytehdr == SBF_HDR:
                    (raw_data, parsed_data) = self._parse_sbf(bytehdr)
                    # if protocol filter passes SBF, return message,
                    # otherwise discard and continue
                    if self._protfilter & SBF_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's an NMEA message (b'\x24\x..)
                elif bytehdr in NMEA_HDR:
                    (raw_data, parsed_data) = self._parse_nmea(bytehdr)
                    # if protocol filter passes NMEA, return message,
                    # otherwise discard and continue
                    if self._protfilter & NMEA_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's a RTCM3 message
                # (byte1 = 0xd3; byte2 = 0b000000**)
                elif byte1 == b"\xd3" and (byte2[0] & ~0x03) == 0:
                    (raw_data, parsed_data) = self._parse_rtcm3(bytehdr)
                    # if protocol filter passes RTCM, return message,
                    # otherwise discard and continue
                    if self._protfilter & RTCM3_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # unrecognised protocol header
                else:
                    raise SBFParseError(f"Unknown protocol header {bytehdr}.")

            except EOFError:
                return (None, None)
            except (
                SBFMessageError,
                SBFTypeError,
                SBFParseError,
                SBFStreamError,
                NMEAMessageError,
                NMEATypeError,
                NMEAParseError,
                NMEAStreamError,
                RTCMMessageError,
                RTCMTypeError,
                RTCMParseError,
                RTCMStreamError,
            ) as err:
                if self._quitonerror:
                    self._do_error(err)
                continue

        return (raw_data, parsed_data)

    def _parse_sbf(self, hdr: bytes) -> tuple:
        """
        Parse remainder of SBF message.

        :param bytes hdr: SBF header (b'\\x24\\x40')
        :return: tuple of (raw_data as bytes, parsed_data as SBFMessage or None)
        :rtype: tuple
        """

        # read the rest of the SBF message from the buffer
        byten = self._read_bytes(6)
        crc = byten[0:2]
        msgid = byten[2:4]
        lenb = byten[4:6]
        # lenb includes 8 byte header
        leni = int.from_bytes(lenb, "little", signed=False) - 8
        plb = self._read_bytes(leni)
        raw_data = hdr + crc + msgid + lenb + plb
        # only parse if we need to (filter passes SBF)
        if (self._protfilter & SBF_PROTOCOL) and self._parsing:
            parsed_data = self.parse(
                raw_data,
                validate=self._validate,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_nmea(self, hdr: bytes) -> tuple:
        """
        Parse remainder of NMEA message (using pynmeagps library).

        :param bytes hdr: NMEA header (b'\\x24\\x..')
        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage or None)
        :rtype: tuple
        """

        # read the rest of the NMEA message from the buffer
        byten = self._read_line()  # NMEA protocol is CRLF-terminated
        raw_data = hdr + byten
        # only parse if we need to (filter passes NMEA)
        if (self._protfilter & NMEA_PROTOCOL) and self._parsing:
            # invoke pynmeagps parser
            parsed_data = NMEAReader.parse(
                raw_data,
                validate=self._validate,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_rtcm3(self, hdr: bytes) -> tuple:
        """
        Parse any RTCM3 data in the stream (using pyrtcm library).

        :param bytes hdr: first 2 bytes of RTCM3 header
        :return: tuple of (raw_data as bytes, parsed_stub as RTCMMessage)
        :rtype: tuple
        """

        hdr3 = self._read_bytes(1)
        size = hdr3[0] | (hdr[1] << 8)
        payload = self._read_bytes(size)
        crc = self._read_bytes(3)
        raw_data = hdr + hdr3 + payload + crc
        # only parse if we need to (filter passes RTCM)
        if (self._protfilter & RTCM3_PROTOCOL) and self._parsing:
            # invoke pyrtcm parser
            parsed_data = RTCMReader.parse(
                raw_data,
                validate=self._validate,
                labelmsm=1,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: SBFStreamError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) == 0:  # EOF
            raise EOFError()
        if 0 < len(data) < size:  # truncated stream
            raise SBFStreamError(
                "Serial stream terminated unexpectedly. "
                f"{size} bytes requested, {len(data)} bytes returned."
            )
        return data

    def _read_line(self) -> bytes:
        """
        Read bytes until LF (0x0a) terminator.

        :return: bytes
        :rtype: bytes
        :raises: SBFStreamError if stream ends prematurely
        """

        data = self._stream.readline()  # NMEA protocol is CRLF-terminated
        if len(data) == 0:
            raise EOFError()  # pragma: no cover
        if data[-1:] != b"\x0a":  # truncated stream
            raise SBFStreamError(
                "Serial stream terminated unexpectedly. "
                f"Line requested, {len(data)} bytes returned."
            )
        return data

    def _do_error(self, err: Exception):
        """
        Handle error.

        :param Exception err: error
        :raises: Exception if quitonerror = ERR_RAISE (2)
        """

        if self._quitonerror == ERR_RAISE:
            raise err from err
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            # else just log
            if self._errorhandler is None:
                self._logger.error(err)
            else:
                self._errorhandler(err)

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(
        message: bytes,
        validate: int = VALCKSUM,
    ) -> object:
        """
        Parse SBF byte stream to SBFMessage object.

        :param bytes message: binary message to parse
        :param int validate: VALCKSUM (1) = Validate checksum,
            VALNONE (0) = ignore invalid checksum (1)
        :return: SBFMessage object
        :rtype: SBFMessage
        :raises: SBFMessageError (if data stream contains invalid CRC)
        """

        crc = message[2:4]
        msg = message[4:]
        crccheck = crc2bytes(msg)
        if crccheck != crc and validate & VALCKSUM:
            raise SBFMessageError(
                f"Invalid CRC {escapeall(crc)} - should be {escapeall(crccheck)}"
            )
        msgid, revno = bytes2id(message[4:6])
        length = int.from_bytes(message[6:8], "little")
        plb = message[8:]

        return SBFMessage(msgid, revno, crc, length, payload=plb)
