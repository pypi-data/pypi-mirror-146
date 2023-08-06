import codecs
import re
from pathlib import Path
from typing import Iterator, Optional

from citation_decision import CitationDocument

from .config import MAX_CASE_TITLE, MAX_FALLO, MAX_RAW_PONENTE, PER_CURIAM_PATTERN


def get_html(loc: Path) -> Optional[str]:
    return codecs.open(str(loc), "r").read() if loc.exists() else None


def get_raw_ponente_string(d: dict) -> Optional[str]:
    return raw if (raw := d.get("ponente", None)) else None


def is_per_curiam(d: dict) -> Optional[int]:
    if (x := get_raw_ponente_string(d)) and PER_CURIAM_PATTERN.search(x):
        return 1
    return None


def clean_raw_citations(d: dict):
    if d.get("scra", None):
        d["scra"] = CitationDocument(d["scra"]).first_canonical
    if d.get("phil", None):
        d["phil"] = CitationDocument(d["phil"]).first_canonical
    if d.get("offg", None):
        d["offg"] = CitationDocument(d["offg"]).first_canonical
    return d


def clean_raw_ponente(d: dict) -> Optional[str]:
    from unidecode import unidecode

    if not (text := get_raw_ponente_string(d)):
        return None
    if len(text) >= MAX_RAW_PONENTE:
        return None  # limit text to less than max

    text = text.replace(":", "")
    text = text.replace("*", "")
    text = text.replace("[", "")
    text = text.replace("]", "")

    return unidecode(text)  # remove accent from text


def updated_ponente_id(d: dict) -> dict:
    from lawsql_cases_justices import get_id, get_justice_label_from_id, get_surname
    from lawsql_utils.general import parse_date_if_exists

    cleaned_ponente = clean_raw_ponente(d)
    if is_per_curiam(d):
        return {"ponente": None, "ponente_id": None, "per_curiam": 1}

    if not cleaned_ponente:
        return {"ponente": d["ponente"], "ponente_id": None}

    surname = get_surname(cleaned_ponente)
    if not (date_obj := parse_date_if_exists(d["date_prom"])):
        return {"ponente": surname, "ponente_id": None}

    _id = get_id(date_obj, surname)
    return {"ponente": get_justice_label_from_id(_id), "ponente_id": _id}


def truncate_title(d: dict) -> Optional[str]:
    if not d.get("case_title", None):
        return None
    if len(d["case_title"]) >= MAX_CASE_TITLE:
        return f"{d['case_title'][:MAX_CASE_TITLE]}..."
    return d["case_title"]


def clean_decision_category(d: dict) -> Optional[str]:
    if not d.get("category", None):
        return None

    decision_start = re.compile(r"d\s*e\s*c", re.I)
    if decision_start.search(d["category"]):
        return "Decision"

    resolution_start = re.compile(r"r\s*e\s*s", re.I)
    if resolution_start.search(d["category"]):
        return "Resolution"

    return None


def clean_decision_composition(d: dict) -> Optional[str]:
    if not d.get("composition", None):
        return None

    enbanc = re.compile(r"en", re.I)
    if enbanc.search(d["composition"]):
        return "En Banc"

    division = re.compile(r"div", re.I)
    if division.search(d["composition"]):
        return "Division"

    return None


def process_fields(d: dict, detail_path: Path, folder: Path):
    return {
        "case_title": truncate_title(d),
        "composition": clean_decision_composition(d),
        "category": clean_decision_category(d),
        "year": int(d["date_prom"].split("-")[0]),
        "month": int(d["date_prom"].split("-")[1]),
        "pk": detail_path.parent.name,
        "source": folder.name,
    }


def remove_other_keys(d: dict) -> dict:
    unessential_to_lookups = [
        "origin",
        "ponencia",
        "ruling",
        "ruling_offset",
        "ruling_marker",
        "error",
        "annex",
        "initial",
        "offg",
    ]
    for key in unessential_to_lookups:
        if key in d:
            d.pop(key)
    return d


def extract_fallo(parent_folder: Path) -> dict:
    if not (path_to_location := parent_folder.joinpath("fallo.html")).exists():
        return {}
    if not (content := codecs.open(str(path_to_location), "r").read()):
        return {}
    return {"fallo": content[:MAX_FALLO]}


def filter_details(loc: Path) -> dict:
    from lawsql_utils.files import load_yaml_from_path

    data = load_yaml_from_path(loc.joinpath("details.yaml"))
    return {k: v for k, v in data.items() if k in ["annex"] and v}


def get_addl_files(loc: Path) -> Iterator[dict]:
    for k in ["annex", "ponencia"]:
        l = loc / f"{k}.html"
        if l.exists():
            yield {k: codecs.open(str(l), "r").read()}


def get_content(loc: Path) -> dict:
    contents = filter_details(loc)
    for addl in get_addl_files(loc):
        contents |= addl
    return contents


def add_content(d: dict) -> Optional[dict]:
    from lawsql_utils.files import DECISIONS_PATH

    folder = DECISIONS_PATH.joinpath(d["source"], d["pk"])
    return d | get_content(folder) if folder.exists() else None
