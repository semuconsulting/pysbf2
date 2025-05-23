pysbf2
=======

[Current Status](#currentstatus) |
[Installation](#installation) |
[Message Categories](#msgcat) |
[Reading](#reading) |
[Parsing](#parsing) |
[Generating](#generating) |
[Serializing](#serializing) |
[Examples](#examples) |
[Extensibility](#extensibility) |
[Known Issues](#knownissues) |
[Author & License](#author)

# WORK IN PROGRESS

`pysbf2` is an original Python 3 parser for the SBF &copy; protocol. SBF is a proprietary binary protocol implemented on Septentrio &trade; GNSS receiver modules. `pysbf2` can also parse NMEA 0183 &copy; and RTCM3 &copy; protocols via the underlying [`pynmeagps`](https://github.com/semuconsulting/pynmeagps) and [`pyrtcm`](https://github.com/semuconsulting/pyrtcm) packages from the same author - hence it covers all the common protocols that Septentrio SBF receivers are capable of outputting.

The `psbf2` homepage is located at [https://github.com/semuconsulting/pysbf2](https://github.com/semuconsulting/pysbf2).

This is an independent project and we have no affiliation whatsoever with Septentrio.

## <a name="currentstatus">Current Status</a>

![Status](https://img.shields.io/pypi/status/pysbf2)
![Release](https://img.shields.io/github/v/release/semuconsulting/pysbf2?include_prereleases)
![Build](https://img.shields.io/github/actions/workflow/status/semuconsulting/pysbf2/main.yml?branch=main)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pysbf2)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pysbf2)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pysbf2)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pysbf2.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pysbf2)

The library implements a comprehensive set of messages for Septentrio Mosaic X5 devices, but is readily [extensible](#extensibility). Refer to `SBF_MSGIDS` in [sbftypes_core.py](https://github.com/semuconsulting/pysbf2/blob/main/src/pysbf2/sbftypes_core.py#L83) for the complete dictionary of messages currently supported. SBF protocol information sourced from mosaic-X5 Reference Guide v4.14.10.

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pysbf2/](https://www.semuconsulting.com/pysbf2/).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pysbf2/blob/master/CONTRIBUTING.md). Feel free to discuss any proposed changes beforehand in the [Discussion Channel](https://github.com/semuconsulting/pysbf2/discussions/categories/ideas).

[Bug reports](https://github.com/semuconsulting/pysbf2/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pysbf2/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided. For general queries and advice, post a message to one of the [pysbf2 Discussions](https://github.com/semuconsulting/pysbf2/discussions) channels.

---
## <a name="installation">Installation</a>

![Python version](https://img.shields.io/pypi/pyversions/pysbf2.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pysbf2.svg?style=flat)](https://pypi.org/project/pysbf2/)
![PyPI downloads](https://img.shields.io/pypi/dm/pysbf2.svg?style=flat)

`pysbf2` is compatible with Python 3.9 - 3.13. In the following, `python3` & `pip` refer to the Python 3 executables. You may need to substitute `python` for `python3`, depending on your particular environment (*on Windows it's generally `python`*).

The recommended way to install the latest version of `pysbf2` is with [pip](http://pypi.python.org/pypi/pip/):

```shell
python3 -m pip install --upgrade pysbf2
```

If required, `pysbf2` can also be installed into a virtual environment, e.g.:

```shell
python3 -m venv env
source env/bin/activate # (or env\Scripts\activate on Windows)
python3 -m pip install --upgrade pysbf2
```

For [Conda](https://docs.conda.io/en/latest/) users, `pysbf2` is also available from [conda forge](https://github.com/conda-forge/pysbf2-feedstock):

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pysbf2/badges/version.svg)](https://anaconda.org/conda-forge/pysbf2)
[![Anaconda-Server Badge](https://img.shields.io/conda/dn/conda-forge/pysbf2)](https://anaconda.org/conda-forge/pysbf2)

```shell
conda install -c conda-forge pysbf2
```

---
## <a name="reading">Reading (Streaming)</a>

```
class pysbf2.SBFreader.SBFReader(stream, *args, **kwargs)
```

You can create a `SBFReader` object by calling the constructor with an active stream object. 
The stream object can be any viable data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper). `pysbf2` implements an internal `SocketWrapper` class to allow sockets to be read in the same way as other streams (see example below).

Individual input SBF, NMEA or RTCM3 messages can then be read using the `SBFReader.read()` function, which returns both the raw binary data (as bytes) and the parsed data (as a `SBFMessage`, `NMEAMessage` or `RTCMMessage` object, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `SBFReader` also implements an iterator.

The constructor accepts the following optional keyword arguments:

* `protfilter`: `NMEA_PROTOCOL` (1), `SBF_PROTOCOL` (2), `RTCM3_PROTOCOL` (4). Can be OR'd; default is `NMEA_PROTOCOL | SBF_PROTOCOL | RTCM3_PROTOCOL` (7)
* `quitonerror`: `ERR_IGNORE` (0) = ignore errors, `ERR_LOG` (1) = log errors and continue (default), `ERR_RAISE` (2) = (re)raise errors and terminate
* `validate`: `VALCKSUM` (0x01) = validate checksum (default), `VALNONE` (0x00) = ignore invalid checksum or length

Example -  Serial input. This example will output both SBF and NMEA messages but not RTCM3:
```python
from serial import Serial
from pysbf2 import SBFReader, NMEA_PROTOCOL, SBF_PROTOCOL
with Serial('/dev/ttyACM0', 115200, timeout=3) as stream:
  ubr = SBFReader(stream, protfilter=NMEA_PROTOCOL | SBF_PROTOCOL)
  raw_data, parsed_data = ubr.read()
  if parsed_data is not None:
    print(parsed_data)
```

Example - File input (using iterator). This will only output SBF data:
```python
from pysbf2 import SBFReader, SBF_PROTOCOL
with open('SBFdata.bin', 'rb') as stream:
  ubr = SBFReader(stream, protfilter=SBF_PROTOCOL)
  for raw_data, parsed_data in ubr:
    print(parsed_data)
```

Example - Socket input (using iterator). This will output SBF, NMEA and RTCM3 data:
```python
import socket
from pysbf2 import SBFReader, NMEA_PROTOCOL, SBF_PROTOCOL, RTCM3_PROTOCOL
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("localhost", 50007))
  ubr = SBFReader(stream, protfilter=NMEA_PROTOCOL | SBF_PROTOCOL | RTCM3_PROTOCOL)
  for raw_data, parsed_data in ubr:
    print(parsed_data)
```

---
## <a name="parsing">Parsing</a>

You can parse individual SBF messages using the static `SBFReader.parse(data)` function, which takes a bytes array containing a binary SBF message and returns a `SBFMessage` object.

**NB:** Once instantiated, a `SBFMessage` object is immutable.

The `parse()` method accepts the following optional keyword arguments:

* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length

Example - output (GET) message:
```python
from pysbf2 import SBFReader
msg = SBFReader.parse(b"$@^b\xa6\x0f`\x00X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\x8f\x02\x8f\x02\r\t2P\x01\x00\x00\x00+\x00z\x00\x88\x00`\x01")
print(msg)
```
```
<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=122, VAccuracy=136, Misc=96)>
```

The `SBFMessage` object exposes different public attributes depending on its message type or 'identity',
e.g. the `PVTCartesian` message has the following attributes:

```python
print(msg)
print(msg.identity)
print(msg.X, msg.Y, msg.Z)
```
```
<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=655, MeanCorrAge=655, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=122, VAccuracy=136, Misc=96)>
PVTCartesian
3803640.1823747293, -148797.3625715144, 5100642.783697508
```

The `payload` attribute always contains the raw payload as bytes. Attributes within repeating groups are parsed with a two-digit suffix (PRNMaskNo_01, PRNMaskNo_02, etc.).

**Tip:** To iterate through a repeating group of attributes (*e.g. PRNMaskNo*), the following construct can be used:

```python
vals = [] # list of PRNMaskNo values from repeating group
for i in range(msg.N): # N = size of repeating group
    PRNMaskNo = getattr(msg, f"PRNMaskNo_{i+1:02d}")
    vals.append(PRNMaskNo)
print(vals)
```

---
## <a name="generating">Generating</a>

```
class pysbf2.SBFmessage.SBFMessage(SBFClass, msgid: int, revno: int, **kwargs)
```

You can create a `SBFMessage` object by calling the constructor with the following parameters:
1. message id
2. revision number (optional, defaults to 0)
3. (optional) a series of keyword parameters representing the message payload

The 'message class' and 'message id' parameters may be passed as lookup strings, integers or bytes.

The message payload can be defined via keyword arguments in one of three ways:
1. A single keyword argument of `payload` containing the full payload as a sequence of bytes (any other keyword arguments will be ignored). **NB** the `payload` keyword argument *must* be used for message types which have a 'variable by size' repeating group.
2. One or more keyword arguments corresponding to individual message attributes. Any attributes not explicitly provided as keyword arguments will be set to a nominal value according to their type.
3. If no keyword arguments are passed, the payload is assumed to be null.

Example - to generate a CFG-MSG command (*msgClass 0x06, msgID 0x01*) which sets the NAV-STATUS (*msgClass 0x01, msgID 0x03*) outbound message rate to 1 on the UART1 port, any of the following constructor formats will work:

A. Pass entire payload as bytes:
```python
from pysbf2 import SBFMessage
msg1 = SBFMessage("PVTCartesian", payload=b'X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\xa6\xddABQ\x90\x018\xb4\x86q:\xc0\x93\x85\xbb\xf9\x02\x95\xd0\xe3\xaf\xe6nKl\xde?\x03\xe0V>\x00\x00\x10\x00\xff\xff\xff\xff\r\t2P\x01\x00\x00\x00+\x00\xc4\x04V\x05`')
print(msg1)
```
```
<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=65535, MeanCorrAge=65535, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=1220, VAccuracy=1366, Misc=96)>
```
B. Pass individual attributes as keyword arguments:
```python
from pysbf2 import SBFMessage
msg2 = SBFMessage("PVTCartesian",TOW=208903000,WNc=2367,Mode=1,Error=0,X=3803640.1823747293,Y=-148797.3625715144,Z=5100642.783697508,Undulation=48.466453552246094,Vx=3.0890401831129566e-05,Vy=0.000921349273994565,Vz=-0.004076451063156128,COG=-20000000000.0,RxClkBias=0.47535978155315045,RxClkDrift=0.20983891189098358,TimeSystem=0,Datum=0,NrSV=16,WACorrInfo=0,ReferenceID=65535,MeanCorrAge=65535,SignalInfo=1345456397,AlertFlag=1,NrBases=0,PPPInfo=0,Latency=43,HAccuracy=1220,VAccuracy=1366,Misc=96)
print(msg2)
```
```
<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=48.466453552246094, Vx=3.0890401831129566e-05, Vy=0.000921349273994565, Vz=-0.004076451063156128, COG=-20000000000.0, RxClkBias=0.47535978155315045, RxClkDrift=0.20983891189098358, TimeSystem=0, Datum=0, NrSV=16, WACorrInfo=0, ReferenceID=65535, MeanCorrAge=65535, SignalInfo=1345456397, AlertFlag=1, NrBases=0, PPPInfo=0, Latency=43, HAccuracy=1220, VAccuracy=1366, Misc=96)>
```
C. Pass selected attribute as keyword argument; the rest will be set to nominal values (in this case 0):
```python
from pysbf2 import SBFMessage
msg3 = SBFMessage("PVTCartesian",TOW=208903000,WNc=2367,Mode=1,Error=0,X=3803640.1823747293,Y=-148797.3625715144,Z=5100642.783697508)
print(msg3)
```
```
<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=0.0, Vx=0.0, Vy=0.0, Vz=0.0, COG=0.0, RxClkBias=0.0, RxClkDrift=0.0, TimeSystem=0, Datum=0, NrSV=0, WACorrInfo=0, ReferenceID=0, MeanCorrAge=0, SignalInfo=0, AlertFlag=0, NrBases=0, PPPInfo=0, Latency=0, HAccuracy=0, VAccuracy=0, Misc=0)>
```

---
## <a name="serializing">Serializing</a>

The `SBFMessage` class implements a `serialize()` method to convert a `SBFMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `CFG-MSG` command which sets the NMEA GLL (*msgClass 0xf0, msgID 0x01*) message rate to 1 on the receiver's UART1 and USB ports:

```python
from serial import Serial
from pysbf2 import SBFMessage
serialOut = Serial('/dev/ttyAMA0', 115200, timeout=3)
from pysbf2 import SBFMessage
msg = SBFMessage("PVTCartesian",TOW=208903000,WNc=2367,Mode=1,Error=0,X=3803640.1823747293,Y=-148797.3625715144,Z=5100642.783697508)
print(msg)
output = msg.serialize()
print(output)
serialOut.write(output)
```
```
<SBF(PVTCartesian, TOW=10:01:25, WNc=2367, Mode=1, Error=0, X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508, Undulation=0.0, Vx=0.0, Vy=0.0, Vz=0.0, COG=0.0, RxClkBias=0.0, RxClkDrift=0.0, TimeSystem=0, Datum=0, NrSV=0, WACorrInfo=0, ReferenceID=0, MeanCorrAge=0, SignalInfo=0, AlertFlag=0, NrBases=0, PPPInfo=0, Latency=0, HAccuracy=0, VAccuracy=0, Misc=0)>
b'$@\x81u\xa6\x0f`\x00X\x9bs\x0c?\t\x01\x00\x1d\x0eX\x17\xfc\x04MA\xe6\xe4\x8b\xe6\xea)\x02\xc1\x98\x19(\xb2\x18uSA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
```

---
## <a name="examples">Examples</a>

The following command line examples can be found in the `\examples` folder:

1. TBC

---
## <a name="extensibility">Extensibility</a>

The SBF protocol is principally defined in the modules `sbftypes_*.py` as a series of dictionaries. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. attribute types must be one of the valid types (I1, U2, X4, etc.)
3. if the attribute is scaled, attribute type is list of [attribute type as string (I1, U2, etc.), scaling factor as float] e.g. {"lat": [I4, 1e-7]}
4. repeating or bitfield groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'numCh'
     c. an 'X' attribute type ('X1', 'X2', 'X4', etc) representing a group of individual bit flags
   {dict} is the nested dictionary of repeating items or bitfield group
```

Repeating attribute names are parsed with a two-digit suffix (PRNMaskNo_01, PRNMaskNo_02, etc.). Nested repeating groups are supported. See "MeasEpoch" way of example.

An SBF message's content (payload) is uniquely defined by its ID (message ID and revision number); accommodating the message simply requires the addition of an appropriate dictionary entry to the `sbftypes_blocks.py` module.

---
## <a name="knownissues">Known Issues</a>

1. The following SBF message types are not yet implemented (mainly because definitions are not currently in the public domain or are unresolved):
    1. Meas3CN0HiRes
    1. Meas3Doppler
    1. Meas3MP
    1. Meas3PP
    1. Meas3Ranges
    1. PVTSupport
    1. PVTSupportA
    1. FugroDDS

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![GitHub License](https://img.shields.io/github/license/semuconsulting/pysbf2)

`pysbf2` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the utility useful, please consider sponsoring the project with the price of a coffee...

[![Sponsor](https://github.com/semuconsulting/pyubx2/blob/master/images/sponsor.png?raw=true)](https://buymeacoffee.com/semuconsulting)

[![Freedom for Ukraine](https://github.com/semuadmin/sandpit/blob/main/src/sandpit/resources/ukraine200.jpg?raw=true)](https://u24.gov.ua/)
