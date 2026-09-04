from __future__ import annotations

from collections.abc import Iterator

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.encoders.base import EncoderAdapter


class EncoderRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, EncoderAdapter] = {}

    def register(self, adapter: EncoderAdapter) -> None:
        adapter_id = adapter.descriptor.id
        if adapter_id in self._adapters:
            raise ValidationError(f"Encoder adapter {adapter_id!r} is already registered")
        self._adapters[adapter_id] = adapter

    def get(self, adapter_id: str) -> EncoderAdapter:
        try:
            return self._adapters[adapter_id]
        except KeyError as exc:
            raise ValidationError(f"Unknown encoder adapter: {adapter_id}") from exc

    def __iter__(self) -> Iterator[EncoderAdapter]:
        return iter(self._adapters.values())

    def __len__(self) -> int:
        return len(self._adapters)
