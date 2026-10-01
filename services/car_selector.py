import json
import logging
from datetime import datetime
from pathlib import Path

from services.currency import get_eur_rate

logger = logging.getLogger(__name__)

CARS_FILE = Path(__file__).parent.parent / "data" / "cars.json"
RF_PRICES_FILE = Path(__file__).parent.parent / "data" / "rf_prices.json"

# Расходы на оформление и логистику (обновлять по мере изменения цен на услуги)
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
