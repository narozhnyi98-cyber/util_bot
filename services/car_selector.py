import logging
from datetime import datetime

from services.currency import get_eur_rate

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# БАЗА АВТОМОБИЛЕЙ (встроена в код, чтобы не терялась на сервере)
# ─────────────────────────────────────────────────────────────
CARS = [
    {"id":1,"make":"Toyota","model":"Corolla","country":"Япония","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":122,"price_foreign_rub":1250000},
    {"id":2,"make":"Honda","model":"Vezel","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":131,"price_foreign_rub":1300000},
    {"id":3,"make":"Toyota","model":"RAV4","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":149,"price_foreign_rub":1950000},
    {"id":4,"make":"Mazda","model":"CX-5","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1750000},
    {"id":5,"make":"Nissan","model":"X-Trail","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":149,"price_foreign_rub":1800000},
    {"id":6,"make":"Toyota","model":"Camry","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":181,"price_foreign_rub":1850000},
    {"id":7,"make":"Hyundai","model":"Elantra","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":128,"price_foreign_rub":1350000},
    {"id":8,"make":"Kia","model":"K5","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1650000},
    {"id":9,"make":"Kia","model":"Sportage","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1750000},
    {"id":10,"make":"Hyundai","model":"Tucson","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1850000},
    {"id":11,"make":"Renault","model":"Arkana","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":150,"price_foreign_rub":1600000},
    {"id":12,"make":"Skoda","model":"Octavia","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1500000},
    {"id":13,"make":"Volkswagen","model":"Tiguan","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1850000},
    {"id":14,"make":"Nissan","model":"Qashqai","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1300,"engine_power_hp":140,"price_foreign_rub":1450000},
    {"id":15,"make":"BMW","model":"3 series","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2500000},
    {"id":16,"make":"Mercedes","model":"C-class","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2600000},
    {"id":17,"make":"Chery","model":"Tiggo 4","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1150000},
    {"id":18,"make":"Chery","model":"Tiggo 7 Pro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1550000},
    {"id":19,"make":"Haval","model":"Jolion","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":143,"price_foreign_rub":1350000},
    {"id":20,"make":"Geely","model":"Coolray","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":177,"price_foreign_rub":1450000},
    {"id":21,"make":"Geely","model":"Monjaro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":238,"price_foreign_rub":2300000},
    {"id":22,"make":"Exeed","model":"TXL","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":197,"price_foreign_rub":2050000},
    {"id":23,"make":"Kia","model":"Sorento","country":"Корея","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":2200000},
    {"id":24,"make":"Toyota","model":"Land Cruiser Prado","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2800,"engine_power_hp":177,"price_foreign_rub":3800000},
    {"id":25,"make":"Lexus","model":"RX","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3500,"engine_power_hp":300,"price_foreign_rub":4200000},
]


# ─────────────────────────────────────────────────────────────
# ЦЕНЫ В РФ (встроены в код)
# ─────────────────────────────────────────────────────────────
RF_PRICES = {
    "Toyota|Corolla": 1850000,
    "Honda|Vezel": 1900000,
    "Toyota|RAV4": 2750000,
    "Mazda|CX-5": 3800000,
    "Nissan|X-Trail": 2500000,
    "Toyota|Camry": 3800000,
    "Hyundai|Elantra": 1950000,
    "Kia|K5": 2300000,
    "Kia|Sportage": 3200000,
    "Hyundai|Tucson": 3900000,
    "Renault|Arkana": 2200000,
    "Skoda|Octavia": 2200000,
    "Volkswagen|Tiguan": 2700000,
    "Nissan|Qashqai": 2200000,
    "BMW|3 series": 3900000,
    "Mercedes|C-class": 4100000,
    "Chery|Tiggo 4": 1700000,
    "Chery|Tiggo 7 Pro": 2200000,
    "Haval|Jolion": 1900000,
    "Geely|Coolray": 2100000,
    "Geely|Monjaro": 3500000,
    "Exeed|TXL": 3300000,
    "Kia|Sorento": 3400000,
    "Toyota|Land Cruiser Prado": 4500000,
    "Lexus|RX": 4500000,
}


# ─────────────────────────────────────────────────────────────
# РАСХОДЫ НА ОФОРМЛЕНИЕ И ЛОГИСТИКУ
# ─────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────
# ОФИЦИАЛЬНЫЕ ТАБЛИЦЫ (ПП РФ № 1637, № 1713)
# ─────────────────────────────────────────────────────────────

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

# Коэффициенты утильсбора для физлиц (ПП РФ № 1713)
UTIL_COEF_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]
UTIL_BASE_RATE = 20000


# ─────────────────────────────────────────────────────────────
# ФУНКЦИИ ДОСТУПА К БАЗЕ
# ─────────────────────────────────────────────────────────────

def load_cars() -> list:
    """Возвращает базу автомобилей."""
    return CARS


def get_rf_price(make: str, model: str) -> int | None:
    """Возвращает среднюю цену модели в РФ или None."""
    return RF_PRICES.get(f"{make}|{model}")


# ─────────────────────────────────────────────────────────────
# РАСЧЁТНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────
# ГЛАВНАЯ ФУНКЦИЯ ПОДБОРА
# ─────────────────────────────────────────────────────────────

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

    def sort_key(x):
        if x["difference"] is None:
            return (2, x["total"])
        if x["difference"] > 0:
            return (0, -x["difference"])
        return (1, x["total"])

    results.sort(key=sort_key)
    return results[:5]
