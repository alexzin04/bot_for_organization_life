from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db_api.sport_db import get_all_workouts,get_workouts,get_all_exsersize

sport_keyboard= InlineKeyboardMarkup(row_width=1)
income=InlineKeyboardButton(text='Записать новую тренировку', callback_data='new_sport')
sport_keyboard.insert(income)
consumption=InlineKeyboardButton(text='Посмотреть прошлые тренировки',callback_data='look_last_sport')
sport_keyboard.insert(consumption)
finance_data=InlineKeyboardButton(text='Доп Функции',callback_data='sport_data')
sport_keyboard.row(finance_data)
back_1=InlineKeyboardButton(text='назад',callback_data='start')
sport_keyboard.row(back_1)

sport_data_keyboard=InlineKeyboardMarkup(row_width=1)
income=InlineKeyboardButton(text='Создать новую программу', callback_data='new_plan_sport')
sport_data_keyboard.insert(income)
finance_data=InlineKeyboardButton(text='Добавить новое упражнение',callback_data='new_exsersize_sport')
sport_data_keyboard.row(finance_data)
back_1=InlineKeyboardButton(text='назад',callback_data='sport')
sport_data_keyboard.row(back_1)

def new_keyboard():
    a=get_all_workouts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'workouts_name_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='sport')
    keyboard.insert(cancel)
    return keyboard
def new_keyboard_2(id:int,flag:bool=False):
    a=get_workouts(id)
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id_2=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'workouts_exers_{id_2}')
        keyboard.insert(add_new)
    if flag:
        add_new=InlineKeyboardButton(text='Завершить тренировку?',callback_data=f'workouts_finish')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='new_sport')
    keyboard.insert(cancel)
    return keyboard

def new_keyboard_3(mas:list,tren_id:int,exer_id:int,index:int):
    keyboard=InlineKeyboardMarkup(row_width=1)
    k=0
    for i in mas[index]:
        add_new=InlineKeyboardButton(text=i,callback_data=f'workouts_level_{k}')
        keyboard.insert(add_new)
        k+=1
    add_new=InlineKeyboardButton(text='Добавить новый подход',callback_data=f'workouts_add_level_{len(mas[index])}')
    keyboard.insert(add_new)  
    cancel=InlineKeyboardButton(text='Назад',callback_data=f'workouts_name_{tren_id}_1')
    keyboard.insert(cancel)
    return keyboard

sport_history_keyboard=InlineKeyboardMarkup(row_width=1)
one_day=InlineKeyboardMarkup(text='за сегодня',callback_data='history_sport_time_0')
one_week=InlineKeyboardMarkup(text='за последние 7 дней',callback_data='history_sport_time_7')
one_month=InlineKeyboardMarkup(text='за послдение 30 дней',callback_data='history_sport_time_30')
cancel=InlineKeyboardButton(text='Назад',callback_data='sport')
sport_history_keyboard.add(one_day)
sport_history_keyboard.add(one_week)
sport_history_keyboard.add(one_month)
sport_history_keyboard.add(cancel)


def new_keyboard_5(b:list):
    a=get_all_exsersize()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        if id in b:
            continue
        add_new=InlineKeyboardButton(text=text,callback_data=f'new_sport_program_{id}')
        keyboard.insert(add_new)
    if len(b)!=0:
        add_new=InlineKeyboardButton(text='Закончить с созданием программы?',callback_data=f'finish_new_sport_program')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='sport_data')
    keyboard.insert(cancel)
    return keyboard

sport_yes_no_keyboard=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='sport_yes_1')
no=InlineKeyboardButton(text='Нет',callback_data='sport_no_1')
sport_yes_no_keyboard.add(yes)
sport_yes_no_keyboard.add(no)
