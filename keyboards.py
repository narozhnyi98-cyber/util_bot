from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚗 Рассчитать утильсбор")],
            [KeyboardButton(text="🚗 Подобрать авто под бюджет")],
            [KeyboardButton(text="💰 Стоит ли везти?")],
            [KeyboardButton(text="📩 Оформить под ключ")],
            [KeyboardButton(text="📞 Связаться со мной")]
        ],
        resize_keyboard=True
    )


def get_category_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Легковой"), KeyboardButton(text="Грузовой")],
            [KeyboardButton(text="Автобус"), KeyboardButton(text="Спецтехника")],
            [KeyboardButton(text="⬅️ В меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_importer_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Физическое лицо")],
            [KeyboardButton(text="Юридическое лицо")],
            [KeyboardButton(text="⬅️ В меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_age_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="До 3 лет")],
            [KeyboardButton(text="Старше 3 лет")],
            [KeyboardButton(text="⬅️ В меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_body_type_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Седан"), KeyboardButton(text="Кроссовер")],
            [KeyboardButton(text="Хэтчбек"), KeyboardButton(text="Универсал")],
            [KeyboardButton(text="Любой")],
            [KeyboardButton(text="⬅️ В меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_country_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Япония"), KeyboardButton(text="Корея")],
            [KeyboardButton(text="Китай"), KeyboardButton(text="Европа")],
            [KeyboardButton(text="Любая")],
            [KeyboardButton(text="⬅️ В меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_lead_cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отменить")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_lead_skip_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➡️ Пропустить")],
            [KeyboardButton(text="❌ Отменить")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
