from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
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
    # 1. Сразу убираем крутилку
    await callback.answer()

    # 2. Проверяем подписку
    is_sub = await check_subscription(bot, callback.from_user.id)

    if is_sub:
        # 3. ЖЕЛЕЗОБЕТОННОЕ РЕШЕНИЕ:
        # Мы не удаляем и не отправляем новое. Мы РЕДАКТИРУЕМ текущее сообщение.
        # Это гарантирует, что пользователь увидит результат мгновенно.
        
        await callback.message.edit_text(
            text="✅ Спасибо! Доступ открыт. Выберите действие:",
            reply_markup=get_main_menu_kb()
        )
        
        # Очищаем состояние
        await state.clear()
    else:
        # 4. Если не подписан: просто алерт, сообщение с кнопками остаётся
        await callback.answer("❌ Вы ещё не подписались на канал!", show_alert=True)
