"""
Static method tests for pysbf2

Created on 19 May 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
from datetime import datetime

from pysbf2 import (
    F4,
    F8,
    I4,
    U2,
    X2,
    SBFMessageError,
    SBFTypeError,
    attsiz,
    atttyp,
    bytes2val,
    escapeall,
    getpadding,
    itow2utc,
    msgid2bytes,
    nomval,
    utc2itow,
    val2bytes,
)

DIRNAME = os.path.dirname(__file__)


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testGetpadding(self):
        pad = getpadding(2)
        self.assertEqual(pad, b"\x01\x02")
        pad = getpadding(4)
        self.assertEqual(pad, b"\x01\x02\x03\x04")

    def testiTOW2utc(self):
        EXPECTED_RESULTS = (
            "10:01:23",
            "10:01:24",
            "10:01:25",
            "10:01:26",
            "10:01:27",
            "10:01:28",
            "10:01:29",
        )
        tows = (
            208901000,
            208902000,
            208903000,
            208904000,
            208905000,
            208906000,
            208907000,
        )
        i = 0
        for tow in tows:
            utc = itow2utc(tow)
            print(utc)
            self.assertEqual(str(utc), EXPECTED_RESULTS[i])
            i += 1

    def testutc2itow(self):
        dt = datetime(2024, 2, 8, 11, 31, 14)
        res = utc2itow(dt)
        self.assertEqual(res, (2300, 387092000))

    def testVal2Bytes(self):  # test conversion of value to bytes
        INPUTS = [
            (2345, U2),
            (-2346789, I4),
            (b"\x44\x55", X2),
            (23.12345678, F4),
            (-23.12345678912345, F8),
            ("testing123", "C010"),
        ]
        EXPECTED_RESULTS = [
            b"\x29\x09",
            b"\xdb\x30\xdc\xff",
            b"\x44\x55",
            b"\xd7\xfc\xb8\x41",
            b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0",
            b"testing123",
        ]
        for i, inp in enumerate(INPUTS):
            (val, att) = inp
            res = val2bytes(val, att)
            self.assertEqual(res, EXPECTED_RESULTS[i])
        with self.assertRaisesRegex(
            TypeError,
            "Attribute type U008 value X must be <class 'int'>, not <class 'str'>",
        ):
            res = val2bytes("X", "U008")
        with self.assertRaisesRegex(
            SBFTypeError,
            "Unknown attribute type Y008",
        ):
            res = val2bytes("X", "Y008")

    def testBytes2Val(self):  # test conversion of bytes to value
        INPUTS = [
            (b"\x29\x09", U2),
            (b"\xdb\x30\xdc\xff", I4),
            (b"\x44\x55", X2),
            (b"\xd7\xfc\xb8\x41", F4),
            (b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0", F8),
            (b"testing123", "C010"),
        ]
        EXPECTED_RESULTS = [
            2345,
            -2346789,
            b"\x44\x55",
            23.12345678,
            -23.12345678912345,
            b"testing123",
        ]
        for i, inp in enumerate(INPUTS):
            (valb, att) = inp
            res = bytes2val(valb, att)
            if att == F4:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 6)
            elif att == F8:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 14)
            else:
                self.assertEqual(res, EXPECTED_RESULTS[i])
        with self.assertRaisesRegex(SBFTypeError, "Unknown attribute type Y008"):
            res = bytes2val(23, "Y008")

    def testNomVal(self):
        self.assertEqual(nomval("U002"), 0)
        self.assertEqual(nomval("I002"), 0)
        self.assertEqual(nomval("F008"), 0)
        self.assertEqual(nomval("C003"), b"\x00\x00\x00")
        self.assertEqual(nomval("X002"), b"\x00\x00")
        self.assertEqual(nomval("P002"), b"\x00\x00")
        with self.assertRaisesRegex(SBFTypeError, "Unknown attribute type Y008"):
            res = nomval("Y008")

    def testattsiz(self):  # test attsiz
        self.assertEqual(attsiz("P003"), 3)
        self.assertEqual(attsiz("C032"), 32)

    def testatttyp(self):  # test attsiz
        self.assertEqual(atttyp("U004"), "U")
        self.assertEqual(atttyp("I032"), "I")

    def testescapeall(self):
        EXPECTED_RESULT = "b'\\x68\\x65\\x72\\x65\\x61\\x72\\x65\\x73\\x6f\\x6d\\x65\\x63\\x68\\x61\\x72\\x73'"
        val = b"herearesomechars"
        res = escapeall(val)
        print(res)
        self.assertEqual(res, EXPECTED_RESULT)

    def testmsgid2bytes(self):
        self.assertEqual(msgid2bytes("PVTCartesian"), b"\xa6\x0f")
        with self.assertRaisesRegex(
            SBFMessageError, "No SBF ID found for message NotExist"
        ):
            msgid2bytes("NotExist")
