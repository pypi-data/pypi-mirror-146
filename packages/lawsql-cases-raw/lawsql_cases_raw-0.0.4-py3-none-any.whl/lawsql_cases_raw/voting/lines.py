import re
from typing import Iterator, Optional

from bs4 import BeautifulSoup as Soup
from lawsql_cases_justices import get_justices_on_date

CONCUR = "concur."


def get_voting_lines(d: dict) -> Optional[Soup]:
    return breaks(v) if (v := d.get("voting", None)) else None


def breaks(html_text: str) -> Iterator[str]:
    return (el for i in html_text.split("<br>") if (el := i.strip()) and (el != "<hr>"))


def create_lines(d: dict):
    counter = 0
    if breaks := get_voting_lines(d):
        for break_text in breaks:
            if line := Soup(break_text.strip(), "html.parser").get_text().strip():
                counter += 1
                yield {"line_num": counter, "text": line, "decision_pk": d["pk"]}


def get_first_concurring_line(d: dict):
    if breaks := get_voting_lines(d):
        for break_text in breaks:
            if CONCUR in break_text:
                return Soup(break_text, "html.parser")


def get_actives_date_voting(d: dict):
    return list(get_justices_on_date(d["date_prom"]))


def get_post_concur_text(text: str) -> str:
    return text[text.find(CONCUR) + len(CONCUR) :].strip()


def get_pre_concur_text(text: str) -> str:
    return text[: text.find(CONCUR)]


def get_concurrers(text: str):
    stack: list[str] = []
    text = text.replace("*", " ")
    items = re.split(r"(,|\band\b)", text)

    for item in items:
        if el := item.strip().removeprefix("and").strip().removeprefix(".").strip(", "):
            if el not in [
                "C.J.",
                "JJ.",
                "JBL",
                "C. J.",
                "Acting C.J.",
                "(Chairperson)",
                "(Chairman)",
                "(Acting Chief Justice)",
            ]:
                if el not in ["Jr.", "Sr."]:
                    if len(stack):
                        yield stack.pop(0)
                    stack.append(el)
                else:
                    previous = stack.pop(0)
                    yield f"{previous}, {el}"

    if len(stack):
        yield stack.pop(0)


def concurring_justices(d: dict):
    if not (soup := get_first_concurring_line(d)):
        return None
    return get_concurrers(get_pre_concur_text(soup.get_text()))
