"""
Parse method tests for pysbf2

Created on 19 May 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest
import os
from io import BytesIO

from pysbf2 import (
    SBFReader,
    SBFMessage,
    SBF_PROTOCOL,
    VALNONE,
    VALCKSUM,
    escapeall,
    NMEA_PROTOCOL,
    ERR_LOG,
    ERR_RAISE,
    itow2utc,
)

DIRNAME = os.path.dirname(__file__)


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

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

    def testConstructStream(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=122, VAccuracy=136, Misc=96)>"
        BYTES = b"$@^b\xa6\x0f`\x00X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\x8f\x02\x8f\x02\r\t2P\x01\x00\x00\x00+\x00z\x00\x88\x00`\x01"
        stream = BytesIO(BYTES)
        sbr = SBFReader(stream)
        raw, parsed = sbr.read()
        # print(f'"{res}"')
        self.assertEqual(str(parsed), EXPECTED_RESULT)
