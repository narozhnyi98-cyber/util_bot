import json
import logging
from datetime import datetime
from pathlib import Path

from services.currency import get_eur_rate

logger = logging.getLogger(__name__)

CARS_FILE = Path(__file__).parent.parent / "data" / "cars.json"
RF_PRICES_FILE = Path(__file__).parent.parent / "data" / "rf_prices.json"

# Расходы на оформление и логистику (обновлять по мере изменения цен)
EXPENSES = {
    "СБКТС": 25000,
    "ЭПТС": 5000,
    "ГЛОНАСС": 15000,
    "Логистика Япония": 100000,
    "Логистика Корея": 100000,
    "Логистика Китай": 120000,
    "Логистика Европа": 200000,
    "Брокер": 35000,
}

# Сбор за таможенное оформление (ПП РФ № 1637)
CUSTOMS_FEE_TIERS = [
    (200_000, 1_231),
    (450_000, 2_462),
    (1_200_000, 4_924),
    (2_700_000, 13_541),
    (4_200_000, 18_465),
    (5_500_000, 21_344),
    (10_000_000, 49_240),
    (float('inf'), 73_860),
]

# Пошлина для авто ДО 3 лет: (макс. стоимость, процент, мин. €/см³)
DUTY_NEW = [
    (325_000, 0.54, 2.5),
    (650_000, 0.48, 3.5),
    (1_625_000, 0.48, 5.5),
    (3_250_000, 0.48, 7.5),
    (6_500_000, 0.48, 15.0),
    (float('inf'), 0.48, 20.0),
]

# Пошлина для авто 3–5 лет: (макс. объём, €/см³)
DUTY_3_5 = [
    (1_000, 1.5), (1_500, 1.7), (1_800, 2.5),
    (2_300, 2.7), (3_000, 3.0), (float('inf'), 3.6),
]

# Пошлина для авто старше 5 лет: (макс. объём, €/см³)
DUTY_5_PLUS = [
    (1_000, 3.0), (1_500, 3.2), (1_800, 3.5),
    (2_300, 4.8), (3_000, 5.0), (float('inf'), 5.7),
]

# Коэффициенты утильсбора (ПП РФ № 1713), физлица, легковые
UTIL_COEF_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]
UTIL_BASE_RATE = 20000


def load_cars() -> list:
    with open(CARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_rf_prices() -> dict:
    with open(RF_PRICES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_rf_price(make: str, model: str) -> int | None:
    """Возвращает среднюю цену модели в РФ или None."""
    return load_rf_prices().get(f"{make}|{model}")


def calculate_customs_fee(price_rub: int) -> int:
    """Сбор за таможенное оформление."""
    for limit, fee in CUSTOMS_FEE_TIERS:
        if price_rub <= limit:
            return fee
    return CUSTOMS_FEE_TIERS[-1][1]


def calculate_duty(price_rub: int, volume_cc: int, age_years: int, eur_rub: float) -> float:
    """Таможенная пошлина по единой ставке (в рублях)."""
    if age_years < 3:
        for limit, percent, min_eur in DUTY_NEW:
            if price_rub <= limit:
                return max(price_rub * percent, min_eur * volume_cc * eur_rub)
        return price_rub * 0.48

    if age_years <= 5:
        for limit, rate in DUTY_3_5:
            if volume_cc <= limit:
                return rate * volume_cc * eur_rub
        return DUTY_3_5[-1][1] * volume_cc * eur_rub

    for limit, rate in DUTY_5_PLUS:
        if volume_cc <= limit:
            return rate * volume_cc * eur_rub
    return DUTY_5_PLUS[-1][1] * volume_cc * eur_rub


def calculate_util(power_hp: int, age_years: int) -> float:
    """Утильсбор для физлица (легковой)."""
    table = UTIL_COEF_NEW if age_years < 3 else UTIL_COEF_OLD
    for max_power, coef in table:
        if power_hp <= max_power:
            return UTIL_BASE_RATE * coef
    return UTIL_BASE_RATE * table[-1][1]


def calculate_total_expenses(country: str) -> int:
    """Стоимость оформления и логистики."""
    logistics_key = f"Логистика {country}"
    logistics = EXPENSES.get(logistics_key, 120_000)
    return (
        EXPENSES["СБКТС"]
        + EXPENSES["ЭПТС"]
        + EXPENSES["ГЛОНАСС"]
        + logistics
        + EXPENSES["Брокер"]
    )


async def select_cars(budget: int, body_type: str, country: str) -> list:
    """
    Подбирает автомобили под бюджет с актуальным курсом EUR
    и сравнением с ценой в РФ.
    """
    cars = load_cars()
    current_year = datetime.now().year
    results = []

    eur_rub = await get_eur_rate()
    logger.info(f"Курс EUR для расчёта: {eur_rub:.2f} ₽")

    for car in cars:
        if body_type != "Любой" and car["body_type"] != body_type:
            continue
        if country != "Любая" and car["country"] != country:
            continue

        age_years = current_year - car["year_from"]

        util = calculate_util(car["engine_power_hp"], age_years)
        duty = calculate_duty(
            car["price_foreign_rub"],
            car["engine_volume_cc"],
            age_years,
            eur_rub,
        )
        customs_fee = calculate_customs_fee(car["price_foreign_rub"])
        expenses = calculate_total_expenses(car["country"])

        total = car["price_foreign_rub"] + duty + util + customs_fee + expenses

        # Сравнение с ценой в РФ
        rf_price = get_rf_price(car["make"], car["model"])
        if rf_price is not None:
            difference = rf_price - total
            is_profitable = difference > 0
        else:
            difference = None
            is_profitable = None

        if total <= budget * 1.05:
            results.append({
                "car": car,
                "total": total,
                "util": util,
                "duty": duty,
                "customs_fee": customs_fee,
                "expenses": expenses,
                "age_years": age_years,
                "eur_rub": eur_rub,
                "rf_price": rf_price,
                "difference": difference,
                "is_profitable": is_profitable,
            })

    # Сортировка: сначала выгодные для ввоза, потом остальные
    def sort_key(x):
        if x["difference"] is None:
            return (2, x["total"])
        if x["difference"] > 0:
            return (0, -x["difference"])
        return (1, x["total"])

    results.sort(key=sort_key)
    return results[:5]
