from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram.types import CallbackQuery,Message
from aiogram.dispatcher.filters import Text
from states.sport_state import sport_add_state,sport_add_new_program_state
from keyboards.inline.start_keyboard import start__keybord
from keyboards.inline.sport_keyboards import new_keyboard_2, new_keyboard_5, sport_keyboard,sport_data_keyboard,new_keyboard,new_keyboard_3,sport_history_keyboard,sport_yes_no_keyboard
from utils.db_api.sport_db import history_of_workout, last_result_for_excersize,get_workouts,add_new_tren,get_all_exsersize,add_new_workouts



@dp.callback_query_handler(text='sport')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(text='Выберите функцию:',reply_markup=sport_keyboard)



@dp.callback_query_handler(text='new_sport')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выбери какую тренировку делаем сегодня?',reply_markup=new_keyboard())

@dp.callback_query_handler(text_contains='workouts_name_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    id=int(call.data.split('_')[2])
    if len(call.data.split('_'))==4:
        data=await state.get_data()
        f=False
        for i in data['mas']: 
            if (len(i)!=0):
                f=True
                break
        if f:
            await state.update_data({'flag':True})
            await call.message.answer('Начинаем тренировку для добавления нового подхода выбери упражнение:',reply_markup=new_keyboard_2(id,True))
        else:
            await call.message.answer('Начинаем тренировку для добавления нового подхода выбери упражнение:',reply_markup=new_keyboard_2(id))
    else:
        a=get_workouts(id)
        mas=[[]for i in a]
        await state.set_data({'tren_id':id,'mas':mas})
        await call.message.answer('Начинаем тренировку для добавления нового подхода выбери упражнение:',reply_markup=new_keyboard_2(id))

@dp.callback_query_handler(text_contains='workouts_exers_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    exer_id=int(call.data.split('_')[2])
    await state.update_data({'exer_id':exer_id})
    data=await state.get_data()
    mas=data['mas']
    text=last_result_for_excersize(exer_id)
    tren_id=data['tren_id']
    index=0
    a=get_workouts(tren_id)
    for i in a:
        if int(exer_id)==int(i[1]):
            break
        index+=1
    await state.update_data({'index':index})
    
    await call.message.answer(text,reply_markup=new_keyboard_3(mas,tren_id,exer_id,index))

@dp.callback_query_handler(text_contains="workouts_add_level_")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите количество повторорений и вес с которым вы делали данное упражнение через пробел')
    await state.update_data({'index_2':int(call.data.split('_')[3])})
    await sport_add_state.Q1.set()

@dp.message_handler(state=sport_add_state.Q1)
async def productt(message:Message,state:FSMContext):
    a,b=message.text.split()
    if (not (a.isdigit()))or(not(b.isdigit())) :
         await message.answer('Это не число введите еще раз')
    else:
        a,b=int(a),int(b)
        data=await state.get_data()
        mas=data['mas']
        index=data['index']
        index2=data['index_2']
        tren_id=data['tren_id']
        exer_id=data['exer_id']
        if len(mas[index])>int(index2):
            mas[index][index2]=f'{a} повторений |{b} кг'
        else: mas[index].append(f'{a} повторений |{b} кг')
        await state.update_data({'mas':mas})
        await message.answer('Подход успешно добавлен',reply_markup=new_keyboard_3(mas,tren_id,exer_id,index))
        await state.reset_state(False)
        print(await state.get_data())

@dp.callback_query_handler(text_contains='workouts_level_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Введите количество повторорений и вес с которым вы делали данное упражнение через пробел')
    await state.update_data({'index_2':int(call.data.split('_')[2])})
    await sport_add_state.Q1.set()


@dp.callback_query_handler(text='workouts_finish')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    data=await state.get_data()
    tren_id=data['tren_id']
    mas=data['mas']
    mas_new=[]
    s=''
    a=get_workouts(tren_id)
    k=0
    for i in a:
        f=True
        count=0
        s+=i[0]+'\n'
        for i in mas[k]:
            count+=1
            f=False
            s+=f'Подход №{count} {i}\n'
        if f:
            s+=f'Упражнение не сделано\n'
        k+=1
        
    for i in mas:
        a=[]
        for q in i:
            b=q.split('|')
            a.append(f'{b[0].split()[0]}|{b[1].split()[0]}')
        mas_new.append(a)
    add_new_tren(tren_id,mas_new)
    await state.finish()
    

    await call.message.answer(f'Тренировка успешно добавлена в базу)\n\nИтоги тренировки\n{s}',reply_markup=start__keybord)




@dp.callback_query_handler(text='look_last_sport')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите за какое время хотите посомтреть историю тренировок',reply_markup=sport_history_keyboard)

@dp.callback_query_handler(text_contains='history_sport_time_')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer( history_of_workout(int(call.data.split('_')[3])),reply_markup=start__keybord)

#доп функции

@dp.callback_query_handler(text='sport_data')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer('Выберите функцию:',reply_markup=sport_data_keyboard)

@dp.callback_query_handler(text='new_plan_sport')
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.set_data({'mas':[]})
    await call.message.answer('Выберите упражнение, которое хотите добавить в программу:',reply_markup=new_keyboard_5([]))

@dp.callback_query_handler(text_contains="new_sport_program_")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    id=int(call.data.split('_')[3])
    a=get_all_exsersize()
    data=await state.get_data()
    mas=data['mas']
    mas.append(id)
    for i in a:
        if id ==int(i[1]):
            name=i[0]
    await state.set_data({'mas':mas})
    await call.message.answer(f'Вы выбрали упражнение под название {name}, хотите добавить еще одно упражнение',reply_markup=new_keyboard_5(mas))

@dp.callback_query_handler(text="finish_new_sport_program")
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await sport_add_new_program_state.Q1.set()
    a=get_all_exsersize()
    data=await state.get_data()
    mas=data['mas']
    s='Ваша программа состоит из следущих упражений:\n'
    for id in mas:
        for i in a:
            if id ==int(i[1]):
                s+=i[0]+'\n'
    s+='Если все хорошо напишите название программы иначе отмена'
    await call.message.answer(s)

@dp.message_handler(Text(equals='отмена',ignore_case=True),state=sport_add_new_program_state.Q1)
async def productt(message:Message,state:FSMContext):
    await state.finish()
    await message.answer('Начините все заново(',reply_markup=sport_data_keyboard)

@dp.message_handler(state=sport_add_new_program_state.Q1)
async def productt(message:Message,state:FSMContext):
    texet=message.text
    await state.update_data({'name':texet})
    await message.answer(f'Вы ввели такое название {texet}\n Все верно?',reply_markup=sport_yes_no_keyboard)

@dp.callback_query_handler(text='sport_yes_1',state=sport_add_new_program_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    data=await state.get_data()
    await state.finish()
    add_new_workouts(data['mas'],data['name'])
    await call.message.answer('Программа тренировок успено добавлена',reply_markup=start__keybord)

@dp.callback_query_handler(text='sport_no_1',state=sport_add_new_program_state.Q1)
async def productt(call: CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Напишите название программы или отмена")