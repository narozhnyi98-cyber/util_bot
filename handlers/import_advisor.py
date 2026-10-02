import logging
from datetime import datetime

from services.car_selector import (
    get_rf_price, calculate_util, calculate_duty,
    calculate_customs_fee, calculate_total_expenses,
    calculate_excise, NDS_RATE,
)
from services.currency import get_eur_rate

logger = logging.getLogger(__name__)


async def compare_import(car: dict) -> dict | None:
    current_year = datetime.now().year
    age_years = current_year - car["year_from"]
    eur_rub = await get_eur_rate()

    engine_type = car.get("engine_type", "ICE")
    volume_cc = car.get("engine_volume_cc", 0)

    util = calculate_util(car["engine_power_hp"], age_years, engine_type)
    duty = calculate_duty(car["price_foreign_rub"], volume_cc, age_years, eur_rub)
    customs_fee = calculate_customs_fee(car["price_foreign_rub"])
    expenses = calculate_total_expenses(car["country"])

    excise = 0
    nds = 0
    if engine_type in ("EV", "HEV"):
        excise = calculate_excise(car["engine_power_hp"])
        nds = (car["price_foreign_rub"] + duty + excise) * NDS_RATE

    total_import = (
        car["price_foreign_rub"] + duty + util + customs_fee
        + expenses + excise + nds
    )

    rf_price = get_rf_price(car["make"], car["model"])
    if rf_price is None:
        return None

    difference = rf_price - total_import

    return {
        "car": car, "age_years": age_years, "eur_rub": eur_rub,
        "price_foreign": car["price_foreign_rub"],
        "duty": duty, "util": util, "customs_fee": customs_fee,
        "expenses": expenses, "excise": excise, "nds": nds,
        "total_import": total_import, "rf_price": rf_price,
        "difference": difference, "is_profitable": difference > 0,
        "engine_type": engine_type,
    }
