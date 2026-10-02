import logging

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states import UtilForm
from keyboards import (
    get_importer_kb, get_age_kb, get_main_menu_kb,
    get_category_kb, get_engine_type_kb,
)
from services.calculator import calculate_util
from services.storage import save_calculation

logger = logging.getLogger(__name__)
router = Router()

KW_TO_HP = 1.35962


@router.message(F.text == "⬅️ В меню")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Главное меню. Выберите действие:",
        reply_markup=get_main_menu_kb()
    )


# ── ШАГ 1: тип двигателя ──
@router.message(F.text == "🚗 Рассчитать утильсбор")
async def start_calc(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🚗 <b>Расчёт утилизационного сбора</b>\n\n"
        "Для начала выберите тип двигателя:",
        reply_markup=get_engine_type_kb(),
        parse_mode="HTML"
    )
    await state.set_state(UtilForm.engine_type)


@router.message(UtilForm.engine_type)
async def process_engine_type(message: Message, state: FSMContext):
    text = message.text
    if text == "⛽ ДВС (бензин/дизель)":
        engine_type = "ICE"
    elif text == "⚡ Электромобиль":
        engine_type = "EV"
    elif text == "🔌 Гибрид":
        engine_type = "HEV"
    else:
        await message.answer("Выберите из кнопок:", reply_markup=get_engine_type_kb())
        return

    await state.update_data(engine_type=engine_type)
    await message.answer(
        "Укажите категорию ТС:",
        reply_markup=get_category_kb()
    )
    await state.set_state(UtilForm.category)


# ── ШАГ 2: категория ──
@router.message(UtilForm.category)
async def process_category(message: Message, state: FSMContext):
    category = message.text
    if category not in ["Легковой", "Грузовой", "Автобус", "Спецтехника"]:
        await message.answer("Выберите из кнопок:", reply_markup=get_category_kb())
        return
    await state.update_data(category=category)
    await message.answer("Укажите статус импортёра:", reply_markup=get_importer_kb())
    await state.set_state(UtilForm.importer)


# ── ШАГ 3: импортёр ──
@router.message(UtilForm.importer)
async def process_importer(message: Message, state: FSMContext):
    importer = message.text
    if importer not in ["Физическое лицо", "Юридическое лицо"]:
        await message.answer("Выберите из кнопок:", reply_markup=get_importer_kb())
        return
    await state.update_data(importer=importer)
    await message.answer("Укажите возраст ТС:", reply_markup=get_age_kb())
    await state.set_state(UtilForm.age)


