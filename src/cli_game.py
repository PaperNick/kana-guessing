from typing import Optional

from src.cli_helpers import ColorMessage
from src.engine import Game
from src.models import Kana, KanaChoice


class CliGame:
    def __init__(self, game: Game) -> None:
        self._game = game

    def _get_user_guess(self, kana: Kana, prompt_message: Optional[str] = None) -> str:
        if prompt_message is None:
            prompt_message = f'Enter the romaji transliteration of "{kana.char}": '

        print(prompt_message, end='')
        guess = input().strip()

        return guess

    def prompt_new_kana(self) -> str:
        kana = self._game.next_kana()
        return self._get_user_guess(kana)

    def prompt_current_kana(self) -> str:
        kana = self._game.current_kana() or self._game.next_kana()
        return self._get_user_guess(kana)

    def is_guess_correct(self, romaji_guess: str) -> bool:
        is_correct = self._game.make_guess(romaji_guess)

        if is_correct:
            print(f'{ColorMessage.success("Correct!")}\n')
            self._game.increment_correct()
        else:
            romajis = self._game.correct_answer()
            answers = ' or '.join(romajis)
            print(f'{ColorMessage.error("Incorrect.")} The correct answer is -- "{answers}"\n')
            self._game.increment_incorrect()

        return is_correct

    def show_score(self) -> None:
        correct_guesses, incorrect_guesses = self._game.score()
        print(f'{ColorMessage.success("Correct guesses:")} {correct_guesses}')
        print(f'{ColorMessage.error("Incorrect guesses:")} {incorrect_guesses}\n')

    def quit(self) -> None:
        print('Thanks for playing! Your score is:')
        self.show_score()
        quit_game()


def quit_game(*args, **kwargs) -> None:
    exit()


def main() -> None:
    print('Welcome to the Kana guessing game.')
    print('Enter the romaji transliteration of the kana which is shown.')
    print('To view your score type "s" or "score"')
    print('Press "q" to quit at any time.\n')
    print('Select your Kana of choice:')
    print(f'To select Hiragana, type "{KanaChoice.HIRAGANA}"')
    print(f'To select Katakana, type "{KanaChoice.KATAKANA}"')

    kana_choice = input().strip()
    allowed_choices = (f'{KanaChoice.HIRAGANA}', f'{KanaChoice.KATAKANA}')
    while kana_choice not in allowed_choices:
        print(f'Please type {KanaChoice.HIRAGANA} or {KanaChoice.KATAKANA}: ', end='')
        kana_choice = input().strip()

    kana_chars = KanaChoice(int(kana_choice)).load_chars()
    game = Game(kana_chars)
    cli_game = CliGame(game)

    command_to_action = {
        'q': cli_game.quit,
        'quit': cli_game.quit,
        's': cli_game.show_score,
        'score': cli_game.show_score,
    }

    previous_user_input = None
    current_user_input = None
    while True:
        if previous_user_input in command_to_action:
            current_user_input = cli_game.prompt_current_kana()
        else:
            current_user_input = cli_game.prompt_new_kana()

        if current_user_input in command_to_action:
            action = command_to_action[current_user_input]
            action()
        else:
            cli_game.is_guess_correct(current_user_input)

        previous_user_input = current_user_input
