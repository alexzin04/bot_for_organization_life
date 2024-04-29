from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start__keybord= InlineKeyboardMarkup(row_width=2)
finance=InlineKeyboardButton(text='Финансы', callback_data='finance')
start__keybord.insert(finance)
tasks=InlineKeyboardButton(text='Задачи',callback_data='tasks')
start__keybord.insert(tasks)
sport=InlineKeyboardButton(text='Спорт',callback_data='sport')
start__keybord.insert(sport)
food=InlineKeyboardButton(text='Питание',callback_data='food')
#start__keybord.insert(food)
change=InlineKeyboardButton(text='Редактирование',callback_data='change')
start__keybord.row(change)

