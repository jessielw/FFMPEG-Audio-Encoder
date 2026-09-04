"""Application-specific errors that can be shown safely to users."""


class AudioEncoderError(Exception):
    """Base class for expected application failures."""


class ValidationError(AudioEncoderError):
    """Raised when a request or encoder option is invalid."""


class ProbeError(AudioEncoderError):
    """Raised when media probing fails or returns unusable data."""


class ToolNotFoundError(AudioEncoderError):
    """Raised when a required executable cannot be found."""
