import re
from dataclasses import asdict, dataclass, field
from typing import Iterator, Optional

from bs4.element import Tag
from citation_decision import (
    CitationDocument,
    get_first_docket_model,
    slice_until_end_of_first_citation,
)
from decision_title_vs_inre import (
    VS_EM_PATTERN,
    VSINRE,
    VSINRE_PLUS,
    get_docketlike_text_from_em_tag_and_sibling,
    get_inre_subject_from_text,
    get_parties_from_text,
    get_vs_inre_lines,
    is_single_pattern,
)
from decision_title_vs_inre.checked_latin import no_citation_possible
from lawsql_utils.general import get_splits_from_slicer as splitter
from lawsql_utils.html import make_soup, make_soup_get_italicized


@dataclass
class DecisionTitle:

    nominee: str
    title: Optional[str] = None
    plaintiff: Optional[str] = None
    defendant: Optional[str] = None
    inre: Optional[str] = None
    docket: Optional[str] = None
    phil: Optional[str] = None
    scra: Optional[str] = None
    offg: Optional[str] = None
    citation: Optional[str] = None

    def __post_init__(self):
        if not self.citation:
            if cite := CitationDocument(self.converted_text).first:
                self.docket = cite.docket
                self.scra = cite.scra
                self.phil = cite.phil
                self.offg = cite.offg
                self.citation = cite.model.match.group(0)

        self.title = self.culled(self.citation, self.converted_text)

        if party := get_parties_from_text(self.title):
            x, y = party.plaintiff, self.culled(self.citation, party.defendant)
            self.plaintiff, self.defendant = x, y

        elif subject := get_inre_subject_from_text(self.title):
            self.inre = subject

    @property
    def converted_text(self) -> str:
        return make_soup(self.nominee).get_text()

    def culled(self, pattern: Optional[str], target: str):
        """If no `pattern` exists, return the `target`; if it does, remove `pattern` from the `target` by first escaping special characters of `x` (e.g. `.` which appears in many citation formats) and then substituting the escaped pattern with a blank string `""`"""
        return re.sub(re.escape(pattern), "", target) if pattern else target


@dataclass
class DecisionTitles:
    """Divide text into lines, each line has one or many `DecisionTitle`s"""

    text: str
    candidates: list[DecisionTitle] = field(default_factory=list)

    def __post_init__(self):
        if VSINRE_PLUS.search(self.text):
            self.candidates = list(self.lines)

    @property
    def lines(self) -> Iterator[DecisionTitle]:
        for line in get_vs_inre_lines(self.text):
            italic_indicators = make_soup_get_italicized(line, VSINRE)

            # <em>vs.</em> OR no `<em>` found in line; make splits on citation
            if VS_EM_PATTERN.search(line) or not italic_indicators:
                yield from self.title_citation_splits(line)

            # edge case: <em>X v. Y, GR. 11241</em> Jan. 1, 20000
            elif docket_found := self.neighbor_is_date(italic_indicators[0]):
                yield DecisionTitle(docket_found)

            else:  # process each <em> in line
                for italic in italic_indicators:
                    if is_single_pattern(italic):  # only one case found
                        yield self.get_title_from_element(italic)
                    else:  # likely multiple cases; make splits on citation
                        yield from self.title_citation_splits(str(italic))

    def neighbor_is_date(self, candidate: Tag) -> Optional[str]:
        """Is italicized tag a part of a longer docket citation with the date as the next sibling of the tag?"""
        if nominee := get_docketlike_text_from_em_tag_and_sibling(candidate):
            if get_first_docket_model(nominee):
                return nominee
        return None

    def title_citation_splits(self, line: str) -> Iterator[DecisionTitle]:
        """Must split the line based on citations found. The `slice_until_end_of_first_citation` will be called repeatedly until the line is exhausted. Each call should result in a subline which may contain a `VSINRE_PLUS` pattern."""
        for subline in splitter(line, slice_until_end_of_first_citation):
            if VSINRE_PLUS.search(subline):
                yield DecisionTitle(subline)

    def get_title_from_element(self, italic: Tag) -> DecisionTitle:
        """Based on `is_single_pattern`, there is a `DecisionTitle` within the tag; the only question is if the next sibling of the tag is a citation of the `DecisionTitle` found."""
        title = DecisionTitle(italic.get_text())
        if no_citation_possible(italic):  # crude checker.
            return title

        if not title.citation:
            if cite := CitationDocument(str(italic.next_sibling)).first:
                title.docket = cite.docket
                title.scra = cite.scra
                title.phil = cite.phil
                title.offg = cite.offg
                title.citation = cite.model.match.group(0)
        return title

    @property
    def iter_dicts(self):
        """Get titles as dict in given `text`"""
        if self.candidates:
            for candidate in self.candidates:
                yield asdict(candidate)
