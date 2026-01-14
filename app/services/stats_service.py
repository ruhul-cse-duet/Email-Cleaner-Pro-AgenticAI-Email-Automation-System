from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable


class StatsService:
    def __init__(self, log_dir: Path | None = None) -> None:
        self._log_dir = log_dir or (Path(__file__).resolve().parents[2] / "logs")

        self._processed_patterns = [
            re.compile(r"Processing email:\s", re.IGNORECASE),
            re.compile(r"\bProcessing:\s", re.IGNORECASE),
        ]
        self._auto_reply_patterns = [
            re.compile(r"Sent auto-reply for:\s", re.IGNORECASE),
            re.compile(r"Sent auto-reply to:\s", re.IGNORECASE),
        ]
        self._tagged_patterns = [
            re.compile(r"Tagged email with:\s", re.IGNORECASE),
            re.compile(r"Tagged with:\s", re.IGNORECASE),
        ]
        self._escalation_patterns = [
            re.compile(r"Escalated email:\s", re.IGNORECASE),
            re.compile(r"Escalated to human", re.IGNORECASE),
        ]

    def get_stats(self) -> dict:
        stats = {
            "processed": 0,
            "auto_replies": 0,
            "tagged": 0,
            "escalations": 0,
        }

        for log_file in self._iter_log_files():
            self._accumulate_from_file(log_file, stats)

        return stats

    def _iter_log_files(self) -> Iterable[Path]:
        if not self._log_dir.exists():
            return []

        files = [
            path
            for path in self._log_dir.glob("email_cleaner.log*")
            if path.is_file()
        ]
        return sorted(files)

    def _accumulate_from_file(self, log_file: Path, stats: dict) -> None:
        try:
            with log_file.open("r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    if self._matches_any(line, self._processed_patterns):
                        stats["processed"] += 1
                        continue
                    if self._matches_any(line, self._auto_reply_patterns):
                        stats["auto_replies"] += 1
                        continue
                    if self._matches_any(line, self._tagged_patterns):
                        stats["tagged"] += 1
                        continue
                    if self._matches_any(line, self._escalation_patterns):
                        stats["escalations"] += 1
        except OSError:
            return

    @staticmethod
    def _matches_any(line: str, patterns: list[re.Pattern[str]]) -> bool:
        return any(pattern.search(line) for pattern in patterns)
