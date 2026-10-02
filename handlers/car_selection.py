import logging

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import CarSelectionForm
from keyboards import get_main_menu_kb, get_body_type_kb, get_country_kb
from services.car_selector import select_cars
from services.storage import save_calculation

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
        await message.answer("❌ Введите сумму от 500 000 до 20 000 000 ₽.\nНапример: <code>2000000</code>", parse_mode="HTML")
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
    results = await select_cars(budget, body_type, country)

    if not results:
        await message.answer(
            f"😔 В бюджете {budget:,} ₽ ничего не найдено.\n\n"
            f"Ввоз «под ключ» обычно стоит в 1.5–2 раза дороже самой машины.\n\n"
            f"👉 Попробуйте увеличить бюджет до <b>{int(budget * 1.8):,} ₽</b>.",
            parse_mode="HTML", reply_markup=get_main_menu_kb()
        )
        await state.clear()
        return

    summary = f"Бюджет {budget:,} ₽, {body_type}, {country} — {len(results)} вариантов"
    save_calculation(user_id=message.from_user.id, calc_type="selection", summary=summary,
                     details={"budget": budget, "body_type": body_type, "country": country, "found": len(results)})

    text = f"🚗 <b>Подбор под бюджет: {budget:,} ₽</b>\nТип: {body_type} | Страна: {country}\n\n"

    for i, item in enumerate(results, 1):
        car = item["car"]

        if item["is_profitable"] is True:
            verdict = f"✅ <b>Ввозить выгодно</b> (экономия {item['difference']:,.0f} ₽)"
        elif item["is_profitable"] is False:
            verdict = f"❌ <b>Ввозить невыгодно</b> (в РФ дешевле на {abs(item['difference']):,.0f} ₽)"
        else:
            verdict = "⚠️ Нет данных о цене в РФ"

        over_line = ""
        if item.get("over_budget"):
            over_line = f"   • ⚠️ <i>Выше бюджета на {item['over_amount']:,.0f} ₽</i>\n"

        engine_type = car.get("engine_type", "ICE")
        if engine_type == "EV":
            engine_label = "⚡ Электро"
        elif engine_type == "HEV":
            engine_label = f"🔌 Гибрид, {car['engine_volume_cc']/1000:.1f} л"
        else:
            engine_label = f"{car['engine_volume_cc']/1000:.1f} л"

        text += (
            f"<b>{i}. {car['make']} {car['model']}</b> ({car['country']}, {car['year_from']}+)\n"
            f"   • {engine_label}, {car['engine_power_hp']} л.с.\n"
            f"   • Ввоз «под ключ»: <b>{item['total']:,.0f} ₽</b>\n"
            f"{over_line}"
        )

        if item["rf_price"]:
            text += f"   • Цена в РФ: ~{item['rf_price']:,} ₽\n"

        text += f"   • {verdict}\n\n"

    text += (
        "⚠️ <i>Расчёт по официальным формулам (ПП РФ № 1637, 1713, НК РФ). "
        f"Курс EUR ЦБ: {results[0]['eur_rub']:.2f} ₽.</i>\n\n"
        "📞 Хотите конкретный вариант и оформление? @nrzhnyi"
    )

    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu_kb())
    await state.clear()
