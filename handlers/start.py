from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import UtilForm
from keyboards import get_main_menu_kb, get_category_kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🚗 <b>Расчёт утилизационного сбора</b>\n\n"
        "Я помогу рассчитать предварительную сумму утильсбора "
        "для вашего транспортного средства.\n\n"
        "По вопросам оформления СБКТС, ЭПТС, ГЛОНАСС — @nrzhnyi\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )


@router.message(Command("contact"))
async def cmd_contact(message: Message):
    await message.answer(
        "📞 <b>Связаться со мной</b>\n\n"
        "Telegram: @nrzhnyi\n"
        "Телефон: +7 926 104-45-24\n"
        "WhatsApp: +7 926 104-45-24\n\n"
        "Пишите в любое время — отвечу в течение часа.\n"
        "Помогу с оформлением СБКТС, ЭПТС, ГЛОНАСС и растаможкой.",
        parse_mode="HTML"
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Диалог сброшен.",
        reply_markup=get_main_menu_kb()
    )


@router.message(F.text == "🚗 Рассчитать утильсбор")
async def start_calculation(message: Message, state: FSMContext):
    await message.answer(
        "Выберите категорию ТС:",
        reply_markup=get_category_kb()
    )
    await state.set_state(UtilForm.category)


@router.message(F.text == "📞 Связаться со мной")
async def contact_button(message: Message):
    await message.answer(
        "📞 <b>Связаться со мной</b>\n\n"
        "Telegram: @nrzhnyi\n"
        "Телефон: +7 926 104-45-24\n"
        "WhatsApp: +7 926 104-45-24\n\n"
        "Пишите — отвечу в течение часа.\n"
        "Помогу с оформлением СБКТС, ЭПТС, ГЛОНАСС и растаможкой.",
        parse_mode="HTML"
    )