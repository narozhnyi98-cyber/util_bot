from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚗 Рассчитать утильсбор")],
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