import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from services.car_selector import load_cars
from services.import_advisor import compare_import
from services.storage import save_calculation

logger = logging.getLogger(__name__)
router = Router()


def get_marks_kb() -> InlineKeyboardMarkup:
    cars = load_cars()
    marks = sorted(set(c["make"] for c in cars))

    buttons = []
    row = []
    for i, mark in enumerate(marks, 1):
        row.append(InlineKeyboardButton(text=mark, callback_data=f"ia_mark:{mark}"))
        if i % 2 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_models_kb(mark: str) -> InlineKeyboardMarkup:
    cars = load_cars()
    models = [c for c in cars if c["make"] == mark]

    buttons = []
    for car in models:
        engine_type = car.get("engine_type", "ICE")
        if engine_type == "EV":
            icon = "⚡"
        elif engine_type == "HEV":
            icon = "🔌"
        else:
            icon = ""

        buttons.append([
            InlineKeyboardButton(
                text=f"{icon} {car['model']} ({car['year_from']}+, {car['country']})",
                callback_data=f"ia_car:{car['id']}"
            )
        ])

    buttons.append([InlineKeyboardButton(text="⬅️ К маркам", callback_data="ia_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == "💰 Стоит ли везти?")
async def start_import_check(message, bot: Bot):
    await message.answer(
        "💰 <b>Стоит ли везти это авто?</b>\n\n"
        "Выберите марку автомобиля — я сравню стоимость ввоза «под ключ» "
        "со средней ценой этой же модели в России.\n\n"
        "Вы узнаете: <b>везти выгодно или проще купить здесь</b>.",
        reply_markup=get_marks_kb(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "ia_back")
async def back_to_marks(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "💰 <b>Стоит ли везти это авто?</b>\n\n"
        "Выберите марку автомобиля:",
        reply_markup=get_marks_kb(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("ia_mark:"))
async def choose_mark(callback: CallbackQuery):
    await callback.answer()
    mark = callback.data.split(":", 1)[1]

    await callback.message.edit_text(
        f"💰 <b>{mark}</b>\n\n"
        f"Выберите модель:",
        reply_markup=get_models_kb(mark),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("ia_car:"))
async def choose_car(callback: CallbackQuery):
    await callback.answer()
    car_id = int(callback.data.split(":", 1)[1])

    cars = load_cars()
    car = next((c for c in cars if c["id"] == car_id), None)
    if car is None:
        await callback.message.edit_text("❌ Модель не найдена.")
        return

    result = await compare_import(car)
    if result is None:
        await callback.message.edit_text(
            f"❌ Нет данных о цене <b>{car['make']} {car['model']}</b> в РФ.\n\n"
            f"Попробуйте другую модель.",
            parse_mode="HTML"
        )
        return

    if result["is_profitable"]:
        verdict = "✅ <b>ВВОЗИТЬ ВЫГОДНО</b>"
        economy_line = f"💰 Экономия: <b>{result['difference']:,.0f} ₽</b>"
    else:
        verdict = "❌ <b>ВВОЗИТЬ НЕВЫГОДНО</b>"
        economy_line = f"💸 Выгоднее купить в РФ. Экономия: <b>{abs(result['difference']):,.0f} ₽</b>"

    engine_type = car.get("engine_type", "ICE")
    if engine_type == "EV":
        engine_label = "⚡ Электро"
    elif engine_type == "HEV":
        engine_label = f"🔌 Гибрид, {car['engine_volume_cc']/1000:.1f} л"
    else:
        engine_label = f"{car['engine_volume_cc']/1000:.1f} л"

    text = (
        f"🚗 <b>{car['make']} {car['model']}</b> ({car['year_from']}+, {car['country']})\n"
        f"{engine_label}, {car['engine_power_hp']} л.с.\n\n"
        f"<b>Стоимость ввоза «под ключ»:</b>\n"
        f"   • Авто за рубежом: {result['price_foreign']:,} ₽\n"
        f"   • Пошлина: {result['duty']:,.0f} ₽\n"
        f"   • Утильсбор: {result['util']:,.0f} ₽\n"
        f"   • Сбор оформления: {result['customs_fee']:,} ₽\n"
        f"   • Логистика + услуги: {result['expenses']:,} ₽\n"
        f"   • <b>Итого: {result['total_import']:,.0f} ₽</b>\n\n"
        f"<b>Цена этой же модели в РФ:</b>\n"
        f"   • Средняя: {result['rf_price']:,} ₽\n\n"
        f"{verdict}\n"
        f"{economy_line}\n\n"
        f"⚠️ <i>Курс EUR ЦБ РФ: {result['eur_rub']:.2f} ₽. "
        f"Цена в РФ — средняя по рынку.</i>\n\n"
        f"📞 Нужна помощь с оформлением? @nrzhnyi"
    )

    summary = (
        f"{car['make']} {car['model']} — "
        f"{'✅ выгодно' if result['is_profitable'] else '❌ невыгодно'} "
        f"(разница {abs(result['difference']):,.0f} ₽)"
    )
    save_calculation(
        user_id=callback.from_user.id,
        calc_type="import_check",
        summary=summary,
        details={
            "make": car["make"],
            "model": car["model"],
            "country": car["country"],
            "total_import": result["total_import"],
            "rf_price": result["rf_price"],
            "difference": result["difference"],
            "is_profitable": result["is_profitable"],
        }
    )

    buttons = [
        [InlineKeyboardButton(text="⬅️ Выбрать другую модель", callback_data="ia_back")],
        [InlineKeyboardButton(text="📞 Связаться со мной", url="https://t.me/nrzhnyi")],
    ]

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
