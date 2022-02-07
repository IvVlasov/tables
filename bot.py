from aiogram import  executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, dp, list_hours, connection, admins_list,months
import logging 
import key
import yan
import data as db




logging.basicConfig(level=logging.INFO)

@dp.message_handler( commands=['start'])
async def echo(message:types.Message):
	if db.find_chat_id(connection, message.chat.id) == 'DONE':
		await message.answer('Приветствую, вы хотите ввести рабочие часы?', reply_markup = key.start_button())
	else:
		await message.answer('Приветствую, я телеграм бот, который поможет тебе ввести данные о своей работе\n\n Для использоватния бота вам необходимо сообщить регистрационный номер вашему админу. Ваш номер:\n \n `'+ str(message.chat.id) + '`\n\nПосле регистрация в системе вы сможете пользоваться ботом', parse_mode = 'Markdown')



class Form(StatesGroup):
    place = State()  
    hours = State()  
    count = State()
    comment = State()
    save = State()


@dp.message_handler(lambda message:message , text='Заполнить рабочие часы')
async def echo(message:types.Message):
	list_places = db.read_buts(connection)
	await Form.place.set()
	await message.answer('Выберите место, где вы сегодня работали', reply_markup= key.places(list_places))


@dp.message_handler(lambda message: message.text, state=Form.place)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(place=message.text)
    await message.reply("Выберите 	тип отработанных часов", reply_markup =key.hours())


@dp.message_handler(lambda message: message.text, state=Form.hours)
async def process_age(message: types.Message, state: FSMContext):
	if message.text == 'Нормальные':
		await state.update_data(hours=0)
	elif message.text =='Сверхурочные':
		await state.update_data(hours=2)
	elif message.text =='Выходные':
		await state.update_data(hours=4)
	await Form.next()
	await message.reply("Введите количество отработанных часов", reply_markup =types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text, state=Form.count)
async def process_age(message: types.Message, state: FSMContext):
	if message.text.replace(".", "").isdigit():
	    await state.update_data(count=message.text)
	    await Form.next()
	    await message.reply("Хотите оставить комментарий?", reply_markup =key.comment())
	else: 
	    await message.answer('Вы можете ввести только число.')


@dp.message_handler(lambda message: message.text=='Да' , state=Form.comment)
async def process_age(message: types.Message, state: FSMContext):
	# await Form.next()
    await message.answer("Введите комментарий", reply_markup =types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text , state=Form.comment)
async def process_age(message: types.Message, state: FSMContext):
	if message.text == 'Нет':
		await state.update_data(comment='')
	elif message.text != 'Да':
		await state.update_data(comment=message.text)
	else:
		pass

	async with state.proxy() as data:
            await message.answer('Проверьте правильность введённых данных\n'+'Место работы: '+ str(data['place'])+ '\nТип часов: ' + str(list_hours[data['hours']]) + '\nКоличество часов: ' + str(data['count']) + '\nКомментарий: ' + str(data['comment']) + '\n\nЕсли всё правильно, нажмите кнопку "Сохранить" ', reply_markup=key.save())
	await Form.next()


@dp.message_handler(lambda message: message.text, state=Form.save)
async def process_age(message: types.Message, state: FSMContext):
	if message.text == 'Сохранить':
		fio = db.read_fio(connection,  message.chat.id)
		try: 
			async with state.proxy() as data:
				place = db.find_place(connection, data['place'])
				yan.set_new_value(data['count'], data['hours'], place,  data['comment'], fio)
			yan.update_excel_file()
			await message.answer("Спасибо, "+ str(db.read_name(connection,message.chat.id))+ ' ' +str(db.read_patronymic(connection,message.chat.id))+"! Желаем хорошего отдыха!", reply_markup =key.start_button())
			await state.finish()
		except:
			await message.answer("Произошла ошибка, возможно вашего имени нет в таблице Excel, или оно написано неправильно.\nОбратитесь к администратору бота. Ваше имя должно быть записано: "+ str(fio) , reply_markup =key.start_button())
			await state.finish()

	if message.text == 'Ввести заново':
		await message.answer("Данные удалены, нажмите кнопку что бы начать заново", reply_markup =key.start_button())
		await state.finish()

#################################################################################
###################################	ADMIN PANEL #################################
#################################################################################

@dp.message_handler(lambda message:message.chat.id in admins_list, commands=['adm'] )
async def echo(message:types.Message):
	await message.answer('Вы перешли в панель администратора', reply_markup = key.admin())

