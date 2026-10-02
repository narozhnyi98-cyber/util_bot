import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import get_main_menu_kb
from services.storage import get_user_calculations, delete_user_calculations

logger = logging.getLogger(__name__)
router = Router()

TYPE_NAMES = {
    "util": "🚗 Расчёт утильсбора",
    "selection": "🚗 Подбор под бюджет",
    "import_check": "💰 Стоит ли везти",
}


@router.message(F.text == "📋 Мои расчёты")
async def show_calculations(message: Message):
    calcs = get_user_calculations(message.from_user.id, limit=10)

    if not calcs:
        await message.answer(
            "📋 <b>Мои расчёты</b>\n\n"
            "У вас пока нет сохранённых расчётов.\n\n"
            "Сделайте расчёт утильсбора, подберите авто или проверьте "
            "«стоит ли везти» — история появится здесь.",
            parse_mode="HTML",
            reply_markup=get_main_menu_kb()
        )
        return

    text = "📋 <b>Мои расчёты</b> (последние 10):\n\n"

    for i, calc in enumerate(calcs, 1):
        try:
            date = datetime.fromisoformat(calc["created_at"]).strftime("%d.%m.%Y %H:%M")
        except Exception:
            date = "—"

        type_name = TYPE_NAMES.get(calc["calc_type"], "Расчёт")

        text += (
            f"<b>{i}. {type_name}</b>\n"
            f"   {calc['summary']}\n"
            f"   <i>{date}</i>\n\n"
        )

    buttons = [
        [InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_history")]
    ]

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@router.callback_query(F.data == "clear_history")
async def clear_history(callback: CallbackQuery):
    delete_user_calculations(callback.from_user.id)
    await callback.answer("История очищена", show_alert=True)

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        "🗑 <b>История расчётов очищена.</b>",
        parse_mode="HTML",
        reply_markup=get_main_menu_kb()
    )
