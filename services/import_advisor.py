import logging
from datetime import datetime

from services.car_selector import (
    get_rf_price,
    calculate_util,
    calculate_duty,
    calculate_customs_fee,
    calculate_total_expenses,
)
from services.currency import get_eur_rate

logger = logging.getLogger(__name__)


async def compare_import(car: dict) -> dict | None:
    """Считает ввоз «под ключ» и сравнивает с ценой в РФ."""
    current_year = datetime.now().year
    age_years = current_year - car["year_from"]

    eur_rub = await get_eur_rate()

    util = calculate_util(car["engine_power_hp"], age_years)
    duty = calculate_duty(
        car["price_foreign_rub"],
        car["engine_volume_cc"],
        age_years,
        eur_rub,
    )
    customs_fee = calculate_customs_fee(car["price_foreign_rub"])
    expenses = calculate_total_expenses(car["country"])

    total_import = (
        car["price_foreign_rub"]
        + duty
        + util
        + customs_fee
        + expenses
    )

    rf_price = get_rf_price(car["make"], car["model"])
    if rf_price is None:
        return None

    difference = rf_price - total_import

    return {
        "car": car,
        "age_years": age_years,
        "eur_rub": eur_rub,
        "price_foreign": car["price_foreign_rub"],
        "duty": duty,
        "util": util,
        "customs_fee": customs_fee,
        "expenses": expenses,
        "total_import": total_import,
        "rf_price": rf_price,
        "difference": difference,
        "is_profitable": difference > 0,
    }
