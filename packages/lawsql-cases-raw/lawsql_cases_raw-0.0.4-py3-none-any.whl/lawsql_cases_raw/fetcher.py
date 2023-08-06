from typing import Optional

from .config import MatchedRows


def row_data_from_pk(text: str) -> Optional[dict]:
    from .config import DECISIONS

    try:
        return next(DECISIONS.rows_where(f"pk=?", (text,)))
    except StopIteration:
        ...
    return None


def matched_rows(text: str) -> Optional[MatchedRows]:
    """Get results from the database that matching the `scra`, `phil`, `idx`, `cat`, `date_prom` fields depending on the text inputted and the matches generated from the same.

    Args:
        text (str): Citation either in report format: "1 SCRA 13", "4 Phil. 123", "GR. 1241"

    Returns:
        Optional[MatchedRows]: Namedtuple of rows, the `.counts` property determines the number of rows matched; the `.rows` property is a generator of dicts
    """
    from .dockets import rows_fom_docket_text
    from .reports import rows_from_report_text

    return rows_from_report_text(text) or rows_fom_docket_text(text)


def get_unique_row(text: str) -> Optional[dict]:
    """In case the text inputted matches a docket format and this docket format does not contain a date, duplicate rows will be returned.

    Args:
        text (str): Citation string that will be used in `matched_rows`

    Returns:
        Optional[dict]: Filtered unique row returned
    """
    return next(m.rows) if (m := matched_rows(text)) and (m.counts == 1) else None


def get_unique_row_content(text: str) -> Optional[dict]:
    """Will join content from folder to the row dictionary based on the row `loc` and `parent` keys, the row being generated from `get_unique_row`

    Args:
        text (str): Citation string that will be used in `matched_rows`, filtered by `get_unique_row`

    Returns:
        Optional[dict]: If a unique row is detected, the unique row is combined with the data sourced from the content folder of that row
    """
    from .organizer import add_content

    return add_content(row) if (row := get_unique_row(text)) else None
