# audiochains
A library including sounddevice audio streams with the ability to process raw data in chains of processing methods.

## Installation
```shell
pip install audiochains
```

## Example of using

For instance, it is needed to get an RMS of input audio signal amplitude value. 
```python
from audiochains.streams import InputStreamWithChain
from audiochains.block_methods import RMSFromBytes

with InputStreamWithChain(
        samplerate=16000,
        blocksize=1024,
        channels=1,
        sampwidth=2) as stream:
    stream.set_methods(
        RMSFromBytes()
    )
    for _ in range(stream.get_iterations(seconds=10)):
        stream.read(stream.blocksize)
```