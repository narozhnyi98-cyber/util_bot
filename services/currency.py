import logging
import time

import aiohttp

logger = logging.getLogger(__name__)

# Зеркало API ЦБ РФ (стабильное, отдаёт JSON)
CBR_API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

# Резервные курсы на случай, если ЦБ недоступен и кэш пуст
FALLBACK_RATES = {
    "EUR": 100.0,
    "USD": 90.0,
    "CNY": 12.0,
    "JPY": 0.6,
    "KRW": 0.07,
}

# Кэш курсов — обновляется раз в 6 часов
_cache = {
    "rates": {},
    "timestamp": 0,
}
CACHE_TTL = 6 * 60 * 60  # 6 часов в секундах


async def _fetch_rates() -> dict:
    """Загружает курсы с сайта ЦБ РФ."""
    async with aiohttp.ClientSession() as session:
        async with session.get(CBR_API_URL, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f"ЦБ API вернул статус {resp.status}")
            data = await resp.json()
            return data.get("Valute", {})


async def get_rates() -> dict:
    """
    Возвращает словарь курсов валют к рублю.
    Кэширует результат на 6 часов.
    """
    now = time.time()

    # Если кэш свежий — возвращаем его
    if now - _cache["timestamp"] < CACHE_TTL and _cache["rates"]:
        return _cache["rates"]

    try:
        valute = await _fetch_rates()
        rates = {}
        for code, info in valute.items():
            # Формат: {"Value": 100.5, "Nominal": 1} — курс уже в рублях
            # Или {"Value": 6.5, "Nominal": 100} — 100 единиц за X рублей
            rates[code] = info["Value"] / info["Nominal"]

        _cache["rates"] = rates
        _cache["timestamp"] = now
        logger.info(
            f"Курсы ЦБ обновлены: EUR={rates.get('EUR')}, "
            f"USD={rates.get('USD')}, CNY={rates.get('CNY')}"
        )
        return rates

    except Exception as e:
        logger.error(f"Не удалось загрузить курсы ЦБ: {e}")

        # Если кэш пуст — используем резервные курсы
        if not _cache["rates"]:
            logger.warning("Использую резервные курсы валют")
            _cache["rates"] = FALLBACK_RATES.copy()

        return _cache["rates"]


async def get_rate(currency: str) -> float:
    """Возвращает курс указанной валюты к рублю."""
    rates = await get_rates()
    return rates.get(currency, FALLBACK_RATES.get(currency, 0.0))


async def get_eur_rate() -> float:
    """Возвращает курс EUR → RUB."""
    return await get_rate("EUR")
