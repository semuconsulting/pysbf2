"""
sbftypes_decodes.py

SBF Protocol attribute value decode constants.

Created on 19 May 2025

Info sourced from mosaic-X5 Reference Guide v4.14.10 © 2000-2024 Septentrio NV/SA

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
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

PVTCARTESIAN_TIMESYSTEM = {
    0: "GPS time",
    1: "Galileo time",
    3: "GLONASS time",
    4: "BeiDou time",
    5: "QZSS time",
    100: "Fugro AtomiChron time",
}

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
