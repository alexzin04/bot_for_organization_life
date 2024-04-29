from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram.types import CallbackQuery,Message
from keyboards.inline.finance_keyboards import delete_account_keyboard, finance_keyboard
from keyboards.inline.finance_keyboards import  consumption_keyboard,consumption_keyboard_category,finance_consumption_yes_no_keuboard,finance_consumption_yes_no_keuboard_2
from keyboards.inline.finance_keyboards import finance_income_yes_no_keuboard_2,income_keyboard,finance_income_yes_no_keuboard
from keyboards.inline.finance_keyboards import finance_data_keyboard,transfer_keyboard,transfer_keyboard_2,finance_transfer_yes_no_keuboard,finance_history_keyboard,finance_history_1_keyboard
from keyboards.inline.finance_keyboards import history_keyboard,history_keyboard_2,history_keyboard_3,history_keyboard_4,change_account_money_keyboard,finance_change_yes_no_keuboard
from keyboards.inline.finance_keyboards import delete_account_keyboard,finance_delete_yes_no_keuboard
from keyboards.inline.start_keyboard import start__keybord
from utils.db_api.finance_db import insert_new_purchases,insrert_new_income,transfer_from_account_to_account,get_money_from_accounts,get_all_purchases,get_account_category_purchases
from utils.db_api.finance_db import get_account_from_id,get_account_purchases,get_category_purchases,change_account_money,delete_account
from aiogram.dispatcher import FSMContext
from states.finance_state import finance_income_state,finance_iconsumption_state,finance_transfer_state,finance_change_state
from aiogram.dispatcher.filters import Text

@dp.callback_query_handler(text='finance')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(text='Выберите что вы хотите сделать:',reply_markup=finance_keyboard)


#добавление доходов
@dp.callback_query_handler(text='income')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(text='Выберите счет для добавления дохода',reply_markup=income_keyboard())

