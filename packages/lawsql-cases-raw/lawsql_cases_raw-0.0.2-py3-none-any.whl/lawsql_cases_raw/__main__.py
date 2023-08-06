from pathlib import Path
from typing import Iterator


def init_db():
    from sqlite_utils.db import Table

    from .config import DB, DECISIONS, JUSTICES, VOTING_LINES
    from .raw_sql import duplicate_elements_of_dockets, duplicate_phil_reports

    for i in [JUSTICES, DECISIONS, VOTING_LINES]:
        if not isinstance(i, Table):
            raise Exception("Missing table.")
    DB.create_view("duplicate_phils", duplicate_phil_reports, ignore=True)
    DB.create_view("duplicate_dockets", duplicate_elements_of_dockets, ignore=True)


def get_unique_decisions():
    from .config import DB, DECISIONS

    dup_phil_pks = [row["pk"] for row in DB["duplicate_phils"].rows]
    dup_docket_pks = [row["pk"] for row in DB["duplicate_dockets"].rows]
    dups = dup_phil_pks + dup_docket_pks
    for row in DECISIONS.rows:
        if row["pk"] not in dups:
            yield row
