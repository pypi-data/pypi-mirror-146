from dataclasses import dataclass, field
from typing import Callable, Iterator, Optional

from bs4.element import Tag
from citation_decision import CitationDocument
from decision_footnote import validated_footnotes as get_notes
from decision_section import make_sections
from decision_title import DecisionTitles
from lawsql_utils.html import get_just_integers, make_soup, remove_footnotes
from statute_matcher import StatuteMatcher

from .popover import enable_popover


@dataclass
class RawSegment:
    """Originally a section from `make_sections()`, a segment implies a portion of `LegalContent` with said portion's identified `footnotes`, `citations`, and `provisions`."""

    line: int
    content: str
    keys: list[int] = field(default_factory=list)
    footnotes: list[dict] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    provisions: list[dict] = field(default_factory=list)
    titles: list[dict] = field(default_factory=list)

    @property
    def non_html_content(self):
        return remove_footnotes(self.content)

    @property
    def with_popovers(self):
        return enable_popover(self.content, self.footnotes)


@dataclass
class LegalContent:
    """From `text` (optional `annex` with `footnotes`), create `RawSegments` which may contain `titles`, `citations`, and `provisions`."""

    text: str
    annex: Optional[str] = None
    footnotes: list[dict] = field(default_factory=list)
    segments: list[RawSegment] = field(default_factory=list)

    def __post_init__(self):
        self.footnotes = get_notes(self.text, self.annex) if self.annex else []
        self.segments = list(self._make_segments_from_sections)

    @property
    def with_popovers(self):
        return enable_popover(self.text, self.footnotes)

    @property
    def provisioned_segments(self) -> Iterator[RawSegment]:
        "Collect `RawSegments` which contain `provisions`."
        if self.segments:
            for s in self.segments:
                if s.provisions:
                    yield s

    @property
    def citation_segments(self) -> Iterator[RawSegment]:
        "Collect `RawSegments` which contain `citations`."
        if self.segments:
            for s in self.segments:
                if s.citations:
                    yield s

    @property
    def titled_segments(self) -> Iterator[RawSegment]:
        "Collect `RawSegments` which contain `titles`."
        if self.segments:
            for s in self.segments:
                if s.titles:
                    yield s

    @property
    def nominated_segments(self) -> Iterator[RawSegment]:
        "Collect `RawSegments` which contain either `titles`, `provisions` or `citations`."
        if self.segments:
            for s in self.segments:
                if s.provisions or s.citations or s.titles:
                    yield s

    @property
    def _make_segments_from_sections(self) -> Iterator[RawSegment]:
        "With formatting from `make_sections()`, create `RawSegments`"
        for section_tag in make_sections(self.text):
            data = self._extract_from_tag(section_tag)
            yield RawSegment(
                line=data["line"],
                content=data["content"],  # raw html string
                keys=data["keys"],
                footnotes=data["footnotes"],
                citations=list(extracted(citations_from, data)),
                provisions=list(extracted(provisions_from, data)),
                titles=list(extracted(titles_from, data)),
            )

    def _extract_from_tag(self, section: Tag) -> dict:
        """Extract section metadata from each section of `make_sections()`"""
        return {
            "line": int(section["id"]),
            "content": str(section),
            "keys": (keys := get_just_integers(section("sup"))),
            "footnotes": [n for k in keys for n in fns if n["key"] == k]
            if (fns := self.footnotes) and keys
            else [],
        }


def textify(key: str, d: dict) -> str:
    """Convert html text from dict (with key) to regular text format."""
    return make_soup(d[key]).get_text()


def titles_from(key: str, d: dict) -> Iterator[dict]:
    """Get text from dict (with key), create `DecisionTitle`-based dicts c/o `DecisionTitles`"""
    return DecisionTitles(textify(key, d)).iter_dicts


def citations_from(key: str, d: dict) -> Iterator[dict]:
    """Get text from dict (with key), create `RawCitation`-based dicts c/o `CitationDocument`"""
    return CitationDocument(textify(key, d)).iter_dicts


def provisions_from(key: str, d: dict) -> Iterator[dict]:
    """Get text from dict (with key), create `StatuteDesignation`s-based dicts c/o `StatuteMatcher`"""
    return StatuteMatcher(textify(key, d)).iter_dicts


def extracted(extractor_func: Callable, data: dict) -> Iterator[dict]:
    """Extract data based on `extractor` function passed.

    Args:
        extractor (Callable): Either `citations_from()` ,  `provisions_from()`, `titles_from()` extracts Iterator of dicts from text passed
        data (dict): Each `data` may have either: (a) `value` if what is passed is a footnote; or (b) `content` if what is passed is a segment.

    Yields:
        Iterator[dict]: `dict`s representing `citations`, `provisions` or `titles`.
    """
    line = {"line": data["line"]}

    if footnotes := data["footnotes"]:
        for fn in footnotes:
            if footnote_values := extractor_func("value", fn):
                for footnote_value in footnote_values:
                    yield footnote_value | line | {"key": fn["key"]}

    if content_values := extractor_func("content", data):
        for content_value in content_values:
            yield content_value | line | {"key": None}
