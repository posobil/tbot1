from aiogram import Bot, Dispatcher, F
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.filters import BaseFilter
import os # Импортирую библиотеку для использования данных из окружения

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
API_TOKEN: str = '6351251112:AAEchaYBDiGbrz0UDicVQP9N_T1ezhB5lqc'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Список с ID администраторов бота. !!!Замените на ваш!!!
admin_ids: list[int] = [173901673]


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Список с ID администраторов бота. !!!Замените на ваш!!!
admin_ids: list[int] = [173901673]


# Собственный фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# Этот хэндлер будет срабатывать, если апдейт от админа
@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    await message.answer(text='Вы админ')


# Этот хэндлер будет срабатывать, если апдейт не от админа
@dp.message()
async def answer_if_not_admins_update(message: Message):
    await message.answer(text='Вы не админ')

print(os.getenv('BOT_TOKEN')) # Вывожу в консоль переменную из окружения (токен бота)

if __name__ == '__main__':
    dp.run_polling(bot)