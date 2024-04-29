from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.finance_db import get_all_accounts, get_all_category

finance_keyboard= InlineKeyboardMarkup(row_width=2)
income=InlineKeyboardButton(text='Доход', callback_data='income')
finance_keyboard.insert(income)
consumption=InlineKeyboardButton(text='Расход',callback_data='consumption')
finance_keyboard.insert(consumption)
finance_data=InlineKeyboardButton(text='Доп Функции',callback_data='finance_data')
finance_keyboard.row(finance_data)
back_1=InlineKeyboardButton(text='назад',callback_data='start')
finance_keyboard.row(back_1)

finance_income_yes_no_keuboard=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='income_yes_1')
no=InlineKeyboardButton(text='Нет',callback_data='income_no_1')
finance_income_yes_no_keuboard.add(yes)
finance_income_yes_no_keuboard.add(no)

finance_income_yes_no_keuboard_2=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='income_yes_2')
no=InlineKeyboardButton(text='Нет',callback_data='income_no_2')
finance_income_yes_no_keuboard_2.add(yes)
finance_income_yes_no_keuboard_2.add(no)

finance_consumption_yes_no_keuboard=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='consumption_yes_1')
no=InlineKeyboardButton(text='Нет',callback_data='consumption_no_1')
finance_consumption_yes_no_keuboard.add(yes)
finance_consumption_yes_no_keuboard.add(no)

finance_consumption_yes_no_keuboard_2=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='consumption_yes_2')
no=InlineKeyboardButton(text='Нет',callback_data='consumption_no_2')
finance_consumption_yes_no_keuboard_2.add(yes)
finance_consumption_yes_no_keuboard_2.add(no)

def income_keyboard()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'income_acc_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='finance')
    keyboard.insert(cancel)
    return keyboard
 
def consumption_keyboard()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'consumption_acc_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='finance')
    keyboard.insert(cancel)
    return keyboard

def consumption_keyboard_category()->InlineKeyboardMarkup:
    a=get_all_category()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'consumption_cat_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data="consumption")
    keyboard.insert(cancel)
    return keyboard



finance_data_keyboard=InlineKeyboardMarkup(row_width=1)
transpher=InlineKeyboardButton(text='Перевод между счетами', callback_data='transfer')
finance_data_keyboard.insert(transpher)
bank_count=InlineKeyboardMarkup(text='Деньги на счетах',callback_data='bank_count')
finance_data_keyboard.insert(bank_count)
history_consumption=InlineKeyboardMarkup(text='История расходов',callback_data='history_consumption')
finance_data_keyboard.insert(history_consumption)
change_account_money=InlineKeyboardMarkup(text='Изменение суммы на счетах',callback_data='change_account_money')
finance_data_keyboard.insert(change_account_money)
delete_account=InlineKeyboardMarkup(text='Удаление счета',callback_data='delete_account')
finance_data_keyboard.insert(delete_account)
back_1=InlineKeyboardButton(text='назад',callback_data='finance')
finance_data_keyboard.row(back_1)

def transfer_keyboard()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'transfer_acc_from_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='finance_data')
    keyboard.insert(cancel)
    return keyboard

def transfer_keyboard_2()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'transfer_acc_to_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='transfer')
    keyboard.insert(cancel)
    return keyboard
    
finance_transfer_yes_no_keuboard=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='transfer_yes_1')
no=InlineKeyboardButton(text='Нет',callback_data='transfer_no_1')
finance_transfer_yes_no_keuboard.add(yes)
finance_transfer_yes_no_keuboard.add(no)

finance_change_yes_no_keuboard=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='change_yes_1')
no=InlineKeyboardButton(text='Нет',callback_data='change_no_1')
finance_change_yes_no_keuboard.add(yes)
finance_change_yes_no_keuboard.add(no)

finance_delete_yes_no_keuboard=InlineKeyboardMarkup(row_width=2)
yes=InlineKeyboardButton(text='Да',callback_data='delete_yes_1')
no=InlineKeyboardButton(text='Нет',callback_data='finance_data')
finance_delete_yes_no_keuboard.add(yes)
finance_delete_yes_no_keuboard.add(no)

finance_history_keyboard=InlineKeyboardMarkup(row_width=1)
one_day=InlineKeyboardMarkup(text='за сегодня',callback_data='history_time_0')
one_week=InlineKeyboardMarkup(text='за последние 7 дней',callback_data='history_time_7')
one_month=InlineKeyboardMarkup(text='за послдение 30 дней',callback_data='history_time_30')
cancel=InlineKeyboardButton(text='Назад',callback_data='history_consumption')
finance_history_keyboard.add(one_day)
finance_history_keyboard.add(one_week)
finance_history_keyboard.add(one_month)
finance_history_keyboard.add(cancel)

finance_history_1_keyboard=InlineKeyboardMarkup(row_width=1)
time=InlineKeyboardMarkup(text='за  проможетуок времени',callback_data='history_time_consumption')
acc=InlineKeyboardMarkup(text='c опредленного счета',callback_data='history_acc')
cat=InlineKeyboardMarkup(text='по категории ',callback_data='history_cat')
cat_acc=InlineKeyboardMarkup(text='по категории и счету ',callback_data='history_cat_acc')
cancel=InlineKeyboardButton(text='Назад',callback_data='finance_data')
finance_history_1_keyboard.add(time)
finance_history_1_keyboard.add(cat_acc)
finance_history_1_keyboard.add(acc)
finance_history_1_keyboard.add(cat)
finance_history_1_keyboard.add(cancel)

def history_keyboard()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'history_1_acc_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='history_consumption')
    keyboard.insert(cancel)
    return keyboard

def history_keyboard_2()->InlineKeyboardMarkup:
    a=get_all_category()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'history_1_cat_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='history_cat_acc')
    keyboard.insert(cancel)
    return keyboard

def history_keyboard_3()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'history_2_acc_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='history_consumption')
    keyboard.insert(cancel)
    return keyboard

def history_keyboard_4()->InlineKeyboardMarkup:
    a=get_all_category()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'history_2_cat_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='history_cat_acc')
    keyboard.insert(cancel)
    return keyboard

def change_account_money_keyboard()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'change_acc_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='finance_data')
    keyboard.insert(cancel)
    return keyboard

def delete_account_keyboard()->InlineKeyboardMarkup:
    a=get_all_accounts()
    keyboard=InlineKeyboardMarkup(row_width=1)
    for i in a:
        text,id=i
        add_new=InlineKeyboardButton(text=text,callback_data=f'delete_acc_{id}')
        keyboard.insert(add_new)
    cancel=InlineKeyboardButton(text='Назад',callback_data='finance_data')
    keyboard.insert(cancel)
    return keyboard