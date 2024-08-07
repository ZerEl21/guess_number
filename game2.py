from datetime import datetime as dt
from random import randint

ADMIN_USERNAME = 'Admin'
UNKNOWN_COMMAND = 'Неизвестная команда, попробуйте еще раз!'

start_time = dt.now()


# def access_control(func):
#     def wrapper(*args, **kwargs):
#         if kwargs.get('username') == ADMIN_USERNAME:
#             result = func(*args, **kwargs)
#             return result
#         else:
#             print(UNKNOWN_COMMAND)
#     return wrapper

def access_control(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('username') == ADMIN_USERNAME:
            result = func(*args, **kwargs)
            return result
        else:
            print(UNKNOWN_COMMAND)
    return wrapper


class User:
    def __init__(self, username) -> None:
        self.total_games = 0
        self.username = username

    def game(self) -> None:
        # Получаем случайное число в диапазоне от 1 до 100.
        self.number = randint(1, 100)
        print(
            '\nУгадайте число от 1 до 100.\n'
            'Для выхода из текущей игры введите команду "stop"'
        )
        while True:
            # Получаем пользовательский ввод,
            # отрезаем лишние пробелы и переводим в нижний регистр.
            user_input = input('Введите число или команду: ').strip().lower()

            if user_input == 'stop':
                break
            elif user_input == 'stat':
                self.get_statistics(username=self.username)
            elif user_input == 'answer':
                self.get_right_answer(username=self.username)
            else:
                try:
                    guess = int(user_input)
                except ValueError:
                    print(UNKNOWN_COMMAND)
                    continue

                if self.check_number(guess):
                    break

    @access_control
    def get_statistics(self, *args, **kwargs) -> None:
        game_time = dt.now() - start_time
        print(
            f'Общее время игры: {game_time}, '
            f'текущая игра - №{self.total_games}'
            )

    @access_control
    def get_right_answer(self, *args, **kwargs) -> None:
        print(f'Правильный ответ: {self.number}')

    def check_number(self, guess: int) -> bool:
        # Если число угадано...
        if guess == self.number:
            print(f'Отличная интуиция, {self.username}! Вы угадали число :)')
            # ...возвращаем True
            return True

        if guess < self.number:
            print('Ваше число меньше того, что загадано.')
        else:
            print('Ваше число больше того, что загадано.')
        return False


def get_username() -> str:
    username = input('Представьтесь, пожалуйста, как Вас зовут?\n').strip()
    if username == ADMIN_USERNAME:
        print(
            '\nДобро пожаловать, создатель! '
            'Во время игры вам доступны команды "stat", "answer"'
        )
    else:
        print(f'\n{username}, добро пожаловать в игру!')
    return username


def guess_number() -> None:
    username = get_username()
    this_game = User(username)

    while True:
        this_game.total_games += 1
        this_game.game()
        play_again = input('\nХотите сыграть ещё? (yes/no) ')
        if play_again.strip().lower() not in ('y', 'yes'):
            break


if __name__ == '__main__':
    print(
        'Вас приветствует игра "Угадай число"!\n'
        'Для выхода нажмите Ctrl+C'
    )
    guess_number()
