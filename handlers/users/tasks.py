from datetime import datetime,date,time,timedelta
from email import message
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram.types import CallbackQuery,Message
from aiogram.dispatcher.filters import Text
from keyboards.inline.start_keyboard import start__keybord
from keyboards.inline.tasks_keyboards import  create_challenge_add_keyboard,additional_func_keyboard,create_tasks_today_add_keyboard,create_task_keyboard,create_tasks_today_keyboard,tasks_yes_no_keyborad,add_new_task_keybiard,reg_task_keyboard,reg_days_of_week_keyboard_create,rep_tasks_yes_no_keyborad,rep_tasks_yes_no_1_keyborad,rep_tasks_yes_no_2_keyborad,create_every_day_challenge_keyboard,every_day_challenge_yes_no_2_keyborad,add_today_tasks_yes_no_keyborad,every_day_challenge_add_yes_no_keyborad
from utils.db_api.tasks_db import change_status_from_id,add_new_task,add_repeat_tasks,generate_str_from_dict_task, get_task_for_time,create_str_from_id_for_every_day_challenge,get_inforamtion_about_challenge_today,change_mas_for_every_day_challenge,add_new_every_day_challenge
from states.tasks_state import task_add_state,task_reg_add_state,every_day_challenge_state,add_every_day_challenge_state


@dp.callback_query_handler(text='tasks')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(text='Выберите функцию:',reply_markup=create_task_keyboard())

@dp.callback_query_handler(text="tasks_today")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await state.finish()
    await call.message.delete()
    await call.message.answer(text='Задачи на сегодня:',reply_markup=create_tasks_today_keyboard())

@dp.callback_query_handler(text_contains="task_")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'id':int(call.data.split("_")[1])})
    await call.message.answer("Вы выполнили задачу?",reply_markup=tasks_yes_no_keyborad)

@dp.callback_query_handler(text="tasks_yes")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    dictt=await state.get_data()
    id=dictt['id']
    change_status_from_id(id)
    await state.finish()
    await call.message.answer('Статус задачи изменен\nЗадачи на сегодня',reply_markup=create_tasks_today_keyboard())

@dp.callback_query_handler(text='add_new_tasks')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(text='Выберите:',reply_markup=add_new_task_keybiard)

@dp.callback_query_handler(text='tasks_add_once')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await task_add_state.Q1.set()
    await call.message.answer('Начинается создание новой задачи.\nВведите назавание задачи(в случае выбора по ошибке напишите отмена)')

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=task_add_state)
async def productt(message:Message,state:FSMContext):
    await state.finish()
    await message.delete()
    await message.answer('Начините все заново(',reply_markup=create_tasks_today_keyboard())

@dp.message_handler(state=task_add_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.delete()
    await message.answer(f'''Вы ввели {message.text}\nВыберите дату:\n(или напишите свою в формате yyyy-mm-dd Например: 2024-01-01''',reply_markup=create_tasks_today_add_keyboard())
    await state.update_data({'name':message.text})
    await task_add_state.Q2.set()

@dp.callback_query_handler(text_contains='add_tasks_today_',state=task_add_state.Q2)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'data':(datetime.strptime(call.data.split("_")[3],'%Y-%m-%d'))})
    await call.message.answer('Нужно ли время для этой задачи?',reply_markup=add_today_tasks_yes_no_keyborad)
    await state.reset_state(False)

@dp.callback_query_handler(text='add_tasks_yes')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите время в формате hh-mm (Например 14-01)\nИли омена в случае ошибки')
    await task_add_state.Q3.set()

@dp.callback_query_handler(text='add_tasks_no')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    dictt=await state.get_data()
    await state.finish()
    name=dictt["name"]
    date=dictt['data']
    add_new_task(name,date,False)
    await call.message.answer("Задача успешно добавлена",reply_markup=create_tasks_today_keyboard())


@dp.message_handler(state=task_add_state.Q2)
async def productt(message:Message,state:FSMContext):
    if len(message.text.split('-'))==3:
        year,month,day=map(int,message.text.split('-'))
        dat=date(year,month,day)
        await state.update_data({'data':dat})
        await message.answer('Нужно ли время для этой задачи?',reply_markup=add_today_tasks_yes_no_keyborad)
        await state.reset_state(False)
    else:
        await message.answer('Вы ввели данные в неправильном формате\nПопробуйте еще раз')

@dp.message_handler(state=task_add_state.Q3)
async def productt(message:Message,state:FSMContext):
    await message.delete()
    if len(message.text.split('-'))==2:
        hour,minute=map(int,message.text.split('-'))
        dictt=await state.get_data()
        await state.finish()
        name=dictt['name']
        datee=dictt['data']
        dat=datetime(datee.year,datee.month,datee.day,hour,minute)
        add_new_task(name,dat,True)
        await message.answer("Задача успешно добавлена",reply_markup=create_tasks_today_keyboard())
    else:
        await message.answer('Вы ввели данные в неправильном формате\nПопробуйте еще раз')



