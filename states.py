from aiogram.fsm.state import State, StatesGroup


class UtilForm(StatesGroup):
    engine_type = State()
    category = State()
    importer = State()
    age = State()
    engine_volume = State()
    engine_power = State()


class CarSelectionForm(StatesGroup):
    budget = State()
    body_type = State()
    country = State()


class LeadForm(StatesGroup):
    name = State()
    phone = State()
    comment = State()
