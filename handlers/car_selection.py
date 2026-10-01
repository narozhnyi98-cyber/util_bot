import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import CarSelectionForm
from keyboards import get_main_menu_kb, get_body_type_kb, get_country_kb
from services.car_selector import select_cars

logger = logging.getLogger(__name__)
router = Router()


def parse_budget(text: str) -> int | None:
    text = text.lower().replace(" ", "").replace("₽", "").replace("руб", "").replace("р", "")
    try:
        if "млн" in text:
            return int(float(text.replace("млн", "")) * 1_000_000)
        if "тыс" in text:
            return int(float(text.replace("тыс", "")) * 1_000)
        return int(text)
    except (ValueError, TypeError):
        return None


@router.message(F.text == "🚗 Подобрать авто под бюджет")
async def start_car_selection(message: Message, state: FSMContext):
    await message.answer(
        "🚗 <b>Подбор авто под бюджет</b>\n\n"
        "Укажите ваш бюджет на автомобиль «под ключ» в рублях.\n"
        "Например: <code>2000000</code> или <code>2 млн</code>",
        parse_mode="HTML"
    )
    await state.set_state(CarSelectionForm.budget)


@router.message(CarSelectionForm.budget)
async def process_budget(message: Message, state: FSMContext):
    budget = parse_budget(message.text)
    if budget is None or budget < 500_000 or budget > 20_000_000:
        await message.answer(
            "❌ Введите сумму от 500 000 до 20 000 000 ₽.\n"
            "Например: <code>2000000</code>",
            parse_mode="HTML"
        )
        return
    await state.update_data(budget=budget)
    await message.answer("Выберите тип кузова:", reply_markup=get_body_type_kb())
    await state.set_state(CarSelectionForm.body_type)


@router.message(CarSelectionForm.body_type)
async def process_body_type(message: Message, state: FSMContext):
    bt = message.text
    if bt not in ["Седан", "Кроссовер", "Хэтчбек", "Универсал", "Любой"]:
        await message.answer("Выберите из кнопок:", reply_markup=get_body_type_kb())
        return
    await state.update_data(body_type=bt)
    await message.answer("Из какой страны?", reply_markup=get_country_kb())
    await state.set_state(CarSelectionForm.country)


@router.message(CarSelectionForm.country)
async def process_country(message: Message, state: FSMContext):
    country = message.text
    if country not in ["Япония", "Корея", "Китай", "Европа", "Любая"]:
        await message.answer("Выберите из кнопок:", reply_markup=get_country_kb())
        return

    data = await state.get_data()
    budget = data["budget"]
    body_type = data["body_type"]

    await message.answer("🔎 Подбираю варианты...")

    results = select_cars(budget, body_type, country)

    if not results:
        await message.answer(
            "😔 В этом бюджете ничего не найдено.\n"
            "Попробуйте увеличить бюджет или изменить параметры.",
            reply_markup=get_main_menu_kb()
        )
        await state.clear()
        return

    text = f"🚗 <b>Подбор под бюджет: {budget:,} ₽</b>\nТип: {body_type} | Страна: {country}\n\n"

    for i, item in enumerate(results, 1):
        car = item["car"]
        text += (
            f"<b>{i}. {car['make']} {car['model']}</b> ({car['country']}, {car['year_from']}+)\n"
            f"   • {car['engine_volume_cc']/1000:.1f} л, {car['engine_power_hp']} л.с.\n"
            f"   • Цена авто: {car['price_foreign_rub']:,} ₽\n"
            f"   • Пошлина: {item['duty']:,.0f} ₽\n"
            f"   • Сбор оформления: {item['customs_fee']:,} ₽\n"
            f"   • Утильсбор: {item['util']:,.0f} ₽\n"
            f"   • Логистика и услуги: {item['expenses']:,} ₽\n"
            f"   • <b>Итого «под ключ»: ~{item['total']:,.0f} ₽</b>\n\n"
        )

    text += (
        "⚠️ <i>Расчёт по официальным формулам (ПП РФ № 1637, 1713). "
        "Точная сумма зависит от курса ЦБ РФ на дату декларации.</i>\n\n"
        "📞 Хотите конкретный вариант и оформление? @nrzhnyi"
    )

    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu_kb())
    await state.clear()
