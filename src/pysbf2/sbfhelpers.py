"""
sbfhelpers.py

Collection of SBF helper methods which can be used
outside the SBFMessage or SBFReader classes.

Created on 19 May 2025

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

import struct
from datetime import datetime, timedelta

from pysbf2.exceptions import SBFMessageError, SBFTypeError
from pysbf2.sbftypes_core import ATTTYPE, SBF_MSGIDS

EPOCH0 = datetime(1980, 1, 6)  # EPOCH start date
LEAPOFFSET = 18  # leap year offset in seconds, valid as from 1/1/2017
SIW = 604800  # seconds in week = 3600*24*7


def getpadding(length: int) -> bytes:
    """
    Generate specified number of padding bytes.

    :param length: length in bytes
    :return: bytes
    :rtype: bytes
    """

    pad = b""
    for i in range(length):
        pad += int.to_bytes(i + 1, 1, "little")
    return pad


def bytes2id(msgid: bytes) -> tuple:
    """
    Get message id and revision number from block ID.

    :param bytes msgid: ID as bytes
    :return: tuple of (msgid, revno)
    :rtype: tuple
    """

    mid = int.from_bytes(msgid, "little")
    msgid = mid & 0b0001111111111111
    revno = (mid & 0b1110000000000000) >> 13
    return msgid, revno


def calc_crc(message: bytes) -> int:
    """
    Perform CRC-CCIT cyclic redundancy check.

    :param bytes message: message
    :return: CRC or 0
    :rtype: int

    """

    poly = 0x1021
    crc = 0
    for byte in message:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1

            crc &= 0xFFFF
    return crc


def crc2bytes(message: bytes) -> bytes:
    """
    Generate CRC as 2 bytes, suitable for
    constructing RTCM message transport.

    :param bytes message: message including hdr and crc
    :return: CRC as 2 bytes
    :rtype: bytes
    """

    return calc_crc(message).to_bytes(2, "little")


def escapeall(val: bytes) -> str:
    """
    Escape all byte characters e.g. b'\\\\x73' rather than b`s`

    :param bytes val: bytes
    :return: string of escaped bytes
    :rtype: str
    """

    return "b'{}'".format("".join(f"\\x{b:02x}" for b in val))


def msgid2bytes(msgid: str) -> int:
    """
    Convert integer SBF message str to bytes.

    :param str msgid: message id e.g. "PVTCartesian"
    :return: message id as bytes e.g. b'\xa6\x0f' (4006)
    :rtype: bytes
    :raises: SBFMessageError

    """

    key = None
    for key, (mid, _) in SBF_MSGIDS.items():
        if msgid == mid:
            return int.to_bytes(key, 2, "little")
    raise SBFMessageError(f"No SBF ID found for message {msgid}")


def atttyp(att: str) -> str:
    """
    Helper function to return attribute type as string.

    :param str: attribute type e.g. 'U002'
    :return: type of attribute as string e.g. 'U'
    :rtype: str

    """

    return att[0:1]


def attsiz(att: str) -> int:
    """
    Helper function to return attribute size in bytes.

    :param str: attribute type e.g. 'U002'
    :return: size of attribute in bytes
    :rtype: int

    """

    return int(att[1:4])


def val2bytes(val, att: str) -> bytes:
    """
    Convert value to bytes for given SBF attribute type.

    :param object val: attribute value e.g. 25
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as bytes
    :rtype: bytes
    :raises: UBXTypeError

    """

    try:
        if not isinstance(val, ATTTYPE[atttyp(att)]):
            raise TypeError(
                f"Attribute type {att} value {val} must be {ATTTYPE[atttyp(att)]}, not {type(val)}"
            )
    except KeyError as err:
        raise SBFTypeError(f"Unknown attribute type {att}") from err
    valb = b""
    if atttyp(att) in ("X", "P", "V"):  # byte
        valb = val
    elif atttyp(att) == "C":  # char
        valb = val.encode("utf-8", "backslashreplace") if isinstance(val, str) else val
    elif atttyp(att) in ("E", "I", "L", "U"):  # integer
        valb = val.to_bytes(attsiz(att), byteorder="little", signed=atttyp(att) == "I")
    elif atttyp(att) == "F":  # floating point
        valb = struct.pack("<f" if attsiz(att) == 4 else "<d", float(val))
    # elif atttyp(att) == "A":  # array of unsigned integers
    #     valb = b""
    #     for i in range(attsiz(att)):
    #         valb += val[i].to_bytes(1, byteorder="little", signed=False)
    return valb


def bytes2val(valb: bytes, att: str) -> object:
    """
    Convert bytes to value for given SBF attribute type.

    :param bytes valb: attribute value in byte format e.g. b'\\\\x19\\\\x00\\\\x00\\\\x00'
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as int, float, str or bytes
    :rtype: object
    :raises: UBXTypeError

    """

    if atttyp(att) in ("X", "C", "P", "V"):
        val = valb
    elif atttyp(att) in ("I", "U"):  # integer
        val = int.from_bytes(valb, byteorder="little", signed=atttyp(att) == "I")
    elif atttyp(att) == "F":  # floating point
        val = struct.unpack("<f" if attsiz(att) == 4 else "<d", valb)[0]
    # elif atttyp(att) == "A":  # array of unsigned integers
    #     val = []
    #     for i in range(attsiz(att)):
    #         val.append(valb[i])
    else:
        raise SBFTypeError(f"Unknown attribute type {att}")
    return val


def nomval(att: str) -> object:
    """
    Get nominal value for given SBF attribute type.

    :param str att: attribute type e.g. 'U004'
    :return: attribute value as int, float, str or bytes
    :rtype: object
    :raises: UBXTypeError

    """

    if atttyp(att) in ("X", "C", "P", "V"):
        val = b"\x00" * attsiz(att)
    elif atttyp(att) == "F":
        val = 0.0
    elif atttyp(att) in ("I", "U"):
        val = 0
    # elif atttyp(att) == "A":  # array of unsigned integers
    #     val = [0] * attsiz(att)
    else:
        raise SBFTypeError(f"Unknown attribute type {att}")
    return val


def itow2utc(itow: int) -> datetime.time:
    """
    Convert GPS Time Of Week to UTC time

    :param int itow: GPS Time Of Week in milliseconds
    :return: UTC time hh.mm.ss
    :rtype: datetime.time

    """

    utc = EPOCH0 + timedelta(seconds=(itow / 1000) - LEAPOFFSET)
    return utc.time()


def utc2itow(utc: datetime) -> tuple:
    """
    Convert UTC datetime to GPS Week Number, Time Of Week

    :param datetime utc: datetime
    :return: GPS Week Number, Time of Week in milliseconds
    :rtype: tuple

    """

    wno = int((utc - EPOCH0).total_seconds() / SIW)
    sow = EPOCH0 + timedelta(seconds=wno * SIW)
    itow = int(((utc - sow).total_seconds() + LEAPOFFSET) * 1000)
    return wno, itow
