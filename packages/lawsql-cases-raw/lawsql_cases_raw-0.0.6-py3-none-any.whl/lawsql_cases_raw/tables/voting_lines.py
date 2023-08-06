from sqlite_utils import Database
from sqlite_utils.db import Table


def create_voting_lines_tbl(db: Database, table_name: str) -> Table:
    tbl = db[table_name]
    if tbl.exists():
        return tbl

    tbl.create(
        columns={
            "line_num": int,
            "decision_pk": str,
            "text": str,
        },
        pk=("line_num", "decision_pk"),
        foreign_keys=[("decision_pk", "Decisions", "pk")],
    )

    tbl.enable_fts(["text"], create_triggers=True)

    if not tbl.has_counts_triggers:
        tbl.enable_counts()

    return tbl
