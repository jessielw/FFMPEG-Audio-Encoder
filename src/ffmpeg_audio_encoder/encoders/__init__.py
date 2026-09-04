"""First-party encoder adapters."""

from ffmpeg_audio_encoder.encoders.ffmpeg import (
    AacEncoder,
    Ac3Encoder,
    AlacEncoder,
    DtsEncoder,
    Eac3Encoder,
    FlacEncoder,
    Mp3Encoder,
    OpusEncoder,
)
from ffmpeg_audio_encoder.encoders.registry import EncoderRegistry


def default_registry() -> EncoderRegistry:
    registry = EncoderRegistry()
    registry.register(OpusEncoder())
    registry.register(FlacEncoder())
    registry.register(AacEncoder())
    registry.register(Mp3Encoder())
    registry.register(Ac3Encoder())
    registry.register(Eac3Encoder())
    registry.register(DtsEncoder())
    registry.register(AlacEncoder())
    return registry


__all__ = [
    "AacEncoder",
    "Ac3Encoder",
    "AlacEncoder",
    "DtsEncoder",
    "Eac3Encoder",
    "EncoderRegistry",
    "FlacEncoder",
    "Mp3Encoder",
    "OpusEncoder",
    "default_registry",
]
