import random
from typing import List, Optional, Tuple

from src.models import Kana


class Game:
    def __init__(self, kana_chars: List[Kana]) -> None:
        self._correct_guesses = 0
        self._incorrect_guesses = 0
        self._kana_chars = kana_chars
        self._current_kana: Optional[Kana] = None

    def increment_correct(self) -> int:
        self._correct_guesses += 1
        return self._correct_guesses

    def increment_incorrect(self) -> int:
        self._incorrect_guesses += 1
        return self._incorrect_guesses

    def make_guess(self, romaji_guess: str) -> bool:
        if self._current_kana is None:
            raise ValueError('No kana character selected. Please generate one first.')

        return romaji_guess in self._current_kana.romajis

    def correct_answer(self) -> List[str]:
        if self._current_kana is None:
            raise ValueError('No kana character selected. Please generate one first.')

        return self._current_kana.romajis

    def current_kana(self) -> Optional[Kana]:
        return self._current_kana

    def next_kana(self) -> Kana:
        self._current_kana = random.choice(self._kana_chars)
        return self._current_kana

    def score(self) -> Tuple[int, int]:
        return (self._correct_guesses, self._incorrect_guesses)
