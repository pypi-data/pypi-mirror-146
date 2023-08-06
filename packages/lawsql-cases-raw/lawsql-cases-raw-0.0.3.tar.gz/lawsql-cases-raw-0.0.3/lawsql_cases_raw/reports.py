from typing import Optional

from .config import DECISIONS, MatchedRows


def match_report(pattern: str, text: str) -> Optional[MatchedRows]:
    from citation_report.__main__ import get_report_formats

    try:
        result = next(get_report_formats(text))
        if pattern in result.lower():
            counts = DECISIONS.count_where(f"{pattern} = ?", (result,))
            rows = DECISIONS.rows_where(f"{pattern} = ?", (result,))
            return MatchedRows(counts=counts, rows=rows)
    except:
        ...
    return None


def rows_from_report_text(text: str) -> Optional[MatchedRows]:
    return match_report("phil", text) or match_report("scra", text)
