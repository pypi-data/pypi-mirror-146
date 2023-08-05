from io import RawIOBase
from struct import pack
import wave

from .mp3reader import Mp3Reader


def decode(src: RawIOBase, dst):
    """
    Read MP3 from src and output PCM to dst.
    """
    with (
        Mp3Reader.open(src) as mp3,
        wave.open(dst, "wb") as wav,
    ):
        header = mp3.header()

        wav.setnchannels(header.stereo)
        wav.setsampwidth(2)
        wav.setframerate(header.samplerate)

        if header.stereo == 2:
            for (pcm_l, pcm_r) in mp3.all_frames():
                for (l, r) in zip(pcm_l, pcm_r):
                    wav.writeframes(pack("<h", l))
                    wav.writeframes(pack("<h", r))
        else:
            for (pcm_l, pcm_r) in mp3.all_frames():
                wav.writeframes(pack(f"<{len(pcm_l)}h", *pcm_l))
