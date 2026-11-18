"""Microphone and speaker helpers.

Lesson 1: audio is just a list of numbers (samples). 16,000 samples per
second is enough for speech and is what Sarvam's speech-to-text expects.
"""
import io
import queue

import numpy as np
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16_000


def record_until_enter() -> bytes:
    """Record from the default mic until the user presses Enter.

    Returns WAV bytes, ready to upload. On the robot, a big physical button
    will replace the Enter key.
    """
    chunks: queue.Queue = queue.Queue()

    def on_audio(indata, frames, time, status):
        chunks.put(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=on_audio):
        input("  Listening... press Enter when you finish speaking.")

    samples = np.concatenate(list(chunks.queue)) if not chunks.empty() else np.zeros((0, 1), dtype="int16")
    buffer = io.BytesIO()
    sf.write(buffer, samples, SAMPLE_RATE, format="WAV", subtype="PCM_16")
    return buffer.getvalue()


def play_wav(wav_bytes: bytes) -> None:
    """Play WAV bytes through the default speaker and wait until done."""
    data, rate = sf.read(io.BytesIO(wav_bytes), dtype="float32")
    sd.play(data, rate)
    sd.wait()
