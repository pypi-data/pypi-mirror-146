import base64
import os
from typing import Optional
from zoneinfo import ZoneInfo

import httpx
import yaml
from dateutil import parser
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
# Setup base values for the url

BASE = "https://api.github.com/repos"
OWNER = os.getenv("OWNER", None)
REPO = os.getenv("REPOSITORY", None)

# Token is generated as personal secret which expires
TOKEN = os.getenv("EXPIRING_TOKEN", None)

# Use `git rev-parse HEAD:decisions/sc` within the lawsql-raw directory
SC_TREE_SHA = os.getenv("SC_TREE_SHA", None)

# Use `git rev-parse HEAD:decisions/legacy` within the lawsql-raw directory
LEGACY_TREE_SHA = os.getenv("LEGACY_TREE_SHA", None)


def get_response(url: str) -> httpx.Response:
    """Gets the generic response from a given URL

    >>> get_response(get_base())
    <Response [200 OK]>
    """
    with httpx.Client() as client:
        return client.get(
            url,
            headers={
                "Authorization": f"token {TOKEN}",  # bearer
                "Accept": "application/vnd.github.v3+json",
            },
        )


def get_decision_data(path: str, is_sc: bool = True) -> Optional[dict]:
    """Creates a data dictionary based on the decision path; the default for the second parameter `is_sc` means that it'll use the `decisions/sc` tree path vs. the `decisions/legacy` tree path. The tree path is a SHA1 value based on `git rev-parse HEAD:<path>`"""

    def get_main_folder_url(is_sc: bool) -> str:
        """Checks whether all required env variables are setup before creating the url"""
        if not all([OWNER, TOKEN, REPO, SC_TREE_SHA, LEGACY_TREE_SHA]):
            raise SyntaxError
        base = f"{BASE}/{OWNER}/{REPO}/git/trees"  # see Note upper limit of 1000 files per directory: https://docs.github.com/en/rest/reference/repos#get-repository-content; hence need for trees/
        return f"{base}/{SC_TREE_SHA}" if is_sc else f"{base}/{LEGACY_TREE_SHA}"

    def get_basis(
        url: str, path: str, is_sc: bool
    ) -> Optional[tuple[httpx.Response, dict]]:
        """Gets the initial basis, i.e. the response and the partial data dictionary result, of a request to a URL represented by `path` and `is_sc` variables."""

        response = get_response(url)
        trees = response.json()["tree"]
        for tree in trees:
            if tree["path"] == path:
                path_url = tree["url"]
                path_response = get_response(path_url)
                path_result = {
                    "source": "sc" if is_sc else "legacy",
                    "pk": path,
                    "last_modified": parser.parse(
                        path_response.headers["last-modified"]
                    ).astimezone(ZoneInfo("Asia/Manila")),
                }
                return path_response, path_result
        return None

    def get_raw_content(d: dict) -> bytes:
        """Since the Github Tree API relies on blobs, must use the"""
        url = d["url"]
        r = get_response(url)
        data = r.json()["content"]
        return base64.b64decode(data)

    def get_additional_keys(d: dict):
        from .organizer import (
            clean_decision_category,
            clean_decision_composition,
            truncate_title,
        )

        return {
            "case_title": truncate_title(d),
            "composition": clean_decision_composition(d),
            "category": clean_decision_category(d),
            "year": int(d["date_prom"].split("-")[0]),
            "month": int(d["date_prom"].split("-")[1]),
        }

    url = get_main_folder_url(is_sc)
    basis_found = get_basis(url, path, is_sc)
    if not basis_found:
        return None

    response, result = basis_found
    data = response.json()["tree"]
    for d in data:
        if d["path"] == "body.html":
            result |= {"body": get_raw_content(d).decode("utf-8")}

        if d["path"] == "annex.html":
            result |= {"annex": get_raw_content(d).decode("utf-8")}

        if d["path"] == "ponencia.html":
            result |= {"ponencia": get_raw_content(d).decode("utf-8")}

        if d["path"] == "details.yaml":
            result |= yaml.load(get_raw_content(d), Loader=yaml.FullLoader)
    return result | get_additional_keys(result)
