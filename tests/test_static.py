"""
Static method tests for pysbf2

Created on 19 May 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest
import os

from pysbf2 import (
    itow2utc,
    bytes2val,
    val2bytes,
    U2,
    I4,
    X2,
    F4,
    F8,
    attsiz,
    atttyp,
    getpadding,
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

    def testVal2Bytes(self):  # test conversion of value to bytes
        INPUTS = [
            (2345, U2),
            (-2346789, I4),
            (b"\x44\x55", X2),
            (23.12345678, F4),
            (-23.12345678912345, F8),
        ]
        EXPECTED_RESULTS = [
            b"\x29\x09",
            b"\xdb\x30\xdc\xff",
            b"\x44\x55",
            b"\xd7\xfc\xb8\x41",
            b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0",
        ]
        for i, inp in enumerate(INPUTS):
            (val, att) = inp
            res = val2bytes(val, att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testBytes2Val(self):  # test conversion of bytes to value
        INPUTS = [
            (b"\x29\x09", U2),
            (b"\xdb\x30\xdc\xff", I4),
            (b"\x44\x55", X2),
            (b"\xd7\xfc\xb8\x41", F4),
            (b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0", F8),
        ]
        EXPECTED_RESULTS = [
            2345,
            -2346789,
            b"\x44\x55",
            23.12345678,
            -23.12345678912345,
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

    def testattsiz(self):  # test attsiz
        self.assertEqual(attsiz("CH"), -1)
        self.assertEqual(attsiz("C032"), 32)

    def testatttyp(self):  # test attsiz
        self.assertEqual(atttyp("U004"), "U")
        self.assertEqual(atttyp("I032"), "I")
