from io import RawIOBase
from lame_ctypes import *
from ctypes import *

_READING_BUF_SIZE = 1024
_DECODING_BUF_SIZE = 2304


class Mp3ReaderError(RuntimeError):
    pass


class Mp3Reader:
    @staticmethod
    def open(src: RawIOBase) -> 'Mp3Reader':
        this = Mp3Reader()
        this.src = src
        this._close()
        this.hip = hip_decode_init()
        this.mp3data = None
        return this

    def header(self) -> mp3data_struct:
        """ Return MP3 header """
        pcm_buf_l = (c_short * _DECODING_BUF_SIZE)()
        pcm_buf_r = (c_short * _DECODING_BUF_SIZE)()
        mp3data = mp3data_struct()

        while True:
            (buf_len, buf) = self._read()

            if buf_len == 0:  # EOF
                raise Mp3ReaderError("Mp3 header not found.")

            nout = hip_decode1_headers(
                self.hip, buf, buf_len, pcm_buf_l, pcm_buf_r, byref(mp3data)
            )

            if nout == -1:
                raise Mp3ReaderError("Hip inside error.")

            if mp3data.header_parsed == 1:
                self.mp3data = mp3data
                return mp3data

    def all_frames(self):
        """ Return PCM data generator """

        if self.mp3data is None:
            raise Mp3ReaderError("Call header() method first.")

        # at first, see remain data in buffer
        while True:
            pcm_buf_l = (c_short * _DECODING_BUF_SIZE)()
            pcm_buf_r = (c_short * _DECODING_BUF_SIZE)()

            nout = hip_decode1_headers(
                self.hip, c_ubyte(), 0, pcm_buf_l, pcm_buf_r, self.mp3data)

            match(nout):
                case(-1):
                    raise Mp3ReaderError()
                case(0):
                    break
                case _:
                    yield (pcm_buf_l[:nout], pcm_buf_r[:nout])

        while True:
            (buf_len, buf) = self._read()

            if buf_len == 0:  # EOF
                break

            while True:
                pcm_buf_l = (c_short * _DECODING_BUF_SIZE)()
                pcm_buf_r = (c_short * _DECODING_BUF_SIZE)()

                nout = hip_decode1_headers(
                    self.hip, buf, buf_len, pcm_buf_l, pcm_buf_r, self.mp3data)

                match(nout):
                    case(-1):
                        raise Mp3ReaderError()
                    case(0) if buf_len > 0:
                        buf_len = 0
                        continue
                    case(0):
                        # need more data
                        break
                    case _:
                        buf_len = 0
                        yield (pcm_buf_l[:nout], pcm_buf_r[:nout])

    def _read(self):
        buf = self.src.read(_READING_BUF_SIZE)
        buf_len = len(buf)
        return (buf_len, (c_ubyte * buf_len).from_buffer(bytearray(buf)))

    def _close(self) -> None:
        if hasattr(self, "hip") and self.hip is not None:
            hip_decode_exit(self.hip)
            self.hip = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._close
