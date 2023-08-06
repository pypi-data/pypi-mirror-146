from dataclasses import dataclass
from datetime import date
from enum import Enum, auto, unique
from pathlib import Path
from typing import NoReturn, Optional, Union

MAX_TITLE_LENGTH = 1000  # creation of statute title types


@dataclass
class StatuteItem:
    """
    Utilizes `StatuteID` to get data from `*.yaml` files through the `category` and `idx` parameters.

    This will process data to generate a `StatuteItem` with titles that map to `TitleConvetions`."""

    category: str
    idx: str

    def __post_init__(self):
        from lawsql_tree_unit import get_first_short_title_from_units
        from lawsql_utils.general import format_full_date
        from statute_serial_number import StatuteID, get_member

        self.category: str = self.category.upper()
        self.idx: str = self.idx.upper()
        self.member: StatuteID = get_member(self.category)
        self.category_label: str = self.get_category_label()
        self.folder: Path = self.member.data_source_folder(self.idx)
        self.data: dict = self.get_data
        self.specified_date: date = format_full_date(self.data["date"])
        self.units: list[dict] = self.data["units"]
        self.emails: list[str] = self.data.get("emails", None)
        self.effects: list[str] = self.data.get("effects", None)
        self.short_title = get_first_short_title_from_units(
            {"units": self.units}
        )
        self.serial_title = self.member.make_title(self.idx)
        self.aliases = self.data.get("aliases", [])
        self.titles: dict = {
            "short": self.short_title,
            "official": self.official_title,
            "serial": self.serial_title,
            "aliases": self.aliases,
        }

    def get_category_label(self):
        text = self.member.value[0]
        if the_word_number := self.member.value[1]:
            text = f"{text} {the_word_number}"  # e.g. No./Blg. if present
        return text

    @property
    def get_data(self) -> Union[NoReturn, dict]:
        from lawsql_tree_unit import format_units, load_data

        # secure data from the folder
        if not (raw_data := load_data(self.folder)):
            raise Exception(f"No data from {self.folder}")

        if "date" not in raw_data:
            raise Exception(f"Date missing from StatuteItem")
        if "units" not in raw_data:
            raise Exception(f"Units missing from StatuteItem")
        format_units(raw_data["units"])  # adds a short title, if possible
        return raw_data

    @property
    def effective_actions(self) -> list[dict]:
        """Parse the data for all values with the key `effects`"""
        import itertools

        from lawsql_utils.trees import data_tree_walker

        return list(itertools.chain(*data_tree_walker(self.data, "effects")))

    @property
    def official_title(self) -> Optional[str]:
        from lawsql_utils.general import trim_text

        raw = self.data.get("law_title", None) or self.data.get("item", None)
        return trim_text(raw, MAX_TITLE_LENGTH) if raw else None


def get_statute_title_convention_choices() -> list[str]:
    """Get the names of each member of the `TitleConventions` enum"""

    @unique
    class StatuteTitleConventions(Enum):
        SERIAL = auto()  # e.g. Republic Act No. 386
        SHORT = auto()  # e.g. Civil Code of the Philippines
        OFFICIAL = auto()  # e.g. An Act to Ordain and Institute the...
        ALIAS = auto()  # e.g. New Civil Code

    return [name for name, _ in StatuteTitleConventions.__members__.items()]


def get_statute_on_local(text: str) -> Optional[StatuteItem]:
    """Given text denominated as a statute by `StatuteMatcher`, e.g. 'Republic Act No. 386', 'Civil Code', get a prefilled `StatuteItem` from the local `rawlaw` repository.
    >>> x = get_statute_on_local("Republic Act No. 10410")
    StatuteItem(category='RA', idx='10410')
    """
    from statute_matcher import StatuteMatcher

    try:
        if match := StatuteMatcher.get_single_category_idx(text):
            return StatuteItem(match[0], match[1])
    except Exception as e:
        print(f"{e}")
    return None
