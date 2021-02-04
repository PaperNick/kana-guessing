import json
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import List


HIRAGANA_CHARS_PATH = Path('src') / 'kana' / 'hiragana.json'
KATAKANA_CHARS_PATH = Path('src') / 'kana' / 'katakana.json'


@dataclass
class Kana:
    char: str
    romajis: List[str]


class KanaChoice(IntEnum):
    HIRAGANA = 1
    KATAKANA = 2

    __choice_to_file__ = {
        HIRAGANA: HIRAGANA_CHARS_PATH,
        KATAKANA: KATAKANA_CHARS_PATH,
    }

    def load_chars(self) -> List[Kana]:
        kana_file = self.__choice_to_file__[self]
        kana_list = json.loads(kana_file.read_text())
        return [Kana(char=item[0], romajis=item[1]) for item in kana_list]
