from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import requests

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = '6351251112:AAEchaYBDiGbrz0UDicVQP9N_T1ezhB5lqc'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

api_pugs : str = 'https://dog.ceo/api/breed/pug/images/random'
pug_up = requests.get(api_pugs).json()
pug_link = pug_up['message']


# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')
    print(message.model_dump_json(indent=4, exclude_none=True))


# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

async def send_sticker_echo(message: Message):
    await message.reply_sticker(message.sticker.file_id)
    print(message.model_dump_json(indent=4, exclude_none=True))


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
async def send_echo(message: Message):
    await message.reply(text=message.text)
    print(message.model_dump_json(indent=4, exclude_none=True))


# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_sticker_echo, F.sticker)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)
