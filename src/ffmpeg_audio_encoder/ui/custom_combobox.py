from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QCompleter, QWidget


class AutoCompleteComboBox(QComboBox):
    """Editable QComboBox with type-ahead filtering, adapted from NFOForge.

    A plain QComboBox's popup gets unwieldy once it holds dozens of entries -
    the "Time modification" preset list alone mixes 56 framerate-conversion
    pairs with 11 speed presets. This subclass makes the combo editable and
    wires a QCompleter over its own item list, so typing "24" narrows the
    popup to matching presets instead of scrolling through all of them.

    Typed text that doesn't match a real item is not kept: leaving the field
    reverts to the first entry, so `currentData()` always reflects a real
    choice rather than free text callers would otherwise have to validate.
    """

    def __init__(self, max_visible_items: int = 15, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setMaxVisibleItems(max_visible_items)

        line_edit = self.lineEdit()
        if line_edit is None:
            raise RuntimeError("An editable QComboBox always provides a line edit")
        line_edit.editingFinished.connect(self._revert_unmatched_text)

        completer = self.completer()
        if completer is None:
            raise RuntimeError("An editable QComboBox always provides a completer")
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        # Contains rather than the default starts-with: preset labels like
        # "23.976 -> 24 (1.001x)" are found by typing "24" as readily as "23".
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def _revert_unmatched_text(self) -> None:
        if self.currentText() not in (self.itemText(i) for i in range(self.count())):
            self.setCurrentIndex(0)
