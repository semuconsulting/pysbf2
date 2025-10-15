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
    SBFTypeError,
    SBFReader,
    escapeall,
)

DIRNAME = os.path.dirname(__file__)


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    # def testTestConstruct(self):
    #     EXPECTED_RESULT = "<SBF(TestOnly, TOW=05:47:15.056000, WNc=2397, ScaledVal=1.278, Mode=1, ModeONE=0, SB1Length=8, SB2Length=4, N1=3, test1_01=1, test2_01=11, N2_01=2, test3_01_01=0, test4_01_01=0, test3_01_02=5, test4_01_02=0, test1_02=2, test2_02=22, N2_02=2, test3_02_01=0, test4_02_01=0, test3_02_02=6, test4_02_02=0, test1_03=3, test2_03=33, N2_03=3, test3_03_01=0, test4_03_01=0, test3_03_02=0, test4_03_02=0, test3_03_03=0, test4_03_03=7)>"
    #     EXPECTED_BYTES = b"\x24\x40\x03\x25\xd2\x04\x4c\x00\x40\x31\x3e\x01\x5d\x09\xec\x31\x00\x00\x01\x00\x08\x04\x03\x00\x01\x0b\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02\x16\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x03\x21\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00"
    #     msg1 = SBFMessage(
    #         "TestOnly",
    #         TOW=20853056,
    #         WNc=2397,
    #         ScaledVal=1.278,
    #         Mode=1,
    #         SB1Length=8,
    #         SB2Length=4,
    #         N1=3,
    #         test1_01=1,
    #         test1_02=2,
    #         test1_03=3,
    #         test2_01=11,
    #         test2_02=22,
    #         test2_03=33,
    #         N2_01=2,
    #         N2_02=2,
    #         N2_03=3,
    #         test3_01_02=5,
    #         test3_02_02=6,
    #         test4_03_03=7,
    #     )
    #     # print(f'"{msg1}"')
    #     # print(escapeall(msg1.serialize()))
    #     self.assertEqual(str(msg1), EXPECTED_RESULT)
    #     self.assertEqual(msg1.serialize(), EXPECTED_BYTES)
    #     msg2 = SBFReader.parse(msg1.serialize())
    #     self.assertEqual(str(msg2), EXPECTED_RESULT)
    #     print(escapeall(msg2.serialize()))
    #     self.assertEqual(msg2.serialize(), EXPECTED_BYTES)
    #     stream = BytesIO(msg2.serialize())
    #     sbr = SBFReader(stream, quitonerror=ERR_RAISE)
    #     for raw, parsed in sbr:
    #         self.assertEqual(str(parsed), EXPECTED_RESULT)
    #         self.assertEqual(raw, EXPECTED_BYTES)

    # def testTestConstructOptional(self):
    #     EXPECTED_RESULT1 = "<SBF(TestVariable, TOW=05:47:15.056000, WNc=2397, Mode=1, VariableONE=b'\\x00x\\x01x\\x02')>"
    #     EXPECTED_BYTES1 = b"\x24\x40\x99\x42\xd3\x04\x15\x00\x40\x31\x3e\x01\x5d\x09\x01\x00\x78\x01\x78\x02\x01"
    #     EXPECTED_RESULT2 = "<SBF(TestVariable, TOW=05:47:15.056000, WNc=2397, Mode=0, VariableZERO=b'\\x03x\\x04x\\x05')>"
    #     EXPECTED_BYTES2 = b"\x24\x40\xca\x11\xd3\x04\x15\x00\x40\x31\x3e\x01\x5d\x09\x00\x03\x78\x04\x78\x05\x01"
    #     msg1 = SBFMessage(
    #         "TestVariable",
    #         TOW=20853056,
    #         WNc=2397,
    #         ScaledVal=1.278,
    #         Mode=1,
    #         VariableONE=b"\x00x\01x\02",
    #     )
    #     msg2 = SBFMessage(
    #         "TestVariable",
    #         TOW=20853056,
    #         WNc=2397,
    #         ScaledVal=1.278,
    #         Mode=0,
    #         VariableZERO=b"\x03x\04x\05",
    #     )
    #     # print(f'"{msg1}"')
    #     # print(escapeall(msg1.serialize()))
    #     # print(f'"{msg2}"')
    #     # print(escapeall(msg2.serialize()))
    #     self.assertEqual(str(msg1), EXPECTED_RESULT1)
    #     self.assertEqual(msg1.serialize(), EXPECTED_BYTES1)
    #     self.assertEqual(str(msg2), EXPECTED_RESULT2)
    #     self.assertEqual(msg2.serialize(), EXPECTED_BYTES2)

    def testConstruct(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Type=4, Reserved1=0, AutoSet=0, 2D=0, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, Corr_OrbClkUsed=0, Corr_RngUsed=0, Corr_IonoUsed=0, Corr_OrbAccUsed=0, Corr_DO229Active=0, Corr_RTKType=2, Reserved2=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, RAIMIntegrity=0, GalHPCAFail=0, GalIonStorm=0, Reserved3=0, NrBases=0, PPPSeedAge=0, Reserved4=0, PPPSeedType=0, Latency=43, HAccuracy=122, VAccuracy=136, BaseARP=0, PhaseCtrOffset=0, Reserved5=0, ARPOffset=0)>"
        EXPECTED_BYTES = b"$@\xb7Y\xa6\x0f`\x00X\x9bs\x0c?\t\x04\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10@\x8f\x02\x8f\x02\r\t2P\x00\x00\x00\x00+\x00z\x00\x88\x00\x00\x01"
        EXPECTED_PAYLOAD = b"\x58\x9b\x73\x0c\x3f\x09\x04\x00\x1d\x0e\x58\x17\xfc\x04\x4d\x41\xe6\xe4\x8b\xe6\xea\x29\x02\xc1\x98\x19\x28\xb2\x18\x75\x53\x41\xa6\xdd\x41\x42\x51\x90\x01\x38\xb4\x86\x71\x3a\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6\x6e\x4b\x6c\xde\x3f\x03\xe0\x56\x3e\x00\x00\x10\x40\x8f\x02\x8f\x02\x0d\x09\x32\x50\x00\x00\x00\x00\x2b\x00\x7a\x00\x88\x00\x00\x01"
        EXPECTED_REPR = "SBFMessage(\"PVTCartesian\", payload=b'X\\x9bs\\x0c?\\t\\x04\\x00\\x1d\\x0eX\\x17\\xfc\\x04MA\\xe6\\xe4\\x8b\\xe6\\xea)\\x02\\xc1\\x98\\x19(\\xb2\\x18uSA\\xa6\\xddABQ\\x90\\x018\\xb4\\x86q:\\xc0\\x93\\x85\\xbb\\xf9\\x02\\x95\\xd0\\xe3\\xaf\\xe6nKl\\xde?\\x03\\xe0V>\\x00\\x00\\x10@\\x8f\\x02\\x8f\\x02\\r\\t2P\\x00\\x00\\x00\\x00+\\x00z\\x00\\x88\\x00\\x00\\x01')"
        res = SBFMessage(
            "PVTCartesian",
            TOW=208903000,
            WNc=2367,
            Type=4,
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
            Corr_RTKType=2,
            ReferenceID=655,
            MeanCorrAge=655,
            SignalInfo=1345456397,
            NrBases=0,
            PPPInfo=0,
            Latency=43,
            HAccuracy=122,
            VAccuracy=136,
            Misc=96,
        )
        # print(f'"{res}"')
        # print(escapeall(res.payload))
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)
        ser = res.serialize()
        # print(ser)
        self.assertEqual(ser, EXPECTED_BYTES)
        # print(str(repr(res)))
        self.assertEqual(str(repr(res)), EXPECTED_REPR)
        res2 = eval(repr(res))
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testConstructByteID(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Type=4, Reserved1=0, AutoSet=0, 2D=0, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, Corr_OrbClkUsed=0, Corr_RngUsed=0, Corr_IonoUsed=0, Corr_OrbAccUsed=0, Corr_DO229Active=0, Corr_RTKType=2, Reserved2=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, RAIMIntegrity=0, GalHPCAFail=0, GalIonStorm=0, Reserved3=0, NrBases=0, PPPSeedAge=0, Reserved4=0, PPPSeedType=0, Latency=43, HAccuracy=122, VAccuracy=136, BaseARP=0, PhaseCtrOffset=0, Reserved5=0, ARPOffset=0)>"
        res = SBFMessage(
            b"\xa6\x0f",
            TOW=208903000,
            WNc=2367,
            Type=4,
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
            Corr_RTKType=2,
            ReferenceID=655,
            MeanCorrAge=655,
            SignalInfo=1345456397,
            NrBases=0,
            PPPInfo=0,
            Latency=43,
            HAccuracy=122,
            VAccuracy=136,
            Misc=96,
        )
        # print(f'"{res}"')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testConstructNullPayload(self):
        EXPECTED_RES = "<SBF(FugroDDS, NOT YET IMPLEMENTED)>"
        EXPECTED_REPR = "SBFMessage(\"FugroDDS\", payload=b'')"
        res = SBFMessage(
            "FugroDDS",
            TOW=208903000,
            WNc=2367,
        )
        # print(res.payload)
        # print(repr(res))
        self.assertEqual(str(res), EXPECTED_RES)
        self.assertEqual(str(repr(res)), EXPECTED_REPR)

    def testAuxAntPositionsConstructParse(self):
        EXPECTED_STR = (
            "<SBF(AuxAntPositions, TOW=10:01:25, WNc=2367, N=1, SBLength=52, "
            "NrSV_01=7, Error_01=0, AmbiguityType_01=0, AuxAntID_01=2, "
            "DeltaEast_01=1.0, DeltaNorth_01=-2.0, DeltaUp_01=3.0, "
            "EastVel_01=0.5, NorthVel_01=-0.25, UpVel_01=0.125)>"
        )
        msg = SBFMessage(
            "AuxAntPositions",
            TOW=208903000,
            WNc=2367,
            N=1,
            SBLength=52,
            NrSV_01=7,
            Error_01=0,
            AmbiguityType_01=0,
            AuxAntID_01=2,
            DeltaEast_01=1.0,
            DeltaNorth_01=-2.0,
            DeltaUp_01=3.0,
            EastVel_01=0.5,
            NorthVel_01=-0.25,
            UpVel_01=0.125,
        )
        self.assertEqual(str(msg), EXPECTED_STR)
        self.assertEqual(len(msg.payload), 60)
        serial = msg.serialize()
        parsed = SBFReader.parse(serial)
        self.assertEqual(str(parsed), EXPECTED_STR)
        self.assertEqual(parsed.N, 1)
        self.assertEqual(parsed.SBLength, 52)
        self.assertEqual(parsed.NrSV_01, 7)
        self.assertAlmostEqual(parsed.UpVel_01, 0.125)

    def testConstructParse(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Type=4, Reserved1=0, AutoSet=0, 2D=0, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, Corr_OrbClkUsed=0, Corr_RngUsed=0, Corr_IonoUsed=0, Corr_OrbAccUsed=0, Corr_DO229Active=0, Corr_RTKType=2, Reserved2=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, RAIMIntegrity=0, GalHPCAFail=0, GalIonStorm=0, Reserved3=0, NrBases=0, PPPSeedAge=0, Reserved4=0, PPPSeedType=0, Latency=43, HAccuracy=122, VAccuracy=136, BaseARP=0, PhaseCtrOffset=0, Reserved5=0, ARPOffset=0)>"
        BYTES = b"$@\xb7Y\xa6\x0f`\x00X\x9bs\x0c?\t\x04\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10@\x8f\x02\x8f\x02\r\t2P\x00\x00\x00\x00+\x00z\x00\x88\x00\x00\x01"
        res = SBFReader.parse(BYTES)
        # print(f'"{res}"')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testConstructParseNoBitField(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=b'\\x04', Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=b'@', ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=b'\\x00', NrBases=0, PPPInfo=b'\\x00\\x00', Latency=43, HAccuracy=122, VAccuracy=136, Misc=b'\\x00')>"
        BYTES = b"$@\xb7Y\xa6\x0f`\x00X\x9bs\x0c?\t\x04\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10@\x8f\x02\x8f\x02\r\t2P\x00\x00\x00\x00+\x00z\x00\x88\x00\x00\x01"
        res = SBFReader.parse(BYTES, parsebitfield=False)
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
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Type=4, Reserved1=0, AutoSet=0, 2D=0, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, Corr_OrbClkUsed=0, Corr_RngUsed=0, Corr_IonoUsed=0, Corr_OrbAccUsed=0, Corr_DO229Active=0, Corr_RTKType=2, Reserved2=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, RAIMIntegrity=0, GalHPCAFail=0, GalIonStorm=0, Reserved3=0, NrBases=0, PPPSeedAge=0, Reserved4=0, PPPSeedType=0, Latency=43, HAccuracy=122, VAccuracy=136, BaseARP=0, PhaseCtrOffset=0, Reserved5=0, ARPOffset=0)>"
        BYTES = b"$@\xb7Y\xa6\x0f`\x00X\x9bs\x0c?\t\x04\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10@\x8f\x02\x8f\x02\r\t2P\x00\x00\x00\x00+\x00z\x00\x88\x00\x00\x01"
        stream = BytesIO(BYTES)
        sbr = SBFReader(stream)
        raw, parsed = sbr.read()
        # print(f'"{parsed}"')
        self.assertEqual(str(parsed), EXPECTED_RESULT)

    # def testConstructVariable(self):
    #     EXPECTED_RESULTS = (
    #         "<SBF(TestVariable, TOW=13:40:35.455000, WNc=2397, Mode=0, VariableZERO=b'\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\x01')>",
    #         "<SBF(TestVariable, TOW=13:40:35.455000, WNc=2397, Mode=1, VariableONE=b'\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x01\\x02\\x03')>",
    #     )
    #     BYTES = (
    #         b"\x24\x40\x43\x63\xd3\x04\x18\x00\x4f\x8c\xef\x02\x5d\x09\x00\x01\x02\x03\x04\x05\x06\x07\x08\x01",
    #         b"\x24\x40\xbf\x3c\xd3\x04\x29\x00\x4f\x8c\xef\x02\x5d\x09\x01\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x01\x02\x03",
    #     )
    #     stream = BytesIO(BYTES[0] + BYTES[1])
    #     sbr = SBFReader(stream)
    #     i = 0
    #     for raw, parsed in sbr:
    #         # print(f'"{parsed}"')
    #         self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
    #         i += 1
    #     self.assertEqual(i, len(EXPECTED_RESULTS))

    def testConstructInvalidType(self):
        with self.assertRaisesRegex(
            SBFTypeError,
            "Incorrect type for attribute 'Mode' in message class PVTCartesian",
        ):
            res = SBFMessage(
                "PVTCartesian",
                TOW=208903000,
                WNc=2367,
                Type="BAD",
            )
            # print(f'"{res}"')

    def testConstructUnknownID(self):
        with self.assertRaisesRegex(
            SBFMessageError,
            "Unknown SBF Message ID 4444",
        ):
            res = SBFMessage(
                4444,
                TOW=208903000,
                WNc=2367,
                Type=4,
            )
            # print(f'"{res}"')

    def testConstructOverflow(self):
        with self.assertRaisesRegex(
            SBFTypeError,
            "Overflow error for attribute 'NrSV' in message class PVTCartesian",
        ):
            res = SBFMessage(
                "PVTCartesian",
                TOW=208903000,
                WNc=2367,
                Type=4,
                Error=0,
                NrSV=9**10,
            )
            # print(f'"{res}"')

    def testConstructMutable(self):
        with self.assertRaisesRegex(
            SBFMessageError,
            "Object is immutable. Updates to NrSV not permitted after initialisation.",
        ):
            res = SBFMessage(
                "PVTCartesian",
                TOW=208903000,
                WNc=2367,
                Type=4,
                Error=0,
                NrSV=4,
            )
            res.NrSV = 6
