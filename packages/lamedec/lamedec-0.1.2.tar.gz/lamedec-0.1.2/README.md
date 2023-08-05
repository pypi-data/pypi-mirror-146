# LAME MP3 decoding wrapper

## Usage

```python
lamedec.decode(src, dst)
```

### Parameters

_src_ Instance of io.RawIOBase (eg. FileIO, ByteIO ...).

_dst_ Same parameter for wave module.

## Sample

```python
import io
import lamedec


src = io.FileIO("src.mp3", "rb")
dst = "dst.wav"

lamedec.decode(src, dst)
```

See [samples](https://github.com/sengokyu/python-lamedec/blob/main/samples).
