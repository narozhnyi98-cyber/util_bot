from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import UtilForm
from keyboards import get_main_menu_kb, get_category_kb
from handlers.subscription import check_subscription, get_subscription_kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user_id = message.from_user.id

    # Проверяем, подписан ли пользователь на канал
    if await check_subscription(bot, user_id):
        # Если подписан — показываем главное меню
        await message.answer(
            "🚗 <b>Расчёт утилизационного сбора</b>\n\n"
            "Я помогу рассчитать предварительную сумму утильсбора "
            "для вашего транспортного средства.\n\n"
            "По вопросам оформления СБКТС, ЭПТС, ГЛОНАСС — @nrzhnyi\n\n"
            "Выберите действие:",
            reply_markup=get_main_menu_kb(),
            parse_mode="HTML"
        )
    else:
        # Если не подписан — показываем экран с кнопкой подписки
        await message.answer(
            "👋 Для доступа к боту подпишитесь на наш канал.\n\n"
            "Это бесплатно и займёт 5 секунд.",
            reply_markup=get_subscription_kb()
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
async def start_calculation(message: Message, state: FSMContext, bot: Bot):
    # Заодно проверяем подписку и здесь — на случай, если отписались
    if not await check_subscription(bot, message.from_user.id):
        await message.answer(
            "👋 Для доступа к боту подпишитесь на наш канал.\n\n"
            "Это бесплатно и займёт 5 секунд.",
            reply_markup=get_subscription_kb()
        )
        return

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
