from aiogram.dispatcher.filters.state import StatesGroup,State

class task_add_state(StatesGroup):
    Q1=State()
    Q2=State()
    Q3=State()

class task_reg_add_state(StatesGroup):
    Q1=State()
    Q2=State()

class every_day_challenge_state(StatesGroup):
    Q1=State()

class add_every_day_challenge_state(StatesGroup):
    Q1=State()
    Q2=State()
    Q3=State()
    Q4=State()