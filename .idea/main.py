"""App entrypoint for the Voting App."""
from __future__ import annotations
import sys, os
from PyQt6.QtWidgets import QApplication
from .controller import Controller
from .model import VoteStore
from .view import MainWindow

def main() -> None:
    # Ensure data directory exists relative to project root
    base = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    ui_path = os.path.join(base, "ui", "main_window.ui")

    app = QApplication(sys.argv)
    model = VoteStore(
        votes_filepath=os.path.join(data_dir, "votes.csv"),
        ledger_filepath=os.path.join(data_dir, "ledger.csv"),
        allowed_candidates={"jane", "john"},  # <-- lowercase to match your radios
    )
    view = MainWindow(ui_path=ui_path)
    Controller(model, view)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
