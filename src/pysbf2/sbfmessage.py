"""
SBFmessage.py

Main SBF Message Protocol Class.

Created on 19 May 2025

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

# pylint: disable=invalid-name

import struct
from math import ceil

from pysbf2.exceptions import SBFMessageError, SBFTypeError
from pysbf2.sbfhelpers import (
    attsiz,
    atttyp,
    bytes2val,
    crc2bytes,
    escapeall,
    getpadding,
    itow2utc,
    msgid2bytes,
    nomval,
    val2bytes,
)
from pysbf2.sbftypes_blocks import SBF_BLOCKS
from pysbf2.sbftypes_core import (
    PAD,
    PD,
    PD1,
    PD2,
    SBF_HDR,
    SBF_MSGIDS,
    SCALROUND,
    U2,
    VAR,
    X1,
    X2,
    X4,
    X6,
    X8,
    X24,
)


class SBFMessage:
    """SBF Message Class."""

    def __init__(
        self,
        msgid: object,
        revno: int = 0,
        crc: bytes = b"\x00\x00",
        length: int = 0,
        parsebitfield: bool = True,
        **kwargs,
    ):
        """Constructor.

        If no keyword parms are passed, the payload is taken to be empty.

        If 'payload' is passed as a keyword parm, this is taken to contain the complete
        payload as a sequence of bytes; any other keyword parms are ignored.

        Otherwise, any named attributes will be assigned the value given, all others will
        be assigned a nominal value according to type.

        :param object msgid: message ID as str, int or bytes
        :param int revid: revision number (0)
        :param bytes crc: CRC16-CCIT as 2 bytes (if b"\\\\x00\\\\x00", will be derived)
        :param int length: length (if 0, will be derived)
        :param bool parsebitfield: parse bitfields ('X' type attributes) Y/N
        :param kwargs: optional payload keyword arguments
        :raises: SBFMessageError
        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self._crc = crc
        self._length = length
        self._parsebf = parsebitfield  # parsing bitfields Y/N?
        self._payload = None
        self._nyi = False  # not yet implemented flag

        # convert msgid to string
        if isinstance(msgid, bytes):
            msgid = bytes2val(msgid, U2)
        if isinstance(msgid, int):
            try:
                msgid = msgid & 0b0001111111111111
                revno = (msgid & 0b1110000000000000) >> 13
                msgid = SBF_MSGIDS[msgid][0]
            except KeyError as err:
                raise SBFMessageError(f"Unknown SBF Message ID {msgid}") from err
        self._msgid = msgid
        self._revno = revno

        self._do_attributes(**kwargs)

        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self, **kwargs):
        """
        Populate SBFMessage from named attribute keywords.
        Where a named attribute is absent, set to a nominal value (zeros or blanks).

        :param kwargs: optional payload key/value pairs
        :raises: SBFTypeError

        """

        offset = 0  # payload offset in bytes
        index = []  # array of (nested) group indices

        try:
            if len(kwargs) == 0:  # if no kwargs, assume null payload
                self._payload = None
                self._nyi = True
            else:
                self._payload = kwargs.get("payload", b"")
                pdict = self._get_dict(**kwargs)  # get appropriate payload dict
                if pdict == {}:
                    self._nyi = True
                for anam in pdict:  # process each attribute in dict
                    (offset, index) = self._set_attribute(
                        anam, pdict, offset, index, **kwargs
                    )

            # if message is being constructed rather than parsed from stream,
            # pad to nearest multiple of 4 bytes and calculate crc and length
            if self._crc == b"\x00\x00" and self._length == 0 and not self._nyi:
                padlen = (4 * ceil(offset / 4)) - offset
                self._payload += getpadding(padlen)
                self._do_len_checksum()

        except (
            AttributeError,
            struct.error,
            TypeError,
            ValueError,
        ) as err:
            raise SBFTypeError(
                (
                    f"Incorrect type for attribute '{anam}' "
                    f"in message class {self.identity}"
                )
            ) from err
        except (OverflowError,) as err:
            raise SBFTypeError(
                (
                    f"Overflow error for attribute '{anam}' "
                    f"in message class {self.identity}"
                )
            ) from err

    def _set_attribute(
        self, anam: str, pdict: dict, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param str anam: attribute name
        :param dict pdict: dict representing payload definition
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        adef = pdict[anam]  # get attribute definition
        # repeating group of attributes or subdefined bitfield
        if isinstance(adef, tuple):
            numr, _ = adef
            if numr in (X1, X2, X4, X6, X8, X24):  # bitfield
                if self._parsebf:  # if we're parsing bitfields
                    (offset, index) = self._set_attribute_bitfield(
                        adef, offset, index, **kwargs
                    )
                else:  # treat bitfield as a single byte array
                    offset = self._set_attribute_single(
                        anam, numr, offset, index, **kwargs
                    )
            elif isinstance(numr, tuple):  # conditional group of attributes
                (offset, index) = self._set_attribute_optional(
                    adef, offset, index, **kwargs
                )
            else:
                (offset, index) = self._set_attribute_group(
                    adef, offset, index, **kwargs
                )
        # single attribute
        else:
            offset = self._set_attribute_single(anam, adef, offset, index, **kwargs)

        return (offset, index)

    def _set_attribute_group(
        self, adef: tuple, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple adef: attribute definition - tuple of (num repeats, attribute dict)
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        sblen = 0  # specified sub block length
        index.append(0)  # add a (nested) group index
        anam, gdict = adef  # attribute signifying group size, group dictionary
        # derive or retrieve number of items in group
        if isinstance(anam, int):  # fixed number of repeats
            gsiz = anam
        else:  # number of repeats is defined in named attribute
            # "+n" suffix signifies that one or more nested group indices
            # must be appended to name e.g. "NSubBlock2_01", "NSubBlock2_02"
            if "+" in anam:
                anam, nestlevel = anam.split("+")
                for i in range(int(nestlevel)):
                    anam += f"_{index[i]:02d}"
            gsiz = getattr(self, anam)
            if anam == "RLMLength":  # special case for GALSARRLM
                gsiz = 5 if gsiz == 160 else 3
        # recursively process each group attribute,
        # incrementing the payload offset and index as we go
        for i in range(gsiz):
            sbcum = 0  # cumulative sub block length
            sboff = offset  # starting sub block payload offset
            index[-1] = i + 1
            for key1 in gdict:
                if key1 == PAD:  # sub block padding marker
                    # get sub block length from preceding SBLength attribute
                    # and derive length of sub block padding bytes
                    if gdict[PAD] in (PD, PD1, PD2):
                        sblen = getattr(self, gdict[PAD])
                        gdict[PAD] = f"P{(sblen - sbcum):03d}"
                (offset, index) = self._set_attribute(
                    key1, gdict, offset, index, **kwargs
                )
                # calculate cumulative sub block length
                sbcum = offset - sboff

        index.pop()  # remove this (nested) group index

        return (offset, index)

    def _set_attribute_optional(
        self, adef: tuple, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Process optional group of attributes, subject to condition being met:
        a) group is present if attribute value = specific value, otherwise absent
        b) group is present if attribute value is in specific range, otherwise absent

        :param tuple adef: attribute definition - tuple of ((attribute name, condition), group dict)
        :param int offset: payload offset in bits
        :param list index: repeating group index array
        :return: (offset, index[])
        :rtype: tuple
        """

        pres = False
        (anam, con), gdict = adef  # (attribute, condition), group dictionary
        # "+n" suffix signifies that one or more nested group indices
        # must be appended to name e.g. "N_01", "N_03"
        if "+" in anam:
            anam, nestlevel = anam.split("+")
            for i in range(int(nestlevel)):
                anam += f"_{index[i]:02d}"
        if isinstance(con, int):  # present if attribute == value
            pres = getattr(self, anam) == con
        elif isinstance(con, list):  # present if attribute in range of values
            pres = getattr(self, anam) in con

        if pres:  # if the conditional element is present...
            # recursively process each group attribute,
            # incrementing the payload offset as we go
            for anami in gdict:
                (offset, index) = self._set_attribute(
                    anami, gdict, offset, index, **kwargs
                )

        return (offset, index)

    def _set_attribute_single(
        self, anam: str, adef: object, offset: int, index: list, **kwargs
    ) -> int:
        """
        Set individual attribute value, applying scaling where appropriate.

        :param str anam: attribute keyword
        EITHER
        :param str adef: attribute definition string e.g. 'U002'
        OR
        :param list adef: if scaled, list of [attribute type string, scaling factor float]
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: offset
        :rtype: int

        """
        # pylint: disable=no-member

        # if attribute is scaled
        ares = 1
        if isinstance(adef, list):
            ares = adef[1]  # attribute resolution (i.e. scaling factor)
            adef = adef[0]  # attribute definition

        # if attribute is part of a (nested) repeating group, suffix name with index
        anami = anam
        for i in index:  # one index for each nested level
            if i > 0:
                anami += f"_{i:02d}"

        # determine attribute size (bytes)
        asiz = attsiz(adef)
        if atttyp(adef) == "V":  # variable by size
            asiz = len(self._payload) - offset  # assumed to fill remaining payload
            adef = f"V{asiz:03d}"

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            valb = self._payload[offset : offset + asiz]
            if ares == 1:
                val = bytes2val(valb, adef)
            else:
                val = round(bytes2val(valb, adef) * ares, SCALROUND)
        else:
            # if individual keyword has been provided,
            # set to provided value, else set to
            # nominal value
            val = kwargs.get(anami, nomval(adef))
            if ares == 1:
                valb = val2bytes(val, adef)
            else:
                valb = val2bytes(int(val / ares), adef)
            self._payload += valb

        if anam != PAD:  # don't bother to create padding attributes
            setattr(self, anami, val)

        return offset + asiz

    def _set_attribute_bitfield(
        self, atyp: str, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Parse bitfield attribute (type 'X').

        :param str atyp: attribute type e.g. 'X002'
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """
        # pylint: disable=no-member

        btyp, bdict = atyp  # type of bitfield, bitfield dictionary
        bsiz = attsiz(btyp)  # size of bitfield in bytes
        bfoffset = 0

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            bitfield = int.from_bytes(self._payload[offset : offset + bsiz], "little")
        else:
            bitfield = 0

        # process each flag in bitfield
        for key, keyt in bdict.items():
            (bitfield, bfoffset) = self._set_attribute_bits(
                bitfield, bfoffset, key, keyt, index, **kwargs
            )

        # update payload
        if "payload" not in kwargs:
            self._payload += bitfield.to_bytes(bsiz, "little")

        return (offset + bsiz, index)

    def _set_attribute_bits(
        self,
        bitfield: int,
        bfoffset: int,
        key: str,
        keyt: str,
        index: list,
        **kwargs,
    ) -> tuple:
        """
        Set individual bit flag from bitfield.

        :param int bitfield: bitfield
        :param int bfoffset: bitfield offset in bits
        :param str key: attribute key name
        :param str keyt: key type e.g. 'U001'
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (bitfield, bfoffset)
        :rtype: tuple

        """
        # pylint: disable=no-member

        # if attribute is part of a (nested) repeating group, suffix name with index
        keyr = key
        for i in index:  # one index for each nested level
            if i > 0:
                keyr += f"_{i:02d}"

        atts = attsiz(keyt)  # determine flag size in bits

        if "payload" in kwargs:
            val = (bitfield >> bfoffset) & ((1 << atts) - 1)
        else:
            val = kwargs.get(keyr, 0)
            bitfield = bitfield | (val << bfoffset)

        if key[0:8] != "reserved":  # don't bother to set reserved bits
            setattr(self, keyr, val)
        return (bitfield, bfoffset + atts)

    def _do_len_checksum(self):
        """
        Calculate and format payload length and checksum as bytes."""

        msgidb = msgid2bytes(self._msgid)
        payload = b"" if self._payload is None else self._payload
        self._length = len(payload) + 8  # add 8-byte header
        lenb = val2bytes(self._length, U2)
        self._crc = crc2bytes(msgidb + lenb + payload)

    def _get_dict(self, **kwargs) -> dict:
        """
        Get payload dictionary corresponding to message mode (GET/SET/POLL)
        Certain message types need special handling as alternate payload
        variants exist for the same SBFClass/SBFID/mode.

        :param kwargs: optional payload key/value pairs
        :return: dictionary representing payload definition
        :rtype: dict

        """

        try:
            pdict = SBF_BLOCKS[self._msgid]
            return pdict
        except KeyError as err:
            raise SBFMessageError(
                f"Unknown message type {escapeall(self._msgid)}."
            ) from err

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str

        """

        stg = f"<SBF({self.identity}, "
        if self._nyi:
            stg += "NOT YET IMPLEMENTED"
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                if att == "TOW":  # attribute is a GPS Time of Week
                    val = itow2utc(val)  # show time in UTC format
                stg += att + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"
        return stg.replace(", )>", ")>")

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return: machine readable representation
        :rtype: str

        """

        if self._payload is None:
            return f"SBFMessage({self._msgid})"
        return f"SBFMessage({self._msgid}, payload={self._payload})"

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation.

        :param str name: attribute name
        :param object value: attribute value
        :raises: SBFMessageError

        """

        if self._immutable:
            raise SBFMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """
        Serialize message.

        :return: serialized output
        :rtype: bytes

        """

        return (
            SBF_HDR
            + self._crc
            + msgid2bytes(self._msgid)
            + val2bytes(self._length, U2)
            + (b"" if self._payload is None else self._payload)
        )

    @property
    def identity(self) -> str:
        """
        Returns message identity in plain text form.

        :return: message identity e.g. 'PVTCartesian'
        :rtype: str

        """

        return self._msgid

    @property
    def payload(self) -> bytes:
        """
        Payload getter - returns the raw payload bytes.

        :return: raw payload as bytes
        :rtype: bytes

        """

        return self._payload
