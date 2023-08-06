import re
from collections import namedtuple

from lawsql_utils.files import BASE_CONTENT
from sqlite_utils import Database

MAX_LENGTH_IDX = 100
MAX_RAW_PONENTE = 35
MAX_CASE_TITLE = 1000
MAX_FALLO = 20000
PER_CURIAM_PATTERN = re.compile(r"per\s+curiam", re.I)


MatchedRows = namedtuple("MatchedRows", ["counts", "rows"])


DB_FILE = BASE_CONTENT.joinpath("index.db")
DB = Database(DB_FILE, use_counts_table=True)
