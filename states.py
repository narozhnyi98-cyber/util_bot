from aiogram.fsm.state import State, StatesGroup


class UtilForm(StatesGroup):
    category = State()
    importer = State()
    age = State()
    engine_volume = State()
    engine_power = State()