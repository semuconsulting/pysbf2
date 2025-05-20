"""
SBF Custom Exception Types.

Created on 19 May 2025

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""


class ParameterError(Exception):
    """Parameter Error Class."""


class GNSSStreamError(Exception):
    """Generic Stream Error Class."""


class SBFParseError(Exception):
    """
    SBF Parsing error.
    """


class SBFStreamError(Exception):
    """
    SBF Streaming error.
    """


class SBFMessageError(Exception):
    """
    SBF Undefined message class/id.
    Essentially a prompt to add missing payload types to SBF_PAYLOADS.
    """


class SBFTypeError(Exception):
    """
    SBF Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to SBF_PAYLOADS.
    """
