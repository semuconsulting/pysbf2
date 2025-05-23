"""
sbftypes_core.py

SBF Protocol core globals, constants, datatypes and message identifiers.

Created on 19 May 2025

Info sourced from mosaic-X5 Reference Guide v4.14.10 © 2000-2024 Septentrio NV/SA

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

SBF_HDR = b"\x24\x40"  # "$@'
"""SBF message header"""

ERR_RAISE = 2
"""Raise error and quit"""
ERR_LOG = 1
"""Log errors"""
ERR_IGNORE = 0
"""Ignore errors"""
NMEA_PROTOCOL = 1
"""NMEA Protocol"""
RTCM3_PROTOCOL = 4
"""RTCM3 Protocol"""
SBF_PROTOCOL = 2
"""SBF Protocol"""
VALNONE = 0
"""Do not validate checksum"""
VALCKSUM = 1
"""Validate checksum"""

# scaling factor constants
SCAL9 = 1e-9  # 0.000000001
SCAL8 = 1e-8  # 0.00000001
SCAL7 = 1e-7  # 0.0000001
SCAL6 = 1e-6  # 0.000001
SCAL5 = 1e-5  # 0.00001
SCAL4 = 1e-4  # 0.0001
SCAL3 = 1e-3  # 0.001
SCAL2 = 1e-2  # 0.01
SCAL1 = 1e-1  # 0.1
SCALROUND = 12  # number of dp to round scaled attributes to

# derived group numerations
RTCM2N = "_RTCM2N"
CMRN = "_CMRN"
RTCM3N = "_RTCM3N"
RTCMVN = "_RTCMVN"
PAD = "_Padding"
VAR = "_VarLen"

# **************************************************
# THESE ARE THE SBF PROTOCOL PAYLOAD ATTRIBUTE TYPES
# **************************************************
C1 = "C001"  # ASCII / ISO 8859.1 Encoding 1 bytes
C2 = "C002"  # ASCII / ISO 8859.1 Encoding 2 bytes
C3 = "C003"  # ASCII / ISO 8859.1 Encoding 3 bytes
C6 = "C006"  # ASCII / ISO 8859.1 Encoding 6 bytes
C9 = "C009"  # ASCII / ISO 8859.1 Encoding 9 bytes
C10 = "C010"  # ASCII / ISO 8859.1 Encoding 10 bytes
C20 = "C020"  # ASCII / ISO 8859.1 Encoding 20 bytes
C21 = "C021"  # ASCII / ISO 8859.1 Encoding 21 bytes
C30 = "C030"  # ASCII / ISO 8859.1 Encoding 30 bytes
C32 = "C032"  # ASCII / ISO 8859.1 Encoding 32 bytes
C40 = "C040"  # ASCII / ISO 8859.1 Encoding 40 bytes
C60 = "C060"  # ASCII / ISO 8859.1 Encoding 60 bytes
I1 = "I001"  # Signed Int 2's complement 1 byte
I2 = "I002"  # Signed Int 2's complement 2 bytes
I4 = "I004"  # Signed Int 2's complement 4 bytes
I8 = "I008"  # Signed Int 2's complement 8 bytes
U1 = "U001"  # Unsigned Int 1 byte
U2 = "U002"  # Unsigned Int 2 bytes
U3 = "U003"  # Unsigned Int 3 bytes
U4 = "U004"  # Unsigned Int 4 bytes
U6 = "U006"  # Unsigned Int 6 bytes
U8 = "U008"  # Unsigned Int 8 bytes
U16 = "U016"  # Unsigned Int 16 bytes
U20 = "U020"  # Unsigned Int 20 bytes
F4 = "F004"  # Float (IEEE 754) Single Precision 4 bytes
F8 = "F008"  # Float (IEEE 754) Double Precision 8 bytes
X1 = "X001"  # Bitfield 1 byte
X2 = "X002"  # Bitfield 2 bytes
X4 = "X004"  # Bitfield 4 bytes
X6 = "X006"  # Bitfield 6 bytes
X8 = "X008"  # Bitfield 8 bytes
X24 = "X024"  # Bitfield 24 bytes
V2 = "V002"  # variable number of U2
V4 = "V004"  #  variable number of U4
PD = "SBLength"  # Sub-block padding marker single level
PD1 = "SB1Length"  # Sub-block padding marker level 1
PD2 = "SB2Length"  # Sub-block padding marker level 2

ATTTYPE = {
    "C": (type(b"0"), type("0")),
    "F": (type(0), type(0.1)),
    "I": type(-1),
    "P": type(b"0"),
    "U": type(0),
    "V": type(b"0"),
    "X": type(b"0"),
}
"""Permissible attribute types"""

# ********************************************************************
# THESE ARE THE SBF PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in sbftypes_blocks
# ********************************************************************
SBF_MSGIDS = {
    4075: ("ASCIIIn", "ASCII input from external sensor"),
    5939: ("AttCovEuler", "Covariance matrix of attitude"),
    5938: ("AttEuler", "GNSS attitude expressed as Euler angles"),
    5949: ("BaseStation", "Base station coordinates"),
    4043: (
        "BaseVectorCart",
        "XYZ relative position and velocity with respect to base(s)",
    ),
    4028: (
        "BaseVectorGeod",
        "ENU relative position and velocity with respect to base(s)",
    ),
    4040: ("BBSamples", "Baseband samples"),
    4119: ("BDSAlm", "Almanac data for a BeiDou satellite"),
    4120: ("BDSIon", "BeiDou Ionospheric delay model parameters"),
    4081: ("BDSNav", "BeiDou ephemeris and clock"),
    4047: ("BDSRaw", "BeiDou navigation page"),
    4218: ("BDSRawB1C", "BeiDou B1C navigation frame"),
    4219: ("BDSRawB2a", "BeiDou B2a navigation frame"),
    4242: ("BDSRawB2b", "BeiDou B2b navigation frame"),
    4121: ("BDSUtc", "BDT-UTC data"),
    4013: ("ChannelStatus", "Status of the tracking for all receiver channels"),
    4015: ("Commands", "Commands entered by the user"),
    5936: ("Comment", "Comment entered by the user"),
    5919: ("DiffCorrIn", "Incoming RTCM or CMR message"),
    4059: ("DiskStatus", "Internal logging status"),
    4001: ("DOP", "Dilution of precision"),
    4105: ("DynDNSStatus", "DynDNS status"),
    4097: ("EncapsulatedOutput", "SBF encapsulation of non-SBF messages"),
    5943: ("EndOfAtt", "GNSS attitude epoch marker"),
    5922: ("EndOfMeas", "Measurement epoch marker"),
    5921: ("EndOfPVT", "PVT epoch marker"),
    5924: ("ExtEvent", "Time at the instant of an external event"),
    4237: (
        "ExtEventAttEuler",
        "GNSS attitude expressed as Euler angles at the instant of an event",
    ),
    4217: (
        "ExtEventBaseVectGeod",
        "ENU relative position with respect to base(s) at the instant of an event",
    ),
    4037: ("ExtEventPVTCartesian", "Cartesian position at the instant of an event"),
    4038: ("ExtEventPVTGeodetic", "Geodetic position at the instant of an event"),
    4211: ("FugroDDS", "DDS (Debug Data Stream) from Fugro"),
    4214: ("FugroStatus", "Fugro Status Information"),
    4003: ("GALAlm", "Almanac data for a Galileo satellite"),
    4245: ("GALAuthStatus", "Galileo OSNMA authentication status"),
    4032: ("GALGstGps", "GST-GPS data"),
    4030: ("GALIon", "NeQuick Ionosphere model parameters"),
    4002: ("GALNav", "Galileo ephemeris, clock, health and BGD"),
    4024: ("GALRawCNAV", "Galileo C/NAV navigation page"),
    4022: ("GALRawFNAV", "Galileo F/NAV navigation page"),
    4023: ("GALRawINAV", "Galileo I/NAV navigation page"),
    4034: ("GALSARRLM", "Search-and-rescue return link message"),
    4031: ("GALUtc", "GST-UTC data"),
    5897: ("GEOAlm", "MT17 : SBAS satellite almanac"),
    5934: ("GEOClockEphCovMatrix", "MT28 : Clock-Ephemeris Covariance Matrix"),
    5930: ("GEODegrFactors", "MT10 : Degradation factors"),
    5927: ("GEOFastCorr", "MT02-05/24: Fast Corrections"),
    5929: ("GEOFastCorrDegr", "MT07 : Fast correction degradation factors"),
    5931: ("GEOIGPMask", "MT18 : Ionospheric grid point mask"),
    5928: ("GEOIntegrity", "MT06 : Integrity information"),
    5933: ("GEOIonoDelay", "MT26 : Ionospheric delay corrections"),
    5932: ("GEOLongTermCorr", "MT24/25 : Long term satellite error corrections"),
    5925: ("GEOMT00", "MT00 : SBAS Don't use for safety applications"),
    5896: ("GEONav", "MT09 : SBAS navigation message"),
    5918: ("GEONetworkTime", "MT12 : SBAS Network Time/UTC offset parameters"),
    5926: ("GEOPRNMask", "MT01 : PRN Mask assignments"),
    4020: ("GEORawL1", "SBAS L1 navigation message"),
    4021: ("GEORawL5", "SBAS L5 navigation message"),
    5917: ("GEOServiceLevel", "MT27 : SBAS Service Message"),
    4005: ("GLOAlm", "Almanac data for a GLONASS satellite"),
    4004: ("GLONav", "GLONASS ephemeris and clock"),
    4026: ("GLORawCA", "GLONASS CA navigation string"),
    4036: ("GLOTime", "GLO-UTC, GLO-GPS and GLO-UT1 data"),
    5892: ("GPSAlm", "Almanac data for a GPS satellite"),
    4042: ("GPSCNav", "CNAV Ephemeris data for one satellite."),
    5893: ("GPSIon", "Ionosphere data from the GPS subframe 5"),
    5891: ("GPSNav", "GPS ephemeris and clock"),
    4017: ("GPSRawCA", "GPS CA navigation subframe"),
    4018: ("GPSRawL2C", "GPS L2C navigation frame"),
    4019: ("GPSRawL5", "GPS L5 navigation frame"),
    5894: ("GPSUtc", "GPS-UTC data from GPS subframe 5"),
    4090: ("InputLink", "Statistics on input streams"),
    4058: ("IPStatus", "IP address, gateway and MAC address of Ethernet interface"),
    4204: ("LBandBeams", "L-band satellite/beam information"),
    4212: ("LBandRaw", "L-Band raw user data"),
    4201: ("LBandTrackerStatus", "Status of the L-band signal tracking"),
    4110: (
        "Meas3CN0HiRes",
        "Extension of Meas3Ranges containing fractional C/N0 values",
    ),
    4111: ("Meas3Doppler", "Extension of Meas3Ranges containing Doppler values"),
    4113: (
        "Meas3MP",
        "Extension of Meas3Ranges containing multipath corrections applied by",
    ),
    4112: (
        "Meas3PP",
        "Extension of Meas3Ranges containing proprietary flags for data postprocessing.",
    ),
    4109: ("Meas3Ranges", "Code, phase and CN0 measurements"),
    4027: ("MeasEpoch", "Measurement set of one epoch"),
    4000: ("MeasExtra", "Additional info such as observable variance"),
    4093: ("NAVICRaw", "NavIC/IRNSS subframe"),
    4053: ("NTRIPClientStatus", "NTRIP client connection status"),
    4122: ("NTRIPServerStatus", "NTRIP server connection status"),
    4091: ("OutputLink", "Statistics on output streams"),
    4238: ("P2PPStatus", "P2PP client/server status"),
    4044: ("PosCart", "Position, variance and baseline in Cartesian coordinates"),
    5905: ("PosCovCartesian", "Position covariance matrix (X,Y, Z)"),
    5906: ("PosCovGeodetic", "Position covariance matrix (Lat, Lon, Alt)"),
    4052: ("PosLocal", "Position in a local datum"),
    4094: ("PosProjected", "Plane grid coordinates"),
    4006: (
        "PVTCartesian",
        "GNSS position, velocity, and time in Cartesian coordinates",
    ),
    4007: ("PVTGeodetic", "GNSS position, velocity, and time in geodetic coordinates"),
    4076: ("PVTSupport", "Internal parameters for maintenance and support"),
    4079: ("PVTSupportA", "Internal parameters for maintenance and support"),
    4082: ("QualityInd", "Quality indicators"),
    4116: ("QZSAlm", "Almanac data for a QZSS satellite"),
    4095: ("QZSNav", "QZSS ephemeris and clock"),
    4066: ("QZSRawL1CA", "QZSS L1C/A or L1C/B navigation frame"),
    4067: ("QZSRawL2C", "QZSS L2C navigation frame"),
    4068: ("QZSRawL5", "QZSS L5 navigation frame"),
    5902: ("ReceiverSetup", "General information about the receiver installation"),
    4014: ("ReceiverStatus", "Overall status information of the receiver"),
    5914: ("ReceiverTime", "Current receiver and UTC time"),
    4092: ("RFStatus", "Radio-frequency interference mitigation status"),
    4049: ("RTCMDatum", "Datum information from the RTK service provider"),
    4103: ("RxMessage", "Receiver message"),
    4012: ("SatVisibility", "Azimuth/elevation of visible satellites"),
    5907: ("VelCovCartesian", "Velocity covariance matrix (X, Y, Z)"),
    5908: ("VelCovGeodetic", "Velocity covariance matrix (North, East, Up)"),
    5911: ("xPPSOffset", "Offset of the xPPS pulse with respect to GNSS time"),
    # TODO REMOVE AFTER ALPHA...
    1234: ("TestOnly", "Test Message - Do Not Use"),
    1235: ("TestVariable", "Variable Length Test Message - Do Not Use"),
}
