"""Controller wired to your exact UI object names."""
from __future__ import annotations

from PyQt6.QtCore import QObject

from .model import VoteStore
from .view import MainWindow
from .validators import require_digits
from .exceptions import ValidationError, PersistenceError


class Controller(QObject):
    """Connects UI signals to model methods and updates the view."""
    def __init__(self, model: VoteStore, view: MainWindow) -> None:
        super().__init__(view)
        self.model = model
        self.view = view

        # Your .ui names are:
        #   Submitbutton, resetbutton, IDinput, rbjane, rbjohn, statuslabel, totalstable

        # Fix the line edit initial state (your UI put text "ID" in it)
        try:
            self.view.IDinput.clear()
        except Exception:
            pass
        self.view.IDinput.setPlaceholderText("4-digit ID")

        # Wire signals
        self.view.Submitbutton.clicked.connect(self.on_submit)
        self.view.resetbutton.clicked.connect(self.on_reset_click)
        self.view.IDinput.textChanged.connect(self._maybe_toggle_submit)
        self.view.rbjane.clicked.connect(self._maybe_toggle_submit)
        self.view.rbjohn.clicked.connect(self._maybe_toggle_submit)

        # Initial state
        self.view.Submitbutton.setEnabled(False)
        self._refresh_totals()
        self.view.statuslabel.setText("")

    def _selected_candidate(self) -> str | None:
        if self.view.rbjane.isChecked():
            return "jane"
        if self.view.rbjohn.isChecked():
            return "john"
        return None

    def _maybe_toggle_submit(self) -> None:
        voter_id = self.view.IDinput.text().strip()
        cand = self._selected_candidate()
        ok_len = voter_id.isdigit() and len(voter_id) == 4
        self.view.Submitbutton.setEnabled(bool(cand) and ok_len)

    def _refresh_totals(self) -> None:
        self.view.populate_totals(self.model.totals())

    def on_submit(self) -> None:
        try:
            voter_id = require_digits(self.view.IDinput.text(), 4, "ID")
            cand = self._selected_candidate()
            if not cand:
                raise ValidationError("Please select a candidate.")
            self.model.save_vote(voter_id, cand)
            self.view.show_info("Vote recorded successfully!")
            self._refresh_totals()
            self.view.IDinput.clear()
        except (ValidationError, PersistenceError) as e:
            self.view.show_error(str(e))
            if isinstance(e, PersistenceError):
                self.view.popup_error("Storage Error", str(e))

    def on_reset_click(self) -> None:
        try:
            self.model.reset_all()
            self.view.show_info("All votes cleared.")
            self._refresh_totals()
        except PersistenceError as e:
            self.view.popup_error("Reset Error", str(e))
