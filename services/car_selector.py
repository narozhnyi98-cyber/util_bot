import logging
from datetime import datetime

from services.currency import get_eur_rate

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# БАЗА АВТОМОБИЛЕЙ (встроена в код)
# ─────────────────────────────────────────────────────────────
CARS = [
    # Бюджетные (от 600 тыс.)
    {"id":1,"make":"Daihatsu","model":"Mira","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":660,"engine_power_hp":64,"price_foreign_rub":600000},
    {"id":2,"make":"Suzuki","model":"Alto","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":660,"engine_power_hp":64,"price_foreign_rub":620000},
    {"id":3,"make":"Toyota","model":"Vitz","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1000,"engine_power_hp":69,"price_foreign_rub":800000},
    {"id":4,"make":"Toyota","model":"Aqua","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":74,"price_foreign_rub":900000},
    {"id":5,"make":"Nissan","model":"Note","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":79,"price_foreign_rub":900000},
    {"id":6,"make":"Honda","model":"Fit","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1300,"engine_power_hp":98,"price_foreign_rub":950000},
    {"id":7,"make":"Mazda","model":"2","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1300,"engine_power_hp":93,"price_foreign_rub":950000},
    {"id":8,"make":"Suzuki","model":"Swift","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":83,"price_foreign_rub":1000000},
    {"id":9,"make":"Toyota","model":"Yaris","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":120,"price_foreign_rub":1100000},
    {"id":10,"make":"Kia","model":"Picanto","country":"Корея","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":84,"price_foreign_rub":800000},
    {"id":11,"make":"Hyundai","model":"i10","country":"Корея","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":84,"price_foreign_rub":850000},
    {"id":12,"make":"Kia","model":"Rio","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":123,"price_foreign_rub":1100000},
    {"id":13,"make":"Hyundai","model":"Solaris","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":123,"price_foreign_rub":1150000},
    {"id":14,"make":"Skoda","model":"Fabia","country":"Европа","body_type":"Хэтчбек","year_from":2020,"engine_volume_cc":1200,"engine_power_hp":110,"price_foreign_rub":1100000},
    {"id":15,"make":"Volkswagen","model":"Polo","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":125,"price_foreign_rub":1200000},
    {"id":16,"make":"Chery","model":"Tiggo 2","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":113,"price_foreign_rub":900000},

    # Средний сегмент
    {"id":17,"make":"Toyota","model":"Corolla","country":"Япония","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":122,"price_foreign_rub":1250000},
    {"id":18,"make":"Honda","model":"Vezel","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":131,"price_foreign_rub":1300000},
    {"id":19,"make":"Hyundai","model":"Elantra","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":128,"price_foreign_rub":1350000},
    {"id":20,"make":"Chery","model":"Tiggo 4","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1150000},
    {"id":21,"make":"Haval","model":"Jolion","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":143,"price_foreign_rub":1350000},
    {"id":22,"make":"Geely","model":"Coolray","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":177,"price_foreign_rub":1450000},
    {"id":23,"make":"Nissan","model":"Qashqai","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1300,"engine_power_hp":140,"price_foreign_rub":1450000},
    {"id":24,"make":"Skoda","model":"Octavia","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1500000},
    {"id":25,"make":"Chery","model":"Tiggo 7 Pro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1550000},
    {"id":26,"make":"Renault","model":"Arkana","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":150,"price_foreign_rub":1600000},
    {"id":27,"make":"Kia","model":"K5","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1650000},
    {"id":28,"make":"Mazda","model":"CX-5","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1750000},
    {"id":29,"make":"Kia","model":"Sportage","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1750000},
    {"id":30,"make":"Nissan","model":"X-Trail","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":149,"price_foreign_rub":1800000},
    {"id":31,"make":"Volkswagen","model":"Tiguan","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1850000},
    {"id":32,"make":"Hyundai","model":"Tucson","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1850000},
    {"id":33,"make":"Toyota","model":"Camry","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":181,"price_foreign_rub":1850000},
    {"id":34,"make":"Toyota","model":"RAV4","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":149,"price_foreign_rub":1950000},

    # Премиум
    {"id":35,"make":"Exeed","model":"TXL","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":197,"price_foreign_rub":2050000},
    {"id":36,"make":"Changan","model":"UNI-K","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":226,"price_foreign_rub":2000000},
    {"id":37,"make":"Kia","model":"Sorento","country":"Корея","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":2200000},
    {"id":38,"make":"Geely","model":"Monjaro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":238,"price_foreign_rub":2300000},
    {"id":39,"make":"Hyundai","model":"Santa Fe","country":"Корея","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":2300000},
    {"id":40,"make":"BMW","model":"3 series","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2500000},
    {"id":41,"make":"Mercedes","model":"C-class","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2600000},
    {"id":42,"make":"BMW","model":"X3","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2800000},
    {"id":43,"make":"Audi","model":"Q5","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":2900000},
    {"id":44,"make":"Genesis","model":"GV70","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":249,"price_foreign_rub":3200000},
    {"id":45,"make":"Toyota","model":"Highlander","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":249,"price_foreign_rub":3500000},
    {"id":46,"make":"Toyota","model":"Land Cruiser Prado","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2800,"engine_power_hp":177,"price_foreign_rub":3800000},
    {"id":47,"make":"Lexus","model":"NX","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":239,"price_foreign_rub":3800000},
    {"id":48,"make":"Lexus","model":"RX","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3500,"engine_power_hp":300,"price_foreign_rub":4200000},
    {"id":49,"make":"Toyota","model":"Alphard","country":"Япония","body_type":"Универсал","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":182,"price_foreign_rub":4000000},
    {"id":50,"make":"BMW","model":"5 series","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":249,"price_foreign_rub":3200000},
]


# ─────────────────────────────────────────────────────────────
# ЦЕНЫ В РФ
# ─────────────────────────────────────────────────────────────
RF_PRICES = {
    "Daihatsu|Mira": 850000,
    "Suzuki|Alto": 900000,
    "Toyota|Vitz": 1100000,
    "Toyota|Aqua": 1300000,
    "Nissan|Note": 1250000,
    "Honda|Fit": 1350000,
    "Mazda|2": 1300000,
    "Suzuki|Swift": 1450000,
    "Toyota|Yaris": 1500000,
    "Kia|Picanto": 1150000,
    "Hyundai|i10": 1200000,
    "Kia|Rio": 1550000,
    "Hyundai|Solaris": 1600000,
    "Skoda|Fabia": 1500000,
    "Volkswagen|Polo": 1550000,
    "Chery|Tiggo 2": 1300000,

    "Toyota|Corolla": 1850000,
    "Honda|Vezel": 1900000,
    "Hyundai|Elantra": 1950000,
    "Chery|Tiggo 4": 1700000,
    "Haval|Jolion": 1900000,
    "Geely|Coolray": 2100000,
    "Nissan|Qashqai": 2200000,
    "Skoda|Octavia": 2200000,
    "Chery|Tiggo 7 Pro": 2200000,
    "Renault|Arkana": 2200000,
    "Kia|K5": 2300000,
    "Mazda|CX-5": 3800000,
    "Kia|Sportage": 3200000,
    "Nissan|X-Trail": 2500000,
    "Volkswagen|Tiguan": 2700000,
    "Hyundai|Tucson": 3900000,
    "Toyota|Camry": 3800000,
    "Toyota|RAV4": 2750000,

    "Exeed|TXL": 3300000,
    "Changan|UNI-K": 2700000,
    "Kia|Sorento": 3400000,
    "Geely|Monjaro": 3500000,
    "Hyundai|Santa Fe": 2850000,
    "BMW|3 series": 3900000,
    "Mercedes|C-class": 4100000,
    "BMW|X3": 7100000,
    "Audi|Q5": 4200000,
    "Genesis|GV70": 4100000,
    "Toyota|Highlander": 4500000,
    "Toyota|Land Cruiser Prado": 4500000,
    "Lexus|NX": 4200000,
    "Lexus|RX": 4500000,
    "Toyota|Alphard": 6000000,
    "BMW|5 series": 4500000,
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

DUTY_NEW = [
    (325_000, 0.54, 2.5),
    (650_000, 0.48, 3.5),
    (1_625_000, 0.48, 5.5),
    (3_250_000, 0.48, 7.5),
    (6_500_000, 0.48, 15.0),
    (float('inf'), 0.48, 20.0),
]

DUTY_3_5 = [
    (1_000, 1.5), (1_500, 1.7), (1_800, 2.5),
    (2_300, 2.7), (3_000, 3.0), (float('inf'), 3.6),
]

DUTY_5_PLUS = [
    (1_000, 3.0), (1_500, 3.2), (1_800, 3.5),
    (2_300, 4.8), (3_000, 5.0), (float('inf'), 5.7),
]

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
    return CARS


def get_rf_price(make: str, model: str) -> int | None:
    return RF_PRICES.get(f"{make}|{model}")


# ─────────────────────────────────────────────────────────────
# РАСЧЁТНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────────

def calculate_customs_fee(price_rub: int) -> int:
    for limit, fee in CUSTOMS_FEE_TIERS:
        if price_rub <= limit:
            return fee
    return CUSTOMS_FEE_TIERS[-1][1]


def calculate_duty(price_rub: int, volume_cc: int, age_years: int, eur_rub: float) -> float:
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
    table = UTIL_COEF_NEW if age_years < 3 else UTIL_COEF_OLD
    for max_power, coef in table:
        if power_hp <= max_power:
            return UTIL_BASE_RATE * coef
    return UTIL_BASE_RATE * table[-1][1]


def calculate_total_expenses(country: str) -> int:
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
    Подбирает автомобили под бюджет с учётом всех расходов
    и сравнением с ценой в РФ.
    Показывает машины до budget × 1.5 с пометкой «выше бюджета».
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

        # Показываем машины до 1.5× бюджета
        if total <= budget * 1.5:
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
                "over_budget": total > budget,
                "over_amount": max(0, total - budget),
            })

    # Сортировка: сначала влезающие в бюджет, потом по выгоде
    def sort_key(x):
        # 0 — в бюджете, 1 — выше бюджета
        bucket = 1 if x["over_budget"] else 0
        if x["difference"] is None:
            return (bucket, 2, x["total"])
        if x["difference"] > 0:
            return (bucket, 0, -x["difference"])
        return (bucket, 1, x["total"])

    results.sort(key=sort_key)
    return results[:7]
