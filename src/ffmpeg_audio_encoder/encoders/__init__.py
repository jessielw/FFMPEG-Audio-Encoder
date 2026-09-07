"""First-party encoder adapters."""

from ffmpeg_audio_encoder.encoders.deezy import (
    DeezyAc4Encoder,
    DeezyAtmosEncoder,
    DeezyDdEncoder,
    DeezyDdpBlurayEncoder,
    DeezyDdpEncoder,
)
from ffmpeg_audio_encoder.encoders.external import FdkAacEncoder, OpusencEncoder, QaacEncoder
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
    """Register adapters family by family; the encoder picker keeps this order."""
    registry = EncoderRegistry()
    registry.register(OpusEncoder())
    registry.register(FlacEncoder())
    registry.register(AacEncoder())
    registry.register(Mp3Encoder())
    registry.register(Ac3Encoder())
    registry.register(Eac3Encoder())
    registry.register(DtsEncoder())
    registry.register(AlacEncoder())
    registry.register(OpusencEncoder())
    registry.register(QaacEncoder())
    registry.register(FdkAacEncoder())
    registry.register(DeezyDdEncoder())
    registry.register(DeezyDdpEncoder())
    registry.register(DeezyDdpBlurayEncoder())
    registry.register(DeezyAtmosEncoder())
    registry.register(DeezyAc4Encoder())
    return registry


__all__ = [
    "AacEncoder",
    "Ac3Encoder",
    "AlacEncoder",
    "DeezyAc4Encoder",
    "DeezyAtmosEncoder",
    "DeezyDdEncoder",
    "DeezyDdpBlurayEncoder",
    "DeezyDdpEncoder",
    "DtsEncoder",
    "Eac3Encoder",
    "EncoderRegistry",
    "FdkAacEncoder",
    "FlacEncoder",
    "Mp3Encoder",
    "OpusEncoder",
    "OpusencEncoder",
    "QaacEncoder",
    "default_registry",
]
