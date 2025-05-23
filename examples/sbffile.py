"""
sbffile.py

Usage:

python3 sbffile.py filename=pygpsdata.log

This example illustrates a simple example implementation of a
SBFMessage and/or NMEAMessage binary logfile reader using the
SBFReader iterator functions and an external error handler.

Created on 19 May 2025

@author: semuadmin
"""

from sys import argv

from pysbf2.sbfreader import (
    ERR_LOG,
    SBF_PROTOCOL,
    VALCKSUM,
    SBFReader,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
)


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def main(**kwargs):
    """
    Main Routine.
    """

    filename = kwargs.get("filename", "pygpsdata.log")

    print(f"Opening file {filename}...")
    with open(filename, "rb") as stream:

        count = 0

        ubr = SBFReader(
            stream,
            protfilter=SBF_PROTOCOL | NMEA_PROTOCOL | RTCM3_PROTOCOL,
            quitonerror=ERR_LOG,
            validate=VALCKSUM,
            errorhandler=errhandler,
        )
        for _, parsed_data in ubr:
            print(parsed_data)
            count += 1

    print(f"\n{count} messages read.\n")
    print("Test Complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
