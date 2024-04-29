from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.tasks_db import get_task_for_time,get_all_every_day_challenge

def create_task_keyboard():
    task_keyboard= InlineKeyboardMarkup(row_width=1)
    income=InlineKeyboardButton(text='Задачи на сегодня', callback_data='tasks_today')
    task_keyboard.insert(income)
    consumption=InlineKeyboardButton(text='Задачи на неделю',callback_data='tasks_for_week')
    task_keyboard.insert(consumption)
    if len(get_all_every_day_challenge())!=0:
        finance_data=InlineKeyboardButton(text='Ежедневные вызовы',callback_data='every_day_challenge')
        task_keyboard.row(finance_data)
    finance_data=InlineKeyboardButton(text='Доп Функции',callback_data='additional_func')
    task_keyboard.row(finance_data)
    back_1=InlineKeyboardButton(text='назад',callback_data='start')
    task_keyboard.row(back_1)
    return task_keyboard

def create_tasks_today_keyboard():
    task_keyboard= InlineKeyboardMarkup(row_width=1)
    mas=list(get_task_for_time().values())
    if len(mas)!=0:
        mas=mas[0]
        for i in mas:
            task_keyboard.insert(InlineKeyboardButton(text=i[0]+(' ' if i[2]=='None' else f'({i[2]})'),callback_data=f'task_{i[1]}'))
    task_keyboard.insert(InlineKeyboardButton(text="Добавить новые задачи",callback_data="add_new_tasks"))
    task_keyboard.insert(InlineKeyboardButton(text="Назад",callback_data="tasks"))
    return task_keyboard

tasks_yes_no_keyborad=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='да',callback_data='tasks_yes')
no=InlineKeyboardButton(text='нет',callback_data='tasks_today')   
tasks_yes_no_keyborad.insert(yes)
tasks_yes_no_keyborad.insert(no)

add_new_task_keybiard=InlineKeyboardMarkup(row_width=1)
once=InlineKeyboardButton(text='Единоразово',callback_data='tasks_add_once')
reg=InlineKeyboardButton(text='Регулярно',callback_data='tasks_add_reg')
back=InlineKeyboardButton(text='Назад',callback_data="tasks")
add_new_task_keybiard.insert(once)
add_new_task_keybiard.insert(reg)
add_new_task_keybiard.insert(back)

reg_task_keyboard=InlineKeyboardMarkup(row_width=1)
once_month=InlineKeyboardButton(text='раз в месяц',callback_data='tasks_reg_once/month')
days_of_week=InlineKeyboardButton(text='в опредленый день недели',callback_data='tasks_days_of_week')
every_day=InlineKeyboardButton(text='каждый день',callback_data='tasks_reg_every/day')
back=InlineKeyboardButton(text='Назад',callback_data="add_new_tasks")
reg_task_keyboard.insert(once_month)
reg_task_keyboard.insert(days_of_week)
reg_task_keyboard.insert(every_day)
reg_task_keyboard.row(back)



def reg_days_of_week_keyboard_create(flag:bool=False,mas=[]):
    reg_days_of_week_keyboard=InlineKeyboardMarkup(row_width=2)
    mon=InlineKeyboardButton(text='Понедельник',callback_data='tasks_days_0')
    tue=InlineKeyboardButton(text='Вторник',callback_data='tasks_days_1')
    wed=InlineKeyboardButton(text='Среда',callback_data='tasks_days_2')
    thu=InlineKeyboardButton(text='Четверг',callback_data='tasks_days_3')
    fri=InlineKeyboardButton(text='Пятница',callback_data='tasks_days_4')
    sat=InlineKeyboardButton(text='Суббота',callback_data='tasks_days_5')
    san=InlineKeyboardButton(text='Воскресенье',callback_data='tasks_days_6')
    mas_button=[mon,tue,wed,thu,fri,sat,san]
    for i in mas:
        mas_button[i]=0
    for i in mas_button:
        if i!=0:
            reg_days_of_week_keyboard.insert(i)
    
    if flag:
        reg_days_of_week_keyboard.row(InlineKeyboardButton(text='Далее',callback_data='tasks_reg_days/of/week'))
    reg_days_of_week_keyboard.row(back)
    return reg_days_of_week_keyboard

rep_tasks_yes_no_keyborad=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='да',callback_data='rep_tasks_time_yes')
no=InlineKeyboardButton(text='нет',callback_data='rep_tasks_time_no')   
rep_tasks_yes_no_keyborad.insert(yes)
rep_tasks_yes_no_keyborad.insert(no)

rep_tasks_yes_no_1_keyborad=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='да',callback_data='tasks_add_reg_1')
no=InlineKeyboardButton(text='нет',callback_data='tasks_add_reg')   
rep_tasks_yes_no_1_keyborad.insert(yes)
rep_tasks_yes_no_1_keyborad.insert(no)

rep_tasks_yes_no_2_keyborad=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='да',callback_data='rep_tasks_2_yes')
no=InlineKeyboardButton(text='нет',callback_data='tasks_add_reg')   
rep_tasks_yes_no_2_keyborad.insert(yes)
rep_tasks_yes_no_2_keyborad.insert(no)

def create_tasks_week_keyboard():
    task_keyboard= InlineKeyboardMarkup(row_width=1)
    mas=list(get_task_for_time(7).values())
    for i in mas:
        i=i[0]
        task_keyboard.insert(InlineKeyboardButton(text=i[0]+(' ' if i[2]=='None' else f'({i[2]})'),callback_data=f'task_{i[1]}'))
    task_keyboard.insert(InlineKeyboardButton(text="Добавить новые задачи",callback_data="add_new_tasks"))
    task_keyboard.insert(InlineKeyboardButton(text="Назад",callback_data="tasks"))
    return task_keyboard

def create_every_day_challenge_keyboard():
    mas=get_all_every_day_challenge()
    task_keyboard= InlineKeyboardMarkup(row_width=1)
    for i in mas:
        id=i[0]
        name=i[1]
        task_keyboard.insert(InlineKeyboardButton(text=name,callback_data=f'every_day_challenge_{id}'))
    task_keyboard.insert(InlineKeyboardButton(text="Назад",callback_data="tasks"))
    return task_keyboard
every_day_challenge_yes_no_2_keyborad=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='да',callback_data='every_day_challenge_yes')
no=InlineKeyboardButton(text='нет',callback_data='every_day_challenge')   
every_day_challenge_yes_no_2_keyborad.insert(yes)
every_day_challenge_yes_no_2_keyborad.insert(no)