@dp.callback_query_handler(text='tasks_add_reg')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Введите назавание задачи(в случае выбора по ошибке напишите отмена)")
    await task_reg_add_state.Q1.set()

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=task_reg_add_state)
async def productt(message:Message,state:FSMContext):
    await state.finish()
    await message.delete()
    await message.answer('Начините все заново(',reply_markup=create_tasks_today_keyboard())


@dp.message_handler(state=task_reg_add_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.delete()
    await message.answer(f'Вы ввели {message.text}\nВсе введено верно?',reply_markup=rep_tasks_yes_no_1_keyborad)
    await state.reset_data()
    await state.reset_state(False)
    await state.update_data({'name':message.text})


@dp.callback_query_handler(text='tasks_add_reg_1')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите регулряность задачи:',reply_markup=reg_task_keyboard)

@dp.callback_query_handler(text="tasks_days_of_week")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'days':[]})
    await call.message.answer('Выберите в какие дни недели будет повтор задачи',reply_markup= reg_days_of_week_keyboard_create())



@dp.callback_query_handler(text_contains='tasks_days_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    A=['понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
    listt=(await state.get_data())['days']
    listt.append(int(call.data.split("_")[2]))
    await state.update_data({'days':listt})
    await call.message.answer(f'Вы выбрали {A[int(call.data.split("_")[2])]}\nМожете выбрать еще \nВ случае ошибки вернитесь назад',reply_markup= reg_days_of_week_keyboard_create(True,listt))

@dp.callback_query_handler(text_contains='tasks_reg_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    rules=call.data.split("_")[2]
    rules=rules.replace('/','_',-1)
    if rules=='days_of_week':
        mas=(await state.get_data())['days']
        rules+=' '
        for i in mas:
            rules+=str(i)+','
        rules=rules[:-1]
    
   
    await state.update_data({'rules':rules})
    await call.message.answer("Выберите нужно ли время выполнение для данной задачи:",reply_markup=rep_tasks_yes_no_keyborad)

@dp.callback_query_handler(text='rep_tasks_time_yes')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Введите время для задачи: в формате HH-MM (пример 12-01), для отмены напишите отмена")
    await task_reg_add_state.Q2.set()



def help_generate_text(dictt:dict):
    A=['Понедельник','Вторник','Среду','Четверг','Пятницу','Субботу','Воскресенье']
    rules=dictt['rules']
    if rules=='every_day':
        rules='каждый день'
    elif rules=='once_month':
        rules='каждый месяц(раз в 30 дней)'
    else:
        s='Повтор в '
        mas=list(map(int,(rules.split()[1]).split(',')))
        mas.sort()
        for i in mas:
            s+=' '+A[int(i)]+','
        rules=s[:-1]
    return f'''Вот данные для создания регулярной задачи\nНазвание {dictt['name']}\nПравило {rules}\nВремя {'не нужно' if dictt['time']==None else dictt['time']}\nСоздаем?'''


@dp.message_handler(state=task_reg_add_state.Q2)
async def productt(message:Message,state:FSMContext):
    await message.delete()
    if len(message.text.split('-'))==2:
        await state.update_data({'time':message.text})
        dictt=await state.get_data()
        await message.answer(help_generate_text(dictt),reply_markup=rep_tasks_yes_no_2_keyborad)
        await state.reset_state(False)
    else:
        await message.answer('Время введено в неправильном формате, попробуйти еще раз')

@dp.callback_query_handler(text='rep_tasks_time_no')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'time':None})
    await call.message.answer(help_generate_text(await state.get_data()),reply_markup=rep_tasks_yes_no_2_keyborad)
    

@dp.callback_query_handler(text='rep_tasks_2_yes')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    dictt=await state.get_data()
    if dictt["rules"].split()[0]=="days_of_week":
        cur_weekday=date.today().weekday()
        weekday_array=list(map(int,dictt["rules"].split()[1].split(',')))
        weekday_array.sort()
        next_weekday=None
        for day in weekday_array:
            if day>=cur_weekday:
                next_weekday=day
                break
        if next_weekday==None:
            next_weekday=weekday_array[0]
        s=''
        for i in weekday_array:
            s+=str(i)+','
        dictt["rules"]="days_of_week "+s[:-1]
        date_start = date.today() + timedelta(days=(next_weekday - cur_weekday) % 7)
    elif dictt['rules']=="every_day":
        date_start=date.today()
    elif dictt['rules']=="once_month":
        date_start=date.today()
    add_repeat_tasks(dictt['name'],date_start,dictt["rules"],time(int(dictt['time'].split('-')[0]),int(dictt['time'].split('-')[1])) if dictt['time']!=None else dictt['time'] )
    await call.message.answer('Задача успешно добавлена',reply_markup=start__keybord)

#Задача доделать доп функции, удаление регулярных задач))
@dp.callback_query_handler(text='additional_func')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await state.reset_data()
    await call.message.delete()
    await call.message.answer('Выберите функцию:',reply_markup=additional_func_keyboard)

