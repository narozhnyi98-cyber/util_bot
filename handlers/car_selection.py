import logging
from datetime import datetime

from services.currency import get_eur_rate

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# БАЗА АВТОМОБИЛЕЙ (добавлены электромобили и гибриды)
# ─────────────────────────────────────────────────────────────
CARS = [
    # ... (все существующие машины с ДВС, у них engine_type="ICE") ...
    # Примеры (полный список нужно дополнить):
    {"id":1,"make":"Toyota","model":"Corolla","country":"Япония","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":122,"price_foreign_rub":1250000,"engine_type":"ICE"},
    # ... (остальные машины с ДВС) ...

    # Электромобили и гибриды
    {"id":200,"make":"Zeekr","model":"001","country":"Китай","body_type":"Седан","year_from":2022,"engine_volume_cc":0,"engine_power_hp":544,"price_foreign_rub":3500000,"engine_type":"EV"},
    {"id":201,"make":"Voyah","model":"Free","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":0,"engine_power_hp":694,"price_foreign_rub":3500000,"engine_type":"EV"},
    {"id":202,"make":"Tesla","model":"Model 3","country":"Европа","body_type":"Седан","year_from":2021,"engine_volume_cc":0,"engine_power_hp":283,"price_foreign_rub":3200000,"engine_type":"EV"},
    {"id":203,"make":"Tesla","model":"Model Y","country":"Европа","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":0,"engine_power_hp":331,"price_foreign_rub":3800000,"engine_type":"EV"},
    {"id":204,"make":"BYD","model":"Song Plus","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":0,"engine_power_hp":218,"price_foreign_rub":2200000,"engine_type":"EV"},
    {"id":205,"make":"Li Auto","model":"L7","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":449,"price_foreign_rub":3500000,"engine_type":"HEV"},
    # ... добавь другие электромобили ...

]


# ─────────────────────────────────────────────────────────────
# ЦЕНЫ В РФ (добавлены цены на электромобили)
# ─────────────────────────────────────────────────────────────
RF_PRICES = {
    # ... (существующие цены) ...
    "Zeekr|001": 5000000,
    "Voyah|Free": 5000000,
    "Tesla|Model 3": 4500000,
    "Tesla|Model Y": 5000000,
    "BYD|Song Plus": 3500000,
    "Li Auto|L7": 5500000,
    # ... добавь другие ...
}


# ─────────────────────────────────────────────────────────────
# РАСХОДЫ (без изменений)
# ─────────────────────────────────────────────────────────────
EXPENSES = { ... }


# ─────────────────────────────────────────────────────────────
# ОФИЦИАЛЬНЫЕ ТАБЛИЦЫ
# ─────────────────────────────────────────────────────────────

CUSTOMS_FEE_TIERS = [ ... ]  # без изменений

# Пошлина для авто ДО 3 лет: (макс. стоимость, процент, мин. €/см³)
DUTY_NEW = [ ... ]  # без изменений
DUTY_3_5 = [ ... ]  # без изменений
DUTY_5_PLUS = [ ... ]  # без изменений


# ─── КОЭФФИЦИЕНТЫ УТИЛЬСБОРА (ОБНОВЛЕНЫ ДЛЯ ЭЛЕКТРО) ───

# Для обычных авто (ДВС) с мощностью до 160 л.с.
UTIL_COEF_ICE_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_ICE_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]

# Для электромобилей и последовательных гибридов с мощностью до 80 л.с.
UTIL_COEF_EV_NEW = [
    (80, 0.17),   # Льготный
    (9999, 15.73), # Коммерческий (коэффициент 15.73)
]
UTIL_COEF_EV_OLD = [
    (80, 0.26),   # Льготный
    (9999, 15.73), # Коммерческий
]

# Для гибридов (мощность считается суммарно) с мощностью до 160 л.с.
UTIL_COEF_HEV_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_HEV_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]

UTIL_BASE_RATE = 20000


# ─────────────────────────────────────────────────────────────
# ФУНКЦИИ
# ─────────────────────────────────────────────────────────────

def load_cars() -> list:
    return CARS

def get_rf_price(make: str, model: str) -> int | None:
    return RF_PRICES.get(f"{make}|{model}")


def calculate_customs_fee(price_rub: int) -> int:
    # ... без изменений ...

def calculate_duty(price_rub: int, volume_cc: int, age_years: int, eur_rub: float) -> float:
    # ... без изменений ...

# ⚡ ОБНОВЛЁННАЯ ФУНКЦИЯ РАСЧЁТА УТИЛЬСБОРА
def calculate_util(engine_power_hp: int, age_years: int, engine_type: str = "ICE") -> float:
    """
    Утильсбор для физлица.
    Учитывает тип двигателя (ICE, EV, HEV) и выбирает правильный порог мощности.
    """
    if engine_type == "EV":
        table = UTIL_COEF_EV_NEW if age_years < 3 else UTIL_COEF_EV_OLD
    elif engine_type == "HEV":
        table = UTIL_COEF_HEV_NEW if age_years < 3 else UTIL_COEF_HEV_OLD
    else: # "ICE"
        table = UTIL_COEF_ICE_NEW if age_years < 3 else UTIL_COEF_ICE_OLD

    for max_power, coef in table:
        if engine_power_hp <= max_power:
            return UTIL_BASE_RATE * coef
    return UTIL_BASE_RATE * table[-1][1]


def calculate_total_expenses(country: str) -> int:
    # ... без изменений ...


# ─────────────────────────────────────────────────────────────
# ГЛАВНАЯ ФУНКЦИЯ ПОДБОРА (ОБНОВЛЕНА)
# ─────────────────────────────────────────────────────────────

async def select_cars(budget: int, body_type: str, country: str) -> list:
    cars = load_cars()
    current_year = datetime.now().year
    results = []

    eur_rub = await get_eur_rate()

    for car in cars:
        if body_type != "Любой" and car["body_type"] != body_type:
            continue
        if country != "Любая" and car["country"] != country:
            continue

        age_years = current_year - car["year_from"]
        
        # ⚡ Учитываем тип двигателя
        engine_type = car.get("engine_type", "ICE")
        
        # Для гибридов и электро объем может быть 0
        volume_cc = car.get("engine_volume_cc", 0)

        # ⚡ Передаём engine_type в calculate_util
        util = calculate_util(car["engine_power_hp"], age_years, engine_type)
        
        duty = calculate_duty(
            car["price_foreign_rub"],
            volume_cc,
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

    def sort_key(x):
        bucket = 1 if x["over_budget"] else 0
        if x["difference"] is None:
            return (bucket, 2, x["total"])
        if x["difference"] > 0:
            return (bucket, 0, -x["difference"])
        return (bucket, 1, x["total"])

    results.sort(key=sort_key)
    return results[:7]
