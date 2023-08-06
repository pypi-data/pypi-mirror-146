from bs4 import BeautifulSoup, Tag
from lawsql_utils.html import get_pure_digit_key_from_sup_tag, make_soup


def get_value(item: str, notes: list[dict]) -> str:
    for note in notes:
        if note["key"] == int(item):
            return note["value"]
    return "No value found."


def bootstrap_popover(html: BeautifulSoup, key: str, notes: list[dict]) -> Tag:
    new_tag = html.new_tag("span")
    new_tag.string = key
    new_tag["class"] = "footnote"
    new_tag["data-bs-toggle"] = "popover"
    new_tag["title"] = key
    new_tag["data-bs-content"] = get_value(key, notes)
    return new_tag


def enable_popover(text: str, notes: list[dict]) -> str:
    """
    1. Each text, passed on for loop, should be an html string that potentially contains footnote tags <sup>
    2. Notes are a list of footnote dicts. Some segments do not have footnotes.
    3. For each segment, replace <sup> with <span>
    4. The span will contain visible text: the footnote key
    5. The span will contain a hidden attribute "data content" which should hold the value of the footnote
    """
    if not notes:
        return text

    html = make_soup(text)

    if not (sups := html("sup")):
        return text

    for sup_tag in sups:

        if not (key := get_pure_digit_key_from_sup_tag(sup_tag)):
            continue

        sup_tag.replace_with(bootstrap_popover(html, key, notes))

    return str(html)
