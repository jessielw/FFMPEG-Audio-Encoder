from __future__ import annotations

from PySide6.QtWidgets import QDoubleSpinBox


class TrimmedDoubleSpinBox(QDoubleSpinBox):
    """QDoubleSpinBox that hides padded trailing zeros without losing precision.

    A plain QDoubleSpinBox with decimals=3 always pads its display, so a value of
    2480 renders as "2480.000". This subclass keeps the full decimal precision for
    storage/typing/parsing, but trims trailing zeros (and a bare trailing decimal
    point) from the displayed text, so "2480" shows as "2480" while a genuinely
    fractional value like "21.333" is left untouched.
    """

    def textFromValue(self, value: float) -> str:
        text = super().textFromValue(value)
        decimal_point = self.locale().decimalPoint()
        if decimal_point not in text:
            return text
        integer_part, _, fractional_part = text.partition(decimal_point)
        trimmed_fraction = fractional_part.rstrip("0")
        if not trimmed_fraction:
            return integer_part
        return f"{integer_part}{decimal_point}{trimmed_fraction}"
