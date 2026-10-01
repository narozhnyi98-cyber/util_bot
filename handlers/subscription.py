from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards import get_main_menu_kb

router = Router()

CHANNEL_ID = "@tamozhelp" # Ваш канал
CHANNEL_URL = "https://t.me/tamozhelp"

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Статусы, при которых пользователь считается подписанным[reference:1]
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        # Если бот не админ или канал не найден — считаем, что доступа нет
        return False

def get_subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
    ])

@router.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if await check_subscription(bot, callback.from_user.id):
        await callback.message.delete()
        await callback.message.answer(
            "✅ Спасибо! Доступ открыт. Выберите действие:",
            reply_markup=get_main_menu_kb()
        )
    else:
        await callback.answer("❌ Вы ещё не подписались на канал!", show_alert=True)
