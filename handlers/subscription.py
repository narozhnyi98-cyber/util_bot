import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from keyboards import get_main_menu_kb

logger = logging.getLogger(__name__)
router = Router()

CHANNEL_ID = "@tamozhelp"
CHANNEL_URL = "https://t.me/tamozhelp"


async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        logger.info(f"Статус пользователя {user_id}: {member.status}")
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"ОШИБКА ПРОВЕРКИ ПОДПИСКИ: {type(e).__name__}: {e}")
        return False


def get_subscription_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
    ])


@router.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery, bot: Bot, state: FSMContext):
    logger.info(f"НАЖАТА КНОПКА check_sub пользователем {callback.from_user.id}")
    await callback.answer()

    is_sub = await check_subscription(bot, callback.from_user.id)
    logger.info(f"Результат проверки: is_sub={is_sub}")

    if is_sub:
        try:
            await callback.message.delete()
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение: {e}")

        await bot.send_message(
            chat_id=callback.from_user.id,
            text="✅ Спасибо! Доступ открыт. Выберите действие:",
            reply_markup=get_main_menu_kb()
        )
        await state.clear()
        logger.info("Меню отправлено")
    else:
        await callback.answer("❌ Вы ещё не подписались на канал!", show_alert=True)
