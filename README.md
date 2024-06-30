# audiochains

It is a python package for simultaneous recording and processing audio data on the fly in a stream.

## Motivation

Many similar libraries provide definitely useful and convenient tools for audio recording or processing raw data for the sake of feature extraction, but if you want to implement audio processing during recording, you will face to the need to write your own functions linking these two processes. This is fraught with numerous errors related to the mismatch of input and output data types and code bloat.

This project attempts to avoid these problems by giving the functions of simultaneous audio recording and processing.

`sounddevice` was chosen as the kernel library for audio processing, which is a wrapper for PortAudio cross-platform library.

## **Usage example**

For instance, look at the code snippet below.

```python
from audiochains.streams import InputStream
from audiochains.block_methods import RMSFromBytes

with InputStream(
	samplerate=16000,
	blocksize=1024,
	channels=1,
	sampwidth=2
) as stream:
	stream.set_methods(RMSFromBytes(width=2))
	for _ in range(stream.get_iterations(seconds=10)):
			print("#" * stream.apply())
```

This code opens an audio stream for recording 10 seconds and each constant moment of time it calculates RMS of the given data chunk and prints its.

All this is done by the `InputStream` object, which opens the stream for recording audio, and then creates a special chain of data processing methods (`set_methods()`).  You may call it a pipeline.

## Main entities

### Streams

`StreamWithChain` — an interface which defines for `sounddevice` stream objects. This class should store the `ChainOfMethods` instance and define applying this chain to raw input data

`InputStream` — an overridden `sd.RawInputStream` class as a `StreamWithChain` interface implementation

`IOStream` — an overridden `sd.RawStream` class as a `StreamWithChain` interface implementation

### Block methods

`BlockAudioMethods` — an abstract interface defining the functionality of audio processing unit.  The are so called because they are processing blocks of raw audio data (or chunks).

Each algorithm of audio processing should be implemented as inheritance from this interface with implementation of _ _ call _ _ magic method.

### ChainOfMethods

`ChainOfMethods`— it is an implementation of Chain Of Command pattern for sequences of `BlockAudioMethod.` In other way it can be called as a pipeline which automate the process of sequential execution of algorithms 

### Devices

`AudioDevices` — a special class combining functions for getting advanced information about the input or output device separately. For example:

- `get_all_input_devices()` — returns the list containing all input devices indices by checking an amount of input channels
- `get_all_output_devices()` — returns the list containing all output devices indices by checking an amount of output channels
- `get_hostapi_with_devices(self, kind: str = None)` — returns a dictionary where key is a name of audio system host api and corresponded value is dictionary containing information about all compatible devices

## Future plans

- [ ] upload project to PyPi
- [ ] add implementation of OutputStream
- [ ] implement audio recording with blocks overlapping
- [ ] expand the set of block methods
- [ ] distinguish blocks_methods by their purpose
    - unpacking
    - resampling
    - feature extraction
    - augmentation, filtering, windows function, etc.
- [ ] add support for two-channel audio processing
