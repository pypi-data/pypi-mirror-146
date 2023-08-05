# hawksoft.serialPortComm package

- [hawksoft.serialPortComm package](#hawksoftserialportcomm-package)
  - [Installation:](#installation)
  - [usage:](#usage)

Provides a thread which send and receive bytes from serial port. The main thread can communicate with thread by  send and receive fucntion.



## Installation:

```
pip install hawksoft.serialPortComm
```

## usage:

```
from hawksoft import comm
comm.start('COM1',9600)
...
frames = comm.receive()
for abyte in frames:
    ...deal with abute
...
comm.send(b'\x01\x02')
...
comm.close()
```