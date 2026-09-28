from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states import UtilForm
from keyboards import get_importer_kb, get_age_kb, get_main_menu_kb, get_category_kb
from services.calculator import calculate_util

router = Router()


@router.message(F.text == "⬅️ В меню")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Главное меню. Выберите действие:",
        reply_markup=get_main_menu_kb()
    )


@router.message(UtilForm.category)
async def process_category(message: Message, state: FSMContext):
    category = message.text
    if category not in ["Легковой", "Грузовой", "Автобус", "Спецтехника"]:
        await message.answer(
            "Пожалуйста, выберите категорию из кнопок ниже:",
            reply_markup=get_category_kb()
        )
        return
    await state.update_data(category=category)
    await message.answer(
        "Укажите статус импортёра:",
        reply_markup=get_importer_kb()
    )
    await state.set_state(UtilForm.importer)


@router.message(UtilForm.importer)
async def process_importer(message: Message, state: FSMContext):
    importer = message.text
    if importer not in ["Физическое лицо", "Юридическое лицо"]:
        await message.answer(
            "Пожалуйста, выберите статус из кнопок ниже:",
            reply_markup=get_importer_kb()
        )
        return
    await state.update_data(importer=importer)
    await message.answer(
        "Укажите возраст ТС:",
        reply_markup=get_age_kb()
    )
    await state.set_state(UtilForm.age)


@router.message(UtilForm.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text
    if age not in ["До 3 лет", "Старше 3 лет"]:
        await message.answer(
            "Пожалуйста, выберите возраст из кнопок ниже:",
            reply_markup=get_age_kb()
        )
        return
    await state.update_data(age=age)
    await message.answer(
        "Введите объём двигателя в см³ (только число, например: 1998):"
    )
    await state.set_state(UtilForm.engine_volume)


@router.message(UtilForm.engine_volume)
async def process_engine_volume(message: Message, state: FSMContext):
    try:
        volume = int(message.text.strip().replace(" ", ""))
        if volume <= 0 or volume > 20000:
            raise ValueError
    except ValueError:
        await message.answer(
            "Пожалуйста, введите корректное число (объём в см³, например: 1998)."
        )
        return
    await state.update_data(engine_volume=volume)
    await message.answer(
        "Введите мощность двигателя в л.с. (только число, например: 150):"
    )
    await state.set_state(UtilForm.engine_power)


@router.message(UtilForm.engine_power)
async def process_engine_power(message: Message, state: FSMContext):
    try:
        power = int(message.text.strip().replace(" ", ""))
        if power <= 0 or power > 2000:
            raise ValueError
    except ValueError:
        await message.answer(
            "Пожалуйста, введите корректное число (мощность в л.с., например: 150)."
        )
        return
    await state.update_data(engine_power=power)

    data = await state.get_data()
    result = calculate_util(data)

    if result is None:
        await message.answer(
            "❌ Не удалось рассчитать сбор. Попробуйте ещё раз через /start.",
            reply_markup=get_main_menu_kb()
        )
        await state.clear()
        return

    contact_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="💬 Написать мне в Telegram",
                url="https://t.me/nrzhnyi"
            )],
            [InlineKeyboardButton(
                text="📱 Написать в WhatsApp",
                url="https://wa.me/79261044524"
            )]
        ]
    )

    await message.answer(
        f"📊 <b>Результат расчёта утилизационного сбора</b>\n\n"
        f"Категория ТС: {result['category']}\n"
        f"Статус: {result['importer']}\n"
        f"Возраст: {result['age']}\n"
        f"Объём двигателя: {result['engine_volume']} см³\n"
        f"Мощность: {result['engine_power']} л.с.\n\n"
        f"Базовая ставка: {result['base']:,} ₽\n"
        f"Коэффициент: {result['coefficient']}\n"
        f"<b>Итого: {result['total']:,.2f} ₽</b>\n\n"
        f"⚠️ Расчёт является предварительным и не заменяет "
        f"официальный расчёт таможенного органа.\n\n"
        f"📞 <b>Нужна помощь с оформлением?</b>\n"
        f"Telegram: @nrzhnyi\n"
        f"WhatsApp: +7 926 104-45-24\n\n"
        f"Нажмите кнопку ниже или напишите мне напрямую:",
        reply_markup=contact_kb,
        parse_mode="HTML"
    )

    await message.answer(
        "Что делаем дальше?",
        reply_markup=get_main_menu_kb()
    )
    await state.clear()