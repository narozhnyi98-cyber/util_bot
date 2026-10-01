from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from keyboards import get_main_menu_kb

router = Router()

CHANNEL_ID = "@tamozhelp"  # Твой канал
CHANNEL_URL = "https://t.me/tamozhelp"

async def check_subscription(bot: Bot, user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на канал."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Статусы, при которых пользователь считается подписанным
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        # Если бот не админ или канал не найден — логируем ошибку и возвращаем False
        print(f"Ошибка проверки подписки (возможно, бот не админ): {e}")
        return False

def get_subscription_kb() -> InlineKeyboardMarkup:
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
    ])

@router.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery, bot: Bot, state: FSMContext):
    # ВАЖНО: Сразу подтверждаем получение нажатия. Без этого Telegram крутит индикатор загрузки.
    await callback.answer()

    try:
        is_sub = await check_subscription(bot, callback.from_user.id)
    except Exception as e:
        print(f"Критическая ошибка в обработчике подписки: {e}")
        await callback.message.edit_text(
            "⚠️ Не удалось проверить подписку. Обратитесь к администратору."
        )
        return

    if is_sub:
        # Пользователь подписан: удаляем экран подписки и показываем главное меню
        await callback.message.delete()
        await callback.message.answer(
            "✅ Спасибо! Доступ открыт. Выберите действие:",
            reply_markup=get_main_menu_kb()
        )
    else:
        # Пользователь НЕ подписан: показываем всплывающее уведомление, кнопки остаются
        await callback.answer("❌ Вы ещё не подписались на канал!", show_alert=True)
