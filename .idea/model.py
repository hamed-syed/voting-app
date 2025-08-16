"""Data model & persistence for votes."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, Set, Tuple
import csv
import os
from .exceptions import PersistenceError, ValidationError

@dataclass
class VoteStore:
    """Stores vote totals and who has voted, persisted to CSV files."""
    votes_filepath: str
    ledger_filepath: str
    allowed_candidates: Set[str]
    _totals: Dict[str, int] = field(default_factory=dict)
    _voted_ids: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        # initialize totals
        for name in self.allowed_candidates:
            self._totals.setdefault(name, 0)
        self._load_files()

    def _load_files(self) -> None:
        # Load totals from votes file (aggregated) and ledger of IDs
        try:
            if os.path.exists(self.votes_filepath):
                with open(self.votes_filepath, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cand = row.get("candidate", "")
                        if cand in self._totals:
                            self._totals[cand] += 1
            if os.path.exists(self.ledger_filepath):
                with open(self.ledger_filepath, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        vid = row.get("id", "").strip()
                        if vid:
                            self._voted_ids.add(vid)
        except OSError as e:
            raise PersistenceError(f"Could not load data files: {e}") from e

    # Public API
    def has_voted(self, voter_id: str) -> bool:
        return voter_id in self._voted_ids

    def save_vote(self, voter_id: str, candidate: str) -> None:
        """Append a new vote and update totals. Raises on errors/invalids."""
        if candidate not in self.allowed_candidates:
            raise ValidationError(f"Unknown candidate: {candidate}")
        if self.has_voted(voter_id):
            raise ValidationError("This ID has already voted.")

        # Append to votes file and to ledger
        try:
            new_votes = not os.path.exists(self.votes_filepath)
            with open(self.votes_filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["candidate"])
                if new_votes:
                    writer.writeheader()
                writer.writerow({"candidate": candidate})
            new_ledger = not os.path.exists(self.ledger_filepath)
            with open(self.ledger_filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "candidate"])
                if new_ledger:
                    writer.writeheader()
                writer.writerow({"id": voter_id, "candidate": candidate})
            self._totals[candidate] += 1
            self._voted_ids.add(voter_id)
        except OSError as e:
            raise PersistenceError(f"Could not write data files: {e}") from e

    def totals(self) -> Dict[str, int]:
        """Return a copy of current totals."""
        return dict(self._totals)

    def reset_all(self) -> None:
        """Clear all persisted data and memory (dev/testing helper)."""
        self._totals = {name:0 for name in self.allowed_candidates}
        self._voted_ids.clear()
        for path in (self.votes_filepath, self.ledger_filepath):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError as e:
                raise PersistenceError(f"Could not reset file {path}: {e}") from e