@dp.callback_query_handler(text='add_new_challenge')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите название ежедневного вызова\nВ случае ошибки введите отмена')
    await add_every_day_challenge_state.Q1.set()

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=add_every_day_challenge_state)
async def productt(message:Message,state:FSMContext):
    await state.finish()
    await message.delete()
    await message.answer('Ежедневные вызовы:',reply_markup=create_every_day_challenge_keyboard())

@dp.message_handler(state=add_every_day_challenge_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.answer(f'Вы ввели {message.text}\nТеперь выберите дату начала, данного вызова\n(Или введите свою дату в формате yyyy-mm-dd Например 2024-01-10)',reply_markup=create_challenge_add_keyboard())
    await state.update_data({"name":message.text})
    await add_every_day_challenge_state.Q2.set()

@dp.callback_query_handler(text_contains='challenge_add_today_',state=add_every_day_challenge_state.Q2)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.update_data({'data':(datetime.strptime(call.data.split("_")[3],'%Y-%m-%d'))})
    await call.message.answer('Введите количество повторений\nили отмена в случае ошибки')
    await add_every_day_challenge_state.Q3.set()

@dp.message_handler(state=add_every_day_challenge_state.Q2)
async def productt(message:Message,state:FSMContext):
    if len(message.text.split('-'))==3:
        year,month,day=map(int,message.text.split('-'))
        dat=date(year,month,day)
        await state.update_data({'data':dat})
        await message.answer('Введите количество повторений\nили отмена в случае ошибки')
        await add_every_day_challenge_state.Q3.set()
    else:
        await message.answer('Вы ввели данные в неправильном формате\nПопробуйте еще раз',reply_markup=create_challenge_add_keyboard())

@dp.message_handler(state=add_every_day_challenge_state.Q3)
async def productt(message:Message,state:FSMContext):
    if(message.text.isdigit()):
        await state.update_data({'count':message.text})
        await message.answer('Введите сколько дней будет идти вызов (например 14)\nили отмена в случае ошибки')
        await add_every_day_challenge_state.Q4.set()
    else:
        await message.answer('Введите число еще раз\nИли отмена в случае ошибки')

@dp.message_handler(state=add_every_day_challenge_state.Q4)
async def productt(message:Message,state:FSMContext):
    if (message.text.split()[0]).isdigit():
        dictt=await state.get_data()
        date_finish=dictt['data']+timedelta(days=int((message.text.split()[0])))
        await state.update_data({'days':int(message.text.split()[0])})
        await message.answer(f"Вы ввели следущие данные\n1.Название: {dictt['name']}\n2.Дата начала: {dictt['data'].strftime('%Y-%m-%d')}\n3.Дата конца: {date_finish.strftime('%Y-%m-%d')}\n4.Количество повторений: {dictt['count']}\nВсе данные верны?",reply_markup=every_day_challenge_add_yes_no_keyborad)
        await state.reset_state(False)
    else:
         await message.answer('Введите число дней еще раз\nИли отмена в случае ошибки')

@dp.callback_query_handler(text='every_day_add_challenge_yes')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    dictt=await state.get_data()
    add_new_every_day_challenge(dictt["name"],dictt['data'],dictt['count'],dictt['days'])
    await call.message.answer('Вызов успешно добавлен\nВыберите нужную функцию:',reply_markup=start__keybord)

@dp.callback_query_handler(text='tasks_for_week')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(f'Вот задачи на ближайщую неделю:{generate_str_from_dict_task(get_task_for_time(7))}',reply_markup=start__keybord)

@dp.callback_query_handler(text='every_day_challenge')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.finish()
    await call.message.answer(f'Вот вызовы которые идут на данный момент',reply_markup=create_every_day_challenge_keyboard())


@dp.callback_query_handler(text='every_day_challenge_yes')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    id=(await state.get_data())['id']
    count_today,count_all=get_inforamtion_about_challenge_today(id)
    await every_day_challenge_state.Q1.set()
    await call.message.answer(f'''Введите количество повторений\nНа данный момент вы уже сделали {count_today} из {count_all} ''' )
    

@dp.callback_query_handler(text_contains='every_day_challenge_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.finish()
    id=int(call.data.split("_")[3])
    await state.update_data({'id':id})
    await call.message.answer(create_str_from_id_for_every_day_challenge(id),reply_markup=every_day_challenge_yes_no_2_keyborad)

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=every_day_challenge_state)
async def productt(message:Message,state:FSMContext):
    await state.finish()
    await message.delete()
    await message.answer('Ежедневные вызовы:',reply_markup=create_every_day_challenge_keyboard())


@dp.message_handler(state=every_day_challenge_state.Q1)
async def productt(message:Message,state:FSMContext):
    await message.delete()
    if(not(message.text.isdigit())):
        await message.answer('Вы ввели не число, поробуйте еще раз)')
    else:
        id=(await state.get_data())['id']
        await state.finish()
        change_mas_for_every_day_challenge(id,int(message.text))
        await message.answer(f'{message.text} повторений добавлено в базу данных\n\n Выберите функцию',reply_markup=start__keybord)