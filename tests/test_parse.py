"""
Parse method tests for pyubx2.UBXMessage

Created on 19 May 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest
import os
from datetime import datetime

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

    def testConstruct(self):
        EXPECTED_RESULT = "<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=65535, MeanCorrAge=655.35, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=0.0043, HAccuracy=12.2, VAccuracy=13.66, Misc=96)>"
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
            ReferenceID=65535,
            MeanCorrAge=655.35,
            SignalInfo=1345456397,
            AlertFlag=1,
            NrBases=0,
            PPPInfo=0,
            Latency=0.0043,
            HAccuracy=12.2,
            VAccuracy=13.66,
            Misc=96,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testParsed(self):
        EXPECTED_RESULT = (
            "<SBF(PVTCartesian, TOW=13:31:50, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=65535, MeanCorrAge=655.35, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=0.0043, HAccuracy=12.2, VAccuracy=13.66, Misc=96)>",
            "<SBF(PosCovCartesian, TOW=13:31:50, WNc=2367, Mode=1, Error=0, Cov_xx=53.1199836730957, Cov_yy=5.652109146118164, Cov_zz=25.088281631469727, Cov_bb=39.93962097167969, Cov_xy=3.686392307281494, Cov_xz=12.170706748962402, Cov_xb=35.005733489990234, Cov_yz=-2.246225118637085, Cov_yb=-1.8030028343200684, Cov_zb=26.093219757080078)>",
            "<SBF(VelCovCartesian, TOW=13:31:50, WNc=2367, Mode=1, Error=0, Cov_VxVx=0.00023558673274237663, Cov_VyVy=6.692630267934874e-05, Cov_VzVz=0.0001448081893613562, Cov_DtDt=0.00024842823040671647, Cov_VxVy=-1.3887978639104404e-05, Cov_VxVz=1.2771502042596694e-05, Cov_VxDt=0.00011763897055061534, Cov_VyVz=-2.352825686102733e-05, Cov_VyDt=-4.3235981138423085e-05, Cov_VzDt=9.187815885525197e-05)>",
            "<SBF(BaseVectorCart, TOW=13:31:50, WNc=2367, NSubBlock=0, SBLength=52)>",
            "<SBF(PVTCartesian, TOW=13:31:51, WNc=2367, Mode=1, Error=0, X=3803640.251024515, Y=-148797.3624270166, Z=5100642.778343539, Undulation=48.466453552246094, Vx=-0.005239022895693779, Vy=0.004101206548511982, Vz=-0.002389088273048401, COG=-20000000000.0, RxClkBias=0.47556991589153874, RxClkDrift=0.20985932648181915, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=65535, MeanCorrAge=655.35, SignalInfo=1345454349, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=0.0044, HAccuracy=11.99, VAccuracy=13.17, Misc=96)>",
            "<SBF(PosCovCartesian, TOW=13:31:51, WNc=2367, Mode=1, Error=0, Cov_xx=50.27727508544922, Cov_yy=5.232242584228516, Cov_zz=23.757936477661133, Cov_bb=35.62702560424805, Cov_xy=2.2724266052246094, Cov_xz=10.625672340393066, Cov_xb=31.73499870300293, Cov_yz=-2.705791711807251, Cov_yb=-2.5999596118927, Cov_zb=23.782268524169922)>",
            "<SBF(VelCovCartesian, TOW=13:31:51, WNc=2367, Mode=1, Error=0, Cov_VxVx=0.00023734608839731663, Cov_VyVy=7.352886314038187e-05, Cov_VzVz=0.00014485169958788902, Cov_DtDt=0.00026211829390376806, Cov_VxVy=-1.437065930076642e-05, Cov_VxVz=1.4697610822622664e-05, Cov_VxDt=0.00012056239211233333, Cov_VyVz=-2.448483428452164e-05, Cov_VyDt=-5.166120172361843e-05, Cov_VzDt=9.319968376075849e-05)>",
            "<SBF(BaseVectorCart, TOW=13:31:51, WNc=2367, NSubBlock=0, SBLength=52)>",
        )
        with open(os.path.join(DIRNAME, "pygpsdata_X5.log"), "rb") as stream:
            sbr = SBFReader(
                stream,
                validate=VALCKSUM,
                protfilter=SBF_PROTOCOL,
                quitonerror=ERR_LOG,
                parsing=True,
            )
            i = 0
            for raw, parsed in sbr:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULT[i])
                i += 1
                if i > 7:
                    break
        self.assertEqual(i, len(EXPECTED_RESULT))