# ── ШАГ 4: возраст ──
@router.message(UtilForm.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text
    if age not in ["До 3 лет", "Старше 3 лет"]:
        await message.answer("Выберите из кнопок:", reply_markup=get_age_kb())
        return
    await state.update_data(age=age)

    data = await state.get_data()
    engine_type = data.get("engine_type", "ICE")

    # ⚡ Для электромобилей — пропускаем объём, сразу к мощности в кВт
    if engine_type == "EV":
        await message.answer(
            "⚡ <b>Электромобиль</b>\n\n"
            "Введите мощность двигателя в <b>кВт</b> "
            "(только число, например: 150):\n\n"
            "ℹ️ Льготный тариф действует до 80 л.с. (~58.8 кВт).",
            parse_mode="HTML"
        )
        await state.set_state(UtilForm.engine_power)
        return

    # Для ДВС и гибридов — сначала объём
    await message.answer(
        "Введите объём двигателя в см³ (только число, например: 1998):"
    )
    await state.set_state(UtilForm.engine_volume)


# ── ШАГ 5: объём (только для ICE/HEV) ──
@router.message(UtilForm.engine_volume)
async def process_engine_volume(message: Message, state: FSMContext):
    try:
        volume = int(message.text.strip().replace(" ", ""))
        if volume <= 0 or volume > 20000:
            raise ValueError
    except ValueError:
        await message.answer("Введите корректное число (объём в см³, например: 1998).")
        return
    await state.update_data(engine_volume=volume)
    await message.answer(
        "Введите мощность двигателя в л.с. (только число, например: 150):"
    )
    await state.set_state(UtilForm.engine_power)


# ── ШАГ 6: мощность ──
@router.message(UtilForm.engine_power)
async def process_engine_power(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    engine_type = data.get("engine_type", "ICE")

    if engine_type == "EV":
        try:
            power_kw = float(message.text.strip().replace(" ", "").replace(",", "."))
            if power_kw <= 0 or power_kw > 1500:
                raise ValueError
        except ValueError:
            await message.answer("Введите корректное число в кВт (например: 150).")
            return
        power_hp = int(power_kw * KW_TO_HP)
        await state.update_data(engine_power=power_hp, power_kw=power_kw)
        await state.update_data(engine_volume=0)
    else:
        try:
            power_hp = int(message.text.strip().replace(" ", ""))
            if power_hp <= 0 or power_hp > 2000:
                raise ValueError
        except ValueError:
            await message.answer("Введите корректное число (мощность в л.с., например: 150).")
            return
        await state.update_data(engine_power=power_hp)

    # Финальный расчёт
    data = await state.get_data()
    result = calculate_util(data)

    if result is None:
        await message.answer(
            "❌ Не удалось рассчитать сбор. Попробуйте снова.",
            reply_markup=get_main_menu_kb()
        )
        await state.clear()
        return

    engine_label = {
        "ICE": "⛽ ДВС",
        "EV": "⚡ Электро",
        "HEV": "🔌 Гибрид",
    }.get(engine_type, "ДВС")

    summary = (
        f"{engine_label}, {result['category']}, {result['age']}, "
        f"{result['engine_power']} л.с. — {result['total']:,.0f} ₽"
    )
    save_calculation(
        user_id=message.from_user.id,
        calc_type="util",
        summary=summary,
        details=result,
    )

    power_line = f"Мощность: {result['engine_power']} л.с."
    if engine_type == "EV":
        power_kw = data.get("power_kw", 0)
        power_line = f"Мощность: {power_kw} кВт ({result['engine_power']} л.с.)"

    volume_line = ""
    if engine_type != "EV":
        volume_line = f"Объём двигателя: {result['engine_volume']} см³\n"

    if engine_type == "EV":
        if result["engine_power"] <= 80:
            status_hint = "✅ Льготный тариф (до 80 л.с.)"
        else:
            status_hint = "⚠️ Коммерческий тариф (свыше 80 л.с.)"
    elif engine_type == "HEV":
        if result["engine_power"] <= 160:
            status_hint = "✅ Льготный тариф (до 160 л.с.)"
        else:
            status_hint = "⚠️ Коммерческий тариф (свыше 160 л.с.)"
    else:
        if result["engine_power"] <= 160:
            status_hint = "✅ Льготный тариф (до 160 л.с.)"
        else:
            status_hint = "⚠️ Коммерческий тариф (свыше 160 л.с.)"

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
        f"Тип двигателя: {engine_label}\n"
        f"Категория ТС: {result['category']}\n"
        f"Статус: {result['importer']}\n"
        f"Возраст: {result['age']}\n"
        f"{volume_line}"
        f"{power_line}\n\n"
        f"{status_hint}\n\n"
        f"Базовая ставка: {result['base']:,} ₽\n"
        f"Коэффициент: {result['coefficient']}\n"
        f"<b>Итого: {result['total']:,.2f} ₽</b>\n\n"
        f"⚠️ Расчёт является предварительным и не заменяет "
        f"официальный расчёт таможенного органа.\n\n"
        f"📞 <b>Нужна помощь с оформлением?</b>\n"
        f"Telegram: @nrzhnyi\n"
        f"WhatsApp: +7 926 104-45-24",
        reply_markup=contact_kb,
        parse_mode="HTML"
    )

    await message.answer(
        "Что делаем дальше?",
        reply_markup=get_main_menu_kb()
    )
    await state.clear()