# @dp.message_handler(lambda message:message.chat.id in admins_list, commands=['test'] )
# async def echo(message:types.Message):
# 	a= db.read_fio(connection,  message.chat.id)

# 	await message.answer(a)

class Delete(StatesGroup):
    num = State() 

class Create(StatesGroup):
    month = State() 
    year = State()

class Search(StatesGroup):
    number = State() 
    surname = State() 

class Register(StatesGroup):
    surname = State() 
    name = State()  
    patronymic = State()
    ident = State()
    save = State()

@dp.message_handler(lambda message:message.chat.id in admins_list)
async def echo(message:types.Message):
	if message.text == 'Зарегестрировать пользователя':
		await message.answer('Введите фамилию нового пользователя', reply_markup= types.ReplyKeyboardRemove())
		await Register.surname.set()

	if message.text == 'Удалить пользователя':
		await Delete.num.set()
		await message.answer('Введите номер пользователя на удаление')

	if message.text == 'Найти в базе':
		await message.answer('Выберите вариант поиска в базе', reply_markup = key.search_db())

	if message.text == 'Новая таблица Excel':
		await message.answer('Выберите месяц', reply_markup = key.month())
		await Create.month.set()

	if message.text == 'Редактировать кнопки':
		list_places = db.read_buts(connection)
		await Edit_but.ident.set()

		await message.answer('Выберите кнопку для изменения', reply_markup = key.new_place())
		await message.answer('.', reply_markup = key.cancel())
		for el  in list_places:
			await message.answer('Полное название: '+ el[1] + '\nСокращенное: ' + el[2], reply_markup = key.edit_place(el[0]))


	if message.text == 'Поиск по фамилии':
		await Search.surname.set()
		await message.answer('Введите фамилию сотрудника', reply_markup= types.ReplyKeyboardRemove())

	if message.text == 'Поиск по номеру':
		await Search.number.set()
		await message.answer('Введите регистрационный номер сотрудника', reply_markup= types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.chat.id in admins_list, state=Delete.num)
async def process_age(message: types.Message, state: FSMContext):
	if message.text.isdigit():
		try:
			db.delete_user(connection, int(message.text))
			await message.answer('Пользователь успешно удалён')
			await state.finish()
		except: 
			await message.answer('Что то пошло не так, возможно такого пользователя не существует')


@dp.message_handler(lambda message:	message.chat.id in admins_list, state=Register.surname)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await Register.next()
    await message.answer('Введите имя нового пользователя')

@dp.message_handler(lambda message: message.chat.id in admins_list, state=Register.name)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Register.next()
    await message.answer('Введите отчество нового пользователя')

@dp.message_handler(lambda message: message.chat.id in admins_list, state=Register.patronymic)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    await Register.next()
    await message.answer('Введите регистрационный номер нового пользователя')

@dp.message_handler(lambda message: message.chat.id in admins_list, state=Register.ident)
async def process_age(message: types.Message, state: FSMContext):
	if (message.text).isdigit():
	    await state.update_data(ident=int(message.text))
	    await Register.next()
	    async with state.proxy() as data:
	    	await message.answer('Отлично, проверьте правильность введённых данных и сохраните результат\n\nФамилия: ' + str(data['surname']) +'\nИмя: ' + str(data['name']) + '\nОтчество: ' + str(data['patronymic']) + '\nРегистрационный номер: ' + str(data['ident']) + '\n\n Если всё верно, нажмите кнопку "Сохранить"', reply_markup = key.save())
	else: 
	    await message.answer('Введённый номер должен быть целым числом, без букв')

@dp.message_handler(lambda message: message.text, state=Register.save)
async def process_age(message: types.Message, state: FSMContext):
	if message.text == 'Сохранить':
		async with state.proxy() as data:
			try: 
				db.set_new_user(connection, int(data['ident']), data['name'], data['surname'], data['patronymic'])
				await bot.send_message(data['ident'], text = str(data['name'])+' ' + str(data['patronymic']) + ', вы успешно зарегестрированы!', reply_markup = key.start_button())
				await message.reply("Пользователь зарегестрирован, он получит сообщение об успешной регистрации.", reply_markup =key.admin())
			except:
				if db.find_chat_id(connection, int(data['ident'])) == 'DONE':
					await message.answer('Такой пользователь уже существует в базе', reply_markup =key.admin())
				else:
					await message.answer('Произошла фатальная ошибка, попробуйте ещё раз или обратитесь к разработчику',reply_markup =key.admin())
				await state.finish()
		await state.finish()
	if message.text == 'Ввести заново':
		await message.reply("Данные удалены, нажмите кнопку что бы начать заново", reply_markup =key.admin())
		await state.finish()