@dp.callback_query_handler(text_contains='income_acc_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(text='Введите сумму которую хотите добавить на счет или напишите отмена, для возвращения назад')
    await state.set_data({'id':int(call.data.split('_')[2])})
    await finance_income_state.Q1.set()

@dp.message_handler(Text(equals="отмена",ignore_case=True),state=finance_income_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.answer(text='Выберите счет для добавления дохода',reply_markup=income_keyboard())
    await state.finish()

@dp.message_handler(state=finance_income_state.Q1)
async def productt(message:Message,state:FSMContext):
    t=message.text
    if not(t.isdigit()):
        await message.answer('Вы ввели не число, введите еще раз')
    await state.update_data({'money':int(t)})
    await message.answer(f'Вы ввели вот такую cумму {t}\n Все введено верно?',reply_markup=finance_income_yes_no_keuboard)

@dp.callback_query_handler(text='income_yes_2',state=finance_income_state.Q2)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    data=await state.get_data()
    insrert_new_income(name=data['name'],accounts_id=data['id'],money=data['money'])
    await call.message.answer('Данные успещно добавлены, спасибо!',reply_markup=start__keybord)
    await state.finish()

@dp.callback_query_handler(text='income_no_1',state=finance_income_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите сумму которую хотите добавить на счет еще раз или напишите отмена, для возвращения назад')

@dp.callback_query_handler(text='income_yes_1',state=finance_income_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите источник дохода или отмена для возвращения назад')
    await finance_income_state.Q2.set()

@dp.message_handler(Text(equals="отмена",ignore_case=True),state=finance_income_state.Q2)
async def productt(message:Message,state:FSMContext):
    await message.answer(text='Выберите счет для добавления дохода',reply_markup=income_keyboard())
    await state.finish()

@dp.message_handler(state=finance_income_state.Q2)
async def productt(message:Message,state:FSMContext):
    text=message.text
    await message.answer(f'Вы ввели {text} все верно?',reply_markup=finance_income_yes_no_keuboard_2)
    await state.update_data({'name':text})

@dp.callback_query_handler(text='income_no_2',state=finance_income_state.Q2)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите источник дохода или отмена для возвращения назад')

#Добавление расходов
@dp.callback_query_handler(text='consumption')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет для добавления расхода:',reply_markup=consumption_keyboard())

@dp.callback_query_handler(text_contains='consumption_acc_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(text='Выюерите категорию в которой происходит трата:',reply_markup=consumption_keyboard_category())
    await state.set_data({'acc_id':int(call.data.split('_')[2])})

@dp.callback_query_handler(text_contains='consumption_cat_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({"cat_id":int(call.data.split('_')[2])})
    await call.message.answer('Введите название траты или напишите отмена для возвращения назад')
    await finance_iconsumption_state.Q1.set()

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=finance_iconsumption_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.answer(text='Выберите счет для добавления расхода',reply_markup=consumption_keyboard())
    await state.finish()

@dp.message_handler(state=finance_iconsumption_state.Q1)
async def productt(message:Message,state:FSMContext):
    text=message.text
    await message.answer(f'Вы ввели {text} все верно?',reply_markup=finance_consumption_yes_no_keuboard)
    await state.update_data({'name':text})

@dp.callback_query_handler(text='consumption_yes_1',state=finance_iconsumption_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    print(await state.get_data())
    await call.message.answer('Теперь введите сколько вы потратили или напишите отмена для возвращения назад')
    await finance_iconsumption_state.Q2.set()

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=finance_iconsumption_state.Q2)
async def productt(message:Message,state:FSMContext):
    await finance_iconsumption_state.Q1.set()
    await message.answer(text='Выберите счет для добавления расхода',reply_markup=consumption_keyboard())
    await state.finish()

@dp.callback_query_handler(text='consumption_no_1',state=finance_iconsumption_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите название траты или напишите отмена для возвращения назад')

@dp.message_handler(state=finance_iconsumption_state.Q2)
async def productt(message:Message,state:FSMContext):
    text=message.text
    if not(text.isdigit()):
        await message.answer('Вы ввели не число, введите еще раз')
    else:
        await state.update_data({'money':int(text)})
        await message.answer(f'Вы ввели вот такую cумму {text}\n Все введено верно?',reply_markup=finance_consumption_yes_no_keuboard_2)

@dp.callback_query_handler(text='consumption_yes_2',state=finance_iconsumption_state.Q2)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    data=await state.get_data()
    await state.finish()
    insert_new_purchases(data['name'],data['acc_id'],data['cat_id'],data['money'])
    await call.message.answer('Данные о расходах успешно добавлены',reply_markup=start__keybord)

@dp.callback_query_handler(text='consumption_no_2',state=finance_iconsumption_state.Q2)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите cумму траты или напишите отмена для возвращения назад')


#Доп функции
@dp.callback_query_handler(text='finance_data')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.finish()
    await call.message.answer('Выберите фукнцию',reply_markup=finance_data_keyboard)


#Доп функция перевода между счетами
@dp.callback_query_handler(text='transfer')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет с которого будут выполнен первод',reply_markup=transfer_keyboard())

@dp.callback_query_handler(text_contains='transfer_acc_from_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.set_data({'acc_id_1':int(call.data.split('_')[3])})
    await call.message.answer('Веберите счет куда переводим',reply_markup=transfer_keyboard_2())

@dp.callback_query_handler(text_contains='transfer_acc_to_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'acc_id_2':int(call.data.split('_')[3])})
    await call.message.answer('Введите сумму перевода или отмена для возвращения назад')
    await finance_transfer_state.Q1.set()

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=finance_transfer_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.answer(text='Выберите функцию',reply_markup=finance_data_keyboard)
    await state.finish()

@dp.message_handler(state=finance_transfer_state.Q1)
async def productt(message:Message,state:FSMContext):
    text=message.text
    if not(text.isdigit()):
        await message.answer('Вы ввели не число, введите еще раз')
    else:
        await state.update_data({'money':int(text)})
        await message.answer(f'Вы ввели вот такую cумму {text}\n Все введено верно?',reply_markup=finance_transfer_yes_no_keuboard)


@dp.callback_query_handler(text='transfer_yes_1',state=finance_transfer_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    data=await state.get_data()
    await state.finish()
    transfer_from_account_to_account(data['acc_id_1'],data['acc_id_2'],data['money'])
    await call.message.answer('Деньги успешно переведены',reply_markup=start__keybord)



@dp.callback_query_handler(text='consumption_no_1',state=finance_transfer_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите название траты или напишите отмена для возвращения назад')

#Доп функция вывод сосоятния счета

@dp.callback_query_handler(text="bank_count")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(f'{get_money_from_accounts()}\n Веберите функцию:',reply_markup=start__keybord)

#Доп функция история расходов

@dp.callback_query_handler(text='history_consumption')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.finish()
    await call.message.answer('Выберите по какому приницпу вывести историю трат:',reply_markup=finance_history_1_keyboard)


def transformation_list(listt:list)->str:
    summ=0
    if len(listt)!=0:
        s='Ваши трасходы:\nНазвание траты|Категория траты|Счет|Сумма|Дата\n'
        for i in listt:
            name,cat,acc,money,data=i
            s+=f'''{name}|{cat}|{acc if acc!=None else 'счет удален'}|{money}|{data}\n'''
            summ+=money
        s+=f'\nВсего потрачено: {summ}'
    else: s='У вас нет расходов за это время'
    return s

#по времени
@dp.callback_query_handler(text='history_time_consumption')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Веберите за какое время вывести историю расходов',reply_markup=finance_history_keyboard)

@dp.callback_query_handler(text_contains='history_time')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    day=int(call.data.split('_')[2])
    s=transformation_list(get_all_purchases(day))
    await call.message.answer(f'{s}\nВыберите функцию',reply_markup=start__keybord)

#по категории и счету
@dp.callback_query_handler(text='history_cat_acc')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет:',reply_markup=history_keyboard())
    

@dp.callback_query_handler(text_contains="history_1_acc_")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'acc_id':int(call.data.split('_')[3])})
    await call.message.answer('Выберите категорию:',reply_markup=history_keyboard_2())

@dp.callback_query_handler(text_contains="history_1_cat_")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    acc_id=(await state.get_data())['acc_id']
    s=transformation_list(get_account_category_purchases(int(call.data.split('_')[3]),acc_id,day=30))
    await call.message.answer(f'{s}\nВыберите функцию',reply_markup=start__keybord)
    await state.finish()

#по счету 
@dp.callback_query_handler(text="history_acc")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет:',reply_markup=history_keyboard_3())

@dp.callback_query_handler(text_contains="history_2_acc_")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    s=transformation_list(get_account_purchases(int(call.data.split('_')[3]),day=30))
    await call.message.answer(f'{s}\nВыберите функцию',reply_markup=start__keybord)

#по категории
@dp.callback_query_handler(text="history_cat")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет:',reply_markup=history_keyboard_4())

@dp.callback_query_handler(text_contains="history_2_cat_")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    s=transformation_list(get_category_purchases(int(call.data.split('_')[3]),day=30))
    await call.message.answer(f'{s}\nВыберите функцию',reply_markup=start__keybord)

#изменение суммы на счетах

@dp.callback_query_handler(text="change_account_money")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет на котором хотите поменять, сумму:',reply_markup=change_account_money_keyboard())

@dp.callback_query_handler(text_contains='change_acc_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    id = int((call.data.split("_"))[2])
    await finance_change_state.Q1.set()
    await state.update_data({'id':id})
    await call.message.answer('Теперь введите новую сумму, для данного счета (или отмена для возвращения назад)')


@dp.message_handler(Text(equals='отмена',ignore_case=True),state=finance_change_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.answer(text='Выберите функцию',reply_markup=finance_data_keyboard)
    await state.finish()

@dp.message_handler(state=finance_change_state.Q1)
async def productt(message:Message,state:FSMContext):
    text=message.text
    if not(text.isdigit()):
        await message.answer('Вы ввели не число, введите еще раз')
    else:
        await state.update_data({'money':int(text)})
        await message.answer(f'Вы ввели вот такую cумму {text}\nВсе введено верно?',reply_markup=finance_change_yes_no_keuboard)

@dp.callback_query_handler(text='change_no_1',state=finance_change_state.Q1)
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите новую сумму еще раз (или отмена для возвращения назад)')

@dp.callback_query_handler(text='change_yes_1',state=finance_change_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    dictt= await state.get_data()
    await state.finish()
    change_account_money(dictt['id'],dictt["money"])
    await call.message.answer('Изменение произошло успешно)\nВыберите нужную функцию',reply_markup=start__keybord)

#удаление счат
@dp.callback_query_handler(text="delete_account")
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите счет который хотите удалить:',reply_markup=delete_account_keyboard())

@dp.callback_query_handler(text_contains='delete_acc_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    id = int((call.data.split("_"))[2])
    await state.update_data({'id':id})
    await call.message.answer(f'Вы выбрали следующий счет:{get_account_from_id(id)[0][0]}\n Удаляем его?',reply_markup=finance_delete_yes_no_keuboard)


@dp.callback_query_handler(text='delete_yes_1')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    delete_account( int((await state.get_data())["id"]))
    await state.finish()
    await call.message.answer('Счет успешно удален\nВыберите функцию',reply_markup=start__keybord)