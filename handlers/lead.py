import logging
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import LeadForm
from keyboards import get_main_menu_kb, get_lead_cancel_kb, get_lead_skip_kb

logger = logging.getLogger(__name__)
router = Router()

# ⚠️ ЗАМЕНИ НА CHAT_ID ВТОРОГО АККАУНТА (@tamozhelp_leads)
ADMIN_CHAT_ID = 8601515134


@router.message(F.text == "❌ Отменить")
async def cancel_lead(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Заявка отменена. Возвращаю в меню.",
        reply_markup=get_main_menu_kb()
    )


@router.message(F.text == "📩 Оформить под ключ")
async def start_lead(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📩 <b>Заявка на оформление</b>\n\n"
        "Задам несколько вопросов — и передам вашу заявку специалисту.\n\n"
        "Как вас зовут?",
        parse_mode="HTML",
        reply_markup=get_lead_cancel_kb()
    )
    await state.set_state(LeadForm.name)


@router.message(LeadForm.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2 or len(name) > 100:
        await message.answer("Введите имя (от 2 до 100 символов):")
        return
    await state.update_data(name=name)
    await message.answer(
        f"Приятно познакомиться, {name}!\n\n"
        f"Укажите телефон или @username для связи:",
        reply_markup=get_lead_cancel_kb()
    )
    await state.set_state(LeadForm.phone)


@router.message(LeadForm.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if len(phone) < 5 or len(phone) > 100:
        await message.answer("Введите корректный телефон или @username:")
        return
    await state.update_data(phone=phone)
    await message.answer(
        "Опишите вашу задачу: какую машину хотите, откуда, в какие сроки.\n\n"
        "Если не хотите писать — нажмите «➡️ Пропустить».",
        reply_markup=get_lead_skip_kb()
    )
    await state.set_state(LeadForm.comment)


@router.message(LeadForm.comment)
async def process_comment(message: Message, state: FSMContext, bot: Bot):
    if message.text == "➡️ Пропустить":
        comment = "—"
    else:
        comment = message.text.strip()
        if len(comment) > 1000:
            comment = comment[:1000] + "..."

    data = await state.get_data()
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"

    admin_text = (
        f"🔥 <b>НОВАЯ ЗАЯВКА</b>\n\n"
        f"👤 <b>Имя:</b> {data['name']}\n"
        f"📱 <b>Контакт:</b> {data['phone']}\n"
        f"💬 <b>Задача:</b> {comment}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🆔 Telegram ID: <code>{user.id}</code>\n"
        f"🔗 Username: {username}\n"
        f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text,
            parse_mode="HTML"
        )
        logger.info(f"Заявка от {user.id} ({username}) отправлена админу")
    except Exception as e:
        logger.error(f"Не удалось отправить заявку админу: {e}")

    await message.answer(
        "✅ <b>Заявка принята!</b>\n\n"
        "Я свяжусь с вами в течение 1 рабочего часа.\n\n"
        "Если хотите ускорить — напишите мне напрямую: @nrzhnyi",
        parse_mode="HTML",
        reply_markup=get_main_menu_kb()
    )
    await state.clear()