@dp.message_handler(lambda message: message.chat.id in admins_list, state=Search.number)
async def process_age(message: types.Message, state: FSMContext):
	ident =  int(message.text)
	user = db.read_all(connection, ident)
	await message.answer(str(user), reply_markup =key.admin())
	await state.finish()

@dp.message_handler(lambda message: message.chat.id in admins_list, state=Search.surname)
async def process_age(message: types.Message, state: FSMContext):
	user = db.read_all_by_name(connection, message.text)
	await message.answer(str(user), reply_markup =key.admin())
	await state.finish()


@dp.message_handler(lambda message:	message.chat.id in admins_list, state=Create.month)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(month=months.index(message.text))
    await message.answer(message.text)
    await Create.next()
    await message.answer('Введите год в формате YYYY (Например 2021)')

@dp.message_handler(lambda message:	message.chat.id in admins_list, state=Create.year)
async def process_age(message: types.Message, state: FSMContext):
	if message.text.isdigit():
		await state.update_data(year=int(message.text))
		try:
			async with state.proxy() as data:
				result =''+ str(data['year']) + '-'+str(data['month'])
				yan.create_new_table(result)
				await message.answer('Документ создан и перенесен на Яндекс.диск', reply_markup =key.admin())
				await state.finish()
		except:
			async with state.proxy() as data:
				await message.answer('Что то пошло не так, попробуйте ещё раз или обратитесь к разработчику',reply_markup =key.admin())
				await message.answer(''+ str(data['year']) + '-'+str(data['month']),reply_markup =key.admin())

			await state.finish()
	else:
		await message.answer('Неверный формат даты')
		# await state.finish()

class Edit_but(StatesGroup):
	ident = State()
	argument = State()
	new_value = State()

@dp.callback_query_handler(lambda c: c.data.startswith('delete_place'), state = Edit_but.ident)
async def delete_anketa(call, state: FSMContext):

	try:
		arg = call.data.split('_')[2]
		await call.message.answer('Кнопка была удалена',reply_markup=key.admin())
		await state.finish()
	except:
		await call.message.answer('Возникла фатальная ошибка',reply_markup=key.admin())
		await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('new_place'), state = Edit_but.ident)
async def delete_anketa(call, state: FSMContext):
	try:
		db.new_button(connection)
		await call.message.answer('Кнопка создана, отредактируйте её в режиме редактирования',reply_markup=key.admin())
		await state.finish()
	except:
		await call.message.answer('Возникла фатальная ошибка',reply_markup=key.admin())
		await state.finish()

# GoLogin
@dp.callback_query_handler(lambda c: c.data.startswith('edit_place_'), state = Edit_but.ident)
async def delete_anketa(call, state: FSMContext):
	arg = call.data.split('_')[2]
	for i in range(int(arg)):
		if i == 0:
			continue
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id - i, text='.', reply_markup = None)
	for i in range(len(db.read_buts(connection)) - int(arg)):
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + i+1, text='.', reply_markup = None)
		

	# for i in range(len(db.read_buts(connection))):
	# 	await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id- int(arg), text='.', reply_markup = None)

	await state.update_data(ident=int(arg))
	await Edit_but.next()
	await call.message.answer('Какое значение будем менять?', reply_markup = key.select_value())


@dp.callback_query_handler(lambda c: c.data.startswith('select_value_'), state = Edit_but.argument)
async def delete_anketa(call, state: FSMContext):
	arg = call.data.split('_')[2]
	await state.update_data(argument=int(arg))
	await Edit_but.next()
	await call.message.answer('Введите новое значение' , reply_markup = types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.chat.id in admins_list, state=Edit_but.new_value)
async def process_age(message: types.Message, state: FSMContext):
	await state.update_data(new_value=message.text)
	try:
		async with state.proxy() as data:
			if data['argument'] == 0:
				db.update_place(connection, data['ident'], data['new_value'])
			elif data['argument'] == 1:
				db.update_small_place(connection,data['ident'], data['new_value'])
		await message.answer('Отлично, кнопка сохранена', reply_markup = key.admin())
	except:
		await message.answer('Что то пошло не так, попробуйте ещё раз', reply_markup = key.admin())
	await state.finish()

@dp.message_handler(lambda message: message.chat.id in admins_list, state='*')
async def process_age(message: types.Message, state: FSMContext):
	if message.text == 'Отменить':
			await message.answer('Ввод отменён', reply_markup=key.admin())
			await state.finish()




if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)



