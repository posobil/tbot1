from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random
import requests


api_pugs : str = 'https://dog.ceo/api/breed/pug/images/random'
pug_up = requests.get(api_pugs).json()
pug_link = pug_up['message']

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = '6351251112:AAEchaYBDiGbrz0UDicVQP9N_T1ezhB5lqc'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 5

# Словарь, в котором будут храниться данные пользователей
users: dict = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f'Привет!\nХочу сыграть с тобой в игру.\nЯ загадал число от 1 до 100, попробуй его отгадать с {ATTEMPTS} попыток')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')

# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    try:
        await message.answer(
            f'Всего игр сыграно: '
            f'{users[message.from_user.id]["total_games"]}\n'
            f'Игр выиграно: {users[message.from_user.id]["wins"]}')
        await message.answer(f'Список пользователей {users}')
    except KeyError:
        await message.answer(f'Для начала введите /start')

# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


#@dp.message(F.text.lower().in_({'Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть'}))
@dp.message(F.text.lower().in_({'да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть'}))
async def process_positive_answer(message: Message):
    try:
        if not users[message.from_user.id]['in_game']:
            await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                                 'попробуй угадать!')
            users[message.from_user.id]['in_game'] = True
            users[message.from_user.id]['secret_number'] = get_random_number()
            users[message.from_user.id]['attempts'] = ATTEMPTS
        else:
            await message.answer('Пока мы играем в игру я могу '
                                 'реагировать только на числа от 1 до 100 '
                                 'и команды /cancel и /stat')
    except KeyError:
        await message.answer('А мы с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_({'нет', 'не', 'не хочу', 'не буду'}))
async def process_negative_answer(message: Message):
    try:
        if not users[message.from_user.id]['in_game']:
            await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                                 'напишите об этом')
        else:
            await message.answer('Мы же сейчас с вами играем. Присылайте, '
                                 'пожалуйста, числа от 1 до 100')
    except KeyError:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                                 'пожалуйста, числа от 1 до 100')

# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, сыграем еще?')
            await message.answer(f'{pug_link}')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Мое число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Мое число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(
                    f'К сожалению, у вас больше не осталось '
                    f'попыток. Вы проиграли :(\n\nМое число '
                    f'было {users[message.from_user.id]["secret_number"]}'
                    f'\n\nДавайте сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные текстовые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    try:
        if users[message.from_user.id]['in_game']:
            await message.answer('Мы же сейчас с вами играем. '
                                 'Присылайте, пожалуйста, числа от 1 до 100')
        else:
            await message.answer('Я довольно ограниченный бот, давайте '
                                 'просто сыграем в игру?')
    except KeyError:
        await message.answer('Мы еще не играем. Хотите сыграть?')


if __name__ == '__main__':
    dp.run_polling(bot)