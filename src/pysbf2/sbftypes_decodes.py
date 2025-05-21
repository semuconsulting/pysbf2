"""
sbftypes_decodes.py

SBF Protocol attribute value decode constants.

Created on 19 May 2025

Info sourced from mosaic-X5 Reference Guide v4.14.10 © 2000-2024 Septentrio NV/SA

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

SIGNAL_NUMBER = {
    0: ("L1CA", "GPS", 1575.4, "1C"),
    1: ("L1P", "GPS", 1575.42, "1W"),
    2: ("L2P", "GPS", 1227.60, "2W"),
    3: ("L2C", "GPS", 1227.60, "2L"),
    4: ("L5", "GPS", 1176.45, "5Q"),
    5: ("L1C", "GPS", 1575.42, "1L"),
    6: ("L1CA", "QZSS", 1575.42, "1C"),
    7: ("L2C", "QZSS", 1227.60, "2L"),
    8: ("L1CA", "GLONASS", 1602.00, "1C"),
    9: ("L1P", "GLONASS", 1602.00, "1P"),
    10: ("L2P", "GLONASS", 1246.00, "2P"),
    11: ("L2CA", "GLONASS", 1246.00, "2C"),
    12: ("L3", "GLONASS", 1202.025, "3Q"),
    13: ("B1C", "BeiDou", 1575.42, "1P"),
    14: ("B2a", "BeiDou", 1176.45, "5P"),
    15: ("L5", "NavIC", 1176.45, "5A"),
    16: ("Reserved", "", 0, ""),
    17: ("E1", "Galileo", 1575.42, "1C"),
    18: ("Reserved", "", 0, ""),
    19: ("E6", "Galileo", 1278.75, "6C/6B"),
    20: ("E5a", "Galileo", 1176.45, "5Q"),
    21: ("E5b", "Galileo", 1207.14, "7Q"),
    22: ("E5 AltBOC", "Galileo", 1191.795, "8Q"),
    23: ("LBand", "MSS", 0, "NA"),
    24: ("L1CA", "SBAS", 1575.42, "1C"),
    25: ("L5", "SBAS", 1176.45, "5I"),
    26: ("L5", "QZSS", 1176.45, "5Q"),
    27: ("L6", "QZSS", 1278.75, ""),
    28: ("B1I", "BeiDou", 1561.098, "2I"),
    29: ("B2I", "BeiDou", 1207.14, "7I"),
    30: ("B3I", "BeiDou", 1268.52, "6I"),
    31: ("Reserved", "", 0, ""),
    32: ("L1C", "QZSS", 1575.42, "1L"),
    33: ("L1S", "QZSS", 1575.42, "1Z"),
    34: ("B2b", "BeiDou", 1207.14, "7D"),
    35: ("Reserved", "", 0, ""),
    36: ("Reserved", "", 0, ""),
    37: ("Reserved", "", 0, ""),
    38: ("L1CB", "QZSS", 1575.42, "1E"),
    39: ("L5S", "QZSS", 1176.45, "5P"),
}
"""
Signal Numbering Decode

Number: (Signal Code, Constellation, Base Frequency, RINEX Code)
"""

# bits 0-3
PVTCARTESIAN_MODE = {
    0: "No GNSS PVT available",
    1: "Stand-Alone PVT",
    2: "Differential PVT",
    3: "Fixed location",
    4: "RTK with fixed ambiguities",
    5: "RTK with float ambiguities",
    6: "SBAS aided PVT",
    7: "Moving-base RTK with fixed ambiguities",
    8: "Moving-base RTK with float ambiguities",
    9: "Reserved",
    10: "Precise Point Positioning (PPP)",
    12: "Reserved",
}
"""Mode decode"""

PVTCARTESIAN_ERROR = {
    0: "No Error",
    1: "Not enough measurements",
    2: "Not enough ephemerides available",
    3: "DOP too large (larger than 15)",
    4: "Sum of squared residuals too large",
    5: "No convergence",
    6: "Not enough measurements after outlier rejection",
    7: "Position output prohibited due to export laws",
    8: "Not enough differential corrections available",
    9: "Base station coordinates unavailable",
    10: "Ambiguities not fixed and user requested to only output RTKfixed",
}
"""Error decode"""

PVTCARTESIAN_TIMESYSTEM = {
    0: "GPS time",
    1: "Galileo time",
    3: "GLONASS time",
    4: "BeiDou time",
    5: "QZSS time",
    100: "Fugro AtomiChron time",
}
"""Timesystem decode"""

PVTCARTESIAN_DATUM = {
    0: "WGS84/ITRS",
    19: "Datum equal to that used by the DGNSS/RTK base station",
    30: "ETRS89 (ETRF2000 realization)",
    31: "NAD83(2011), North American Datum (2011)",
    32: "NAD83(PA11), North American Datum, Pacific plate (2011)",
    33: "NAD83(MA11), North American Datum, Marianas plate (2011)",
    34: "GDA94(2010), Geocentric Datum of Australia (2010)",
    35: "GDA2020, Geocentric Datum of Australia 2020",
    36: "JGD2011, Japanese Geodetic Datum 2011",
    250: "First user-defined datum",
    251: "Second user-defined datum",
}
"""Datum decode"""
