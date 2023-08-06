import re
from collections import namedtuple

from lawsql_cases_justices import justices_tbl, load_justices
from lawsql_utils.files import BASE_CONTENT
from sqlite_utils import Database

from .tables import create_decision_tbl, create_voting_lines_tbl

MAX_LENGTH_IDX = 100
MAX_RAW_PONENTE = 35
MAX_CASE_TITLE = 1000
MAX_FALLO = 20000
PER_CURIAM_PATTERN = re.compile(r"per\s+curiam", re.I)


MatchedRows = namedtuple("MatchedRows", ["counts", "rows"])


DB_FILE = BASE_CONTENT.joinpath("index.db")
DB = Database(DB_FILE, use_counts_table=True)


JUSTICES_TABLE_NAME = "Justices"
JUSTICES = (
    justices_tbl()
    if not DB[JUSTICES_TABLE_NAME].exists()
    else load_justices(DB[JUSTICES_TABLE_NAME])
)
if not JUSTICES.exists():
    raise Exception("Justices prerequisite to Decisions.")


DECISIONS_TABLE_NAME = "Decisions"
DECISIONS = (
    DB[DECISIONS_TABLE_NAME]
    if DB[DECISIONS_TABLE_NAME].exists()
    else create_decision_tbl(DB, DECISIONS_TABLE_NAME)
)
if not DECISIONS.exists():
    raise Exception("Decisions prerequisite to Voting Lines.")

VOTING_LINES_TABLE_NAME = "VotingLines"
VOTING_LINES = (
    DB[VOTING_LINES_TABLE_NAME]
    if DB[VOTING_LINES_TABLE_NAME].exists()
    else create_voting_lines_tbl(DB, VOTING_LINES_TABLE_NAME)
)
