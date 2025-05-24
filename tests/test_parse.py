"""
Parse method tests for pysbf2

Created on 19 May 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
from io import BytesIO

from pysbf2 import (
    ERR_RAISE,
    SBFMessage,
    SBFMessageError,
    SBFReader,
    escapeall,
)

DIRNAME = os.path.dirname(__file__)


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testTestConstruct(self):
        EXPECTED_RESULT = "<SBF(TestOnly, TOW=05:47:15.056000, WNc=2397, Mode=1, ModeONE=0, SB1Length=8, SB2Length=4, N1=3, test1_01=1, test2_01=11, N2_01=2, test3_01_01=0, test4_01_01=0, test3_01_02=5, test4_01_02=0, test1_02=2, test2_02=22, N2_02=2, test3_02_01=0, test4_02_01=0, test3_02_02=6, test4_02_02=0, test1_03=3, test2_03=33, N2_03=3, test3_03_01=0, test4_03_01=0, test3_03_02=0, test4_03_02=0, test3_03_03=0, test4_03_03=7)>"
        EXPECTED_BYTES = b"\x24\x40\x91\xa2\xd2\x04\x48\x00\x40\x31\x3e\x01\x5d\x09\x01\x00\x08\x04\x03\x00\x01\x0b\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02\x16\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x03\x21\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00"
        msg1 = SBFMessage(
            "TestOnly",
            TOW=20853056,
            WNc=2397,
            Mode=1,
            SB1Length=8,
            SB2Length=4,
            N1=3,
            test1_01=1,
            test1_02=2,
            test1_03=3,
            test2_01=11,
            test2_02=22,
            test2_03=33,
            N2_01=2,
            N2_02=2,
            N2_03=3,
            test3_01_02=5,
            test3_02_02=6,
            test4_03_03=7,
        )
        # print(f'"{msg1}"')
        # print(escapeall(msg1.serialize()))
        self.assertEqual(str(msg1), EXPECTED_RESULT)
        self.assertEqual(msg1.serialize(), EXPECTED_BYTES)
        msg2 = SBFReader.parse(msg1.serialize())
        self.assertEqual(str(msg2), EXPECTED_RESULT)
        print(escapeall(msg2.serialize()))
        self.assertEqual(
            msg2.serialize(), EXPECTED_BYTES
        )  # inconsequential extra padding byte?
        stream = BytesIO(msg2.serialize())
        sbr = SBFReader(stream, quitonerror=ERR_RAISE)
        for raw, parsed in sbr:
            self.assertEqual(str(parsed), EXPECTED_RESULT)
            self.assertEqual(raw, EXPECTED_BYTES)

    def testConstruct(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=122, VAccuracy=136, Misc=96)>"
        EXPECTED_BYTES = b"$@^b\xa6\x0f`\x00X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\x8f\x02\x8f\x02\r\t2P\x01\x00\x00\x00+\x00z\x00\x88\x00`\x01"
        res = SBFMessage(
            "PVTCartesian",
            TOW=208903000,
            WNc=2367,
            Mode=1,
            Error=0,
            X=3803640.1823747293,
            Y=-148797.3625715144,
            Z=5100642.783697508,
            Undulation=48.466453552246094,
            Vx=3.0890401831129566e-05,
            Vy=0.000921349273994565,
            Vz=-0.004076451063156128,
            COG=-20000000000.0,
            RxClkBias=0.47535978155315045,
            RxClkDrift=0.20983891189098358,
            TimeSystem=0,
            Datum=0,
            NrSV=16,
            WACorrInfo=0,
            ReferenceID=655,
            MeanCorrAge=655,
            SignalInfo=1345456397,
            AlertFlag=1,
            NrBases=0,
            PPPInfo=0,
            Latency=43,
            HAccuracy=122,
            VAccuracy=136,
            Misc=96,
        )
        # print(f'"{res}"')
        self.assertEqual(str(res), EXPECTED_RESULT)
        ser = res.serialize()
        # print(ser)
        self.assertEqual(ser, EXPECTED_BYTES)

    def testConstructParse(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=122, VAccuracy=136, Misc=96)>"
        BYTES = b"$@^b\xa6\x0f`\x00X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\x8f\x02\x8f\x02\r\t2P\x01\x00\x00\x00+\x00z\x00\x88\x00`\x01"
        res = SBFReader.parse(BYTES)
        # print(f'"{res}"')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testInvalidCRC(self):
        BYTES = b"$@^b\xa6\x0f`\x03X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\x8f\x02\x8f\x02\r\t2P\x01\x00\x00\x00+\x00z\x00\x88\x00`\x01"
        with self.assertRaisesRegex(
            SBFMessageError,
            "Invalid CRC b'\\\\x5e\\\\x62' - should be b'\\\\x87\\\\x5c'",
        ):
            res = SBFReader.parse(BYTES)

    def testConstructStream(self):  # TODO REMOVE AFTER ALPHA
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=122, VAccuracy=136, Misc=96)>"
        BYTES = b"$@^b\xa6\x0f`\x00X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\x8f\x02\x8f\x02\r\t2P\x01\x00\x00\x00+\x00z\x00\x88\x00`\x01"
        stream = BytesIO(BYTES)
        sbr = SBFReader(stream)
        raw, parsed = sbr.read()
        # print(f'"{res}"')
        self.assertEqual(str(parsed), EXPECTED_RESULT)

    def testConstructVariable(self):  # TODO REMOVE AFTER ALPHA
        EXPECTED_RESULTS = (
            "<SBF(TestVariable, TOW=13:40:35.455000, WNc=2397, Mode=0, VariableZERO=b'\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\x01')>",
            "<SBF(TestVariable, TOW=13:40:35.455000, WNc=2397, Mode=1, VariableONE=b'\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x01\\x02\\x03')>",
        )
        BYTES = (
            b"\x24\x40\x43\x63\xd3\x04\x18\x00\x4f\x8c\xef\x02\x5d\x09\x00\x01\x02\x03\x04\x05\x06\x07\x08\x01",
            b"\x24\x40\xbf\x3c\xd3\x04\x29\x00\x4f\x8c\xef\x02\x5d\x09\x01\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x01\x02\x03",
        )
        stream = BytesIO(BYTES[0] + BYTES[1])
        sbr = SBFReader(stream)
        i = 0
        for raw, parsed in sbr:
            # print(f'"{parsed}"')
            self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
            i += 1
        self.assertEqual(i, len(EXPECTED_RESULTS))
