from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext  # <-- ЭТОГО НЕ ХВАТАЛО
from keyboards import get_main_menu_kb

router = Router()

CHANNEL_ID = "@tamozhelp"
CHANNEL_URL = "https://t.me/tamozhelp"

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

def get_subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
    ])

@router.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()  # <-- Обязательно: убирает «крутящуюся» анимацию

    try:
        is_sub = await check_subscription(bot, callback.from_user.id)
    except Exception as e:
        print(f"Критическая ошибка в обработчике подписки: {e}")
        await callback.message.edit_text("⚠️ Не удалось проверить подписку. Обратитесь к администратору.")
        return

    if is_sub:
        await callback.message.delete()
        await callback.message.answer(
            "✅ Спасибо!

    else:
        # Пользователь НЕ подписан: показываем всплывающее уведомление, кнопки остаются
        await callback.answer("❌ Вы ещё не подписались на канал!", show_alert=True)
