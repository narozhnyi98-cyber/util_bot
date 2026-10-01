import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

CARS_FILE = Path(__file__).parent.parent / "data" / "cars.json"

# Курс валют (обновлять раз в неделю по данным ЦБ РФ)
EUR_RUB = 100.0
# Официальный таможенный курс может отличаться — нужно смотреть на сайте ФТС

# Расходы на оформление "под ключ" (реальные средние цены услуг 2026)
EXPENSES = {
    "СБКТС": 25000,
    "ЭПТС": 5000,
    "ГЛОНАСС": 15000,
    "Логистика Япония/Корея": 100000,
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
DUTY_3_5 = [(1_000,1.5),(1_500,1.7),(1_800,2.5),(2_300,2.7),(3_000,3.0),(float('inf'),3.6)]

# Пошлина для авто старше 5 лет: (макс. объём, €/см³)
DUTY_5_PLUS = [(1_000,3.0),(1_500,3.2),(1_800,3.5),(2_300,4.8),(3_000,5.0),(float('inf'),5.7)]

# Коэффициенты утильсбора для физлиц (ПП РФ № 1713) — легковые
UTIL_COEF_NEW = [  # До 3 лет
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_OLD = [  # Старше 3 лет
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]
UTIL_BASE_RATE = 20000  # Для легковых


def load_cars() -> list:
    with open(CARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_customs_fee(price_rub: int) -> int:
    """Сбор за таможенное оформление."""
    for limit, fee in CUSTOMS_FEE_TIERS:
        if price_rub <= limit:
            return fee
    return CUSTOMS_FEE_TIERS[-1][1]


def calculate_duty(price_rub: int, volume_cc: int, age_years: int) -> float:
    """Таможенная пошлина по единой ставке (в рублях)."""
    if age_years < 3:
        for limit, percent, min_eur in DUTY_NEW:
            if price_rub <= limit:
                return max(price_rub * percent, min_eur * volume_cc * EUR_RUB)
        return price_rub * 0.48

    if age_years <= 5:
        for limit, rate in DUTY_3_5:
            if volume_cc <= limit:
                return rate * volume_cc * EUR_RUB
        return DUTY_3_5[-1][1] * volume_cc * EUR_RUB

    for limit, rate in DUTY_5_PLUS:
        if volume_cc <= limit:
            return rate * volume_cc * EUR_RUB
    return DUTY_5_PLUS[-1][1] * volume_cc * EUR_RUB


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
    logistics = EXPENSES.get(logistics_key, 120000)
    return (
        EXPENSES["СБКТС"]
        + EXPENSES["ЭПТС"]
        + EXPENSES["ГЛОНАСС"]
        + logistics
        + EXPENSES["Брокер"]
    )


def select_cars(budget: int, body_type: str, country: str) -> list:
    cars = load_cars()
    current_year = datetime.now().year
    results = []

    for car in cars:
        if body_type != "Любой" and car["body_type"] != body_type:
            continue
        if country != "Любая" and car["country"] != country:
            continue

        age_years = current_year - car["year_from"]

        util = calculate_util(car["engine_power_hp"], age_years)
        duty = calculate_duty(car["price_foreign_rub"], car["engine_volume_cc"], age_years)
        customs_fee = calculate_customs_fee(car["price_foreign_rub"])
        expenses = calculate_total_expenses(car["country"])

        total = car["price_foreign_rub"] + duty + util + customs_fee + expenses

        if total <= budget * 1.05:
            results.append({
                "car": car,
                "total": total,
                "util": util,
                "duty": duty,
                "customs_fee": customs_fee,
                "expenses": expenses,
                "age_years": age_years,
            })

    results.sort(key=lambda x: x["total"])
    return results[:5]
