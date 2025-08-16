"""Qt view loader that matches your UI names exactly."""
from __future__ import annotations
from typing import Dict
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi

class MainWindow(QMainWindow):
    """Loads the .ui and provides helpers used by the controller."""
    def __init__(self, ui_path: str) -> None:
        super().__init__()
        loadUi(ui_path, self)  # widgets from the UI become attributes

    def show_info(self, msg: str) -> None:
        # Your label is named statuslabel (all lowercase)
        self.statuslabel.setStyleSheet("color: #1b5e20;")  # green-ish
        self.statuslabel.setText(msg)

    def show_error(self, msg: str) -> None:
        self.statuslabel.setStyleSheet("color: #b00020;")  # red-ish
        self.statuslabel.setText(msg)

    def popup_error(self, title: str, msg: str) -> None:
        QMessageBox.critical(self, title, msg)

    def populate_totals(self, totals: Dict[str, int]) -> None:
        # Your table is named totalstable (all lowercase)
        self.totalstable.setRowCount(len(totals))
        self.totalstable.setColumnCount(2)
        self.totalstable.setHorizontalHeaderLabels(["Candidate", "Votes"])
        for r, (name, count) in enumerate(sorted(totals.items())):
            self.totalstable.setItem(r, 0, QTableWidgetItem(name))
            self.totalstable.setItem(r, 1, QTableWidgetItem(str(count)))
        self.totalstable.resizeColumnsToContents()
