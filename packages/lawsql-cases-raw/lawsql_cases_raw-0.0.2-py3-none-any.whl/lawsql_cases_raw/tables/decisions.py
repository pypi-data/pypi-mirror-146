from datetime import date

from sqlite_utils import Database
from sqlite_utils.db import Table


def create_decision_tbl(db: Database, table_name: str) -> Table:
    tbl = db[table_name]
    tbl.create(
        columns={
            "pk": str,
            "source": str,
            "year": int,
            "month": int,
            "ponente_id": int,
            "ponente": str,
            "per_curiam": int,
            "date_prom": date,
            "cat": str,
            "idx": str,
            "category": str,
            "composition": str,
            "orig_idx": str,
            "scra": str,
            "phil": str,
            "docket": str,
            "case_title": str,
            "fallo": str,
            "voting": str,
            "date_scraped": date,
        },
        pk="pk",
        foreign_keys=[("ponente_id", "Justices", "pk")],
    )

    for i in [
        "date_prom",
        "ponente_id",
        "ponente",
        "cat",
        "idx",
        "category",
        "composition",
        "year",
        "source",
    ]:
        tbl.create_index([i])

    tbl.enable_fts(["fallo", "voting", "case_title"], create_triggers=True)

    if not tbl.has_counts_triggers:
        tbl.enable_counts()

    return tbl
