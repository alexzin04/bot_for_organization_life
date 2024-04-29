from aiogram.dispatcher.filters.state import StatesGroup,State

class finance_income_state(StatesGroup):
    Q1=State()
    Q2=State()
class finance_iconsumption_state(StatesGroup):
    Q1=State()
    Q2=State()

class finance_transfer_state(StatesGroup):
    Q1=State()

class finance_change_state(StatesGroup):
    Q1=State()