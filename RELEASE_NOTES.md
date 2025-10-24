# pysbf2 Release Notes

### RELEASE 1.0.2

1. Added Mosaic G5 P3(H) message definitions
   (https://www.septentrio.com/resources/mosaic-G5+P3/mosaic-G5+Firmware+v1.0.0+Reference+Guide.pdf):
    - 4251: BDSCNAV1
    - 4252: BDSCNAV2
    - 4253: BDSCNAV3
    - 4221: GPSRawL1C
    - 4272: NavCart
    - 4254: NavICLNav
    - 4227: QZSRawL1C
    - 4228: QZSRawL1S
    - 4246: QZSRawL5S
    - 4270: QZSRawL6D
    - 4271: QZSRawL6E
1. `NavBits` attribute in `SBF_NAVIGATION_PAGE_BLOCKS` rendered as single byte array rather than group of bytes.

### RELEASE 1.0.1

1. Minimum actively supported Python version updated to 3.10 (3.9 EOL 31 October 2025). 3.14rc2 added to actions.
1. Added Mosaic H `AuxAntPositions` message definition - thanks to @inuex35 for contribution.

### RELEASE 1.0.0

1. bit flag definitions enhanced in measEpoch and rawNav message types.
1. Development status updated to Production/Stable.

### RELEASE 0.2.0

1. ReceiverStatus bitflags added.
1. Min pyrtcm version updated to 1.1.8.
1. Development status updated to Beta.

### RELEASE 0.1.5

ENHANCEMENTS:

1. Fix `repr` function.
1. PVTCartesian bitflags updated.
1. Test coverage enhanced.
1. Minor updates to docstrings.

### RELEASE 0.1.4

FIXES:

1. Fix typos in message definitions - Commands, PTVCartesian, ExtEvent

ENHANCEMENTS:

1. Add bit flags (parsed when parsebitfield=True)
1. Update GitHub PR and Issue templates and other documentation.

### RELEASE 0.1.3

CHANGES:

1. Add DiffCorn message definition.
1. Test coverage enhanced.

### RELEASE 0.1.2

CHANGES:

1. SBF Message Definitions added

### RELEASE 0.1.0

CHANGES:

1. Initial Pre-Alpha release.

