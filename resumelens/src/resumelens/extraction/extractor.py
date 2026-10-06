from __future__ import annotations

import json
from typing import Any

from resumelens.extraction.patterns import extract_candidate_evidence


class ResumeExtractor:
    """Public extraction wrapper used by the pipeline and tests."""

    def __init__(self, text: str):
        self.text = text

    def extract(self) -> dict[str, list[str]]:
        """Run the extraction stage and return a structured evidence dictionary."""

        return extract_candidate_evidence(self.text)

    def to_json(self) -> str:
        """Serialize extracted candidates as JSON for debugging and export."""

        data = self.extract()
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def extract_from_text(text: str) -> dict[str, list[str]]:
        """Convenience method for one-off extraction calls."""

        return ResumeExtractor(text).extract()


def extract_resume(text: str) -> dict[str, list[str]]:
    """Simple module-level helper for the pipeline."""

    return ResumeExtractor(text).extract()
