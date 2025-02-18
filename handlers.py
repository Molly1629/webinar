from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from db import User, async_session

router = Router()
CHANNEL_USERNAME = "@mainranepa"


async def get_channel_id(bot):
    chat = await bot.get_chat(CHANNEL_USERNAME)

    return chat.id


@router.message(Command("start"))
async def start(message: Message):
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name
            )
            session.add(user)
            await session.commit()

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Регистрация"), KeyboardButton(text="Справка")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            "Добро пожаловать! Зарегистрируйтесь на вебинар:",
            reply_markup=keyboard
        )


@router.message(F.text == "Справка")
async def help(message: Message):
    await message.answer(
        "1. Нажмите '🎫 Регистрация'\n"
        "2. Вступите в нашу группу\n"
        "3. Получите доступ к вебинару"
    )


@router.message(F.text == "Регистрация")
async def register(message: Message, bot: Bot):
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)

        chat_id = await get_channel_id(bot)
        member = await bot.get_chat_member(chat_id, user.telegram_id)

        if member.status in ["member", "administrator", "creator"]:
            user.subscribed = True
            user.registered = True

            await session.commit()

            await message.answer(
                "Регистрация успешна!\n"
                "Ссылка на вебинар: https://example.com/webinar",
                reply_markup=ReplyKeyboardMarkup(remove_keyboard=True)
            )
        else:
            await message.answer(f"Вступите в группу: {CHANNEL_USERNAME}")
