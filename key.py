from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton


def start_button():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Заполнить рабочие часы')
	menu.add(num1)
	return menu


def places(list1):
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	for el in list1:
		num1 = KeyboardButton(el[1])
		menu.add(num1)
	return menu


def hours():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Нормальные')
	num2 = KeyboardButton('Сверхурочные')
	num3 = KeyboardButton('Выходные')
	menu.add(num1).add(num2).add(num3)
	return menu


def comment():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Да')
	num2 = KeyboardButton('Нет')
	menu.add(num1).add(num2)
	return menu


def save():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Сохранить')
	num2 = KeyboardButton('Ввести заново')
	menu.add(num1).add(num2)
	return menu


def start():
	menu = InlineKeyboardMarkup(resize_keyboard=True)
	num1 = InlineKeyboardButton( text="Начать", callback_data='start_bot' )
	menu.add(num1)
	return menu


def admin():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Зарегестрировать пользователя')
	num2 = KeyboardButton('Удалить пользователя')
	num3 = KeyboardButton('Найти в базе')
	num4 = KeyboardButton('Новая таблица Excel')
	num5 = KeyboardButton('Редактировать кнопки')
	menu.add(num1).add(num2).add(num3).add(num4,num5)
	return menu


def search_db():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Поиск по фамилии')
	num2 = KeyboardButton('Поиск по номеру')
	menu.add(num1).add(num2)
	return menu


def month():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Янв')
	num2 = KeyboardButton('Фев')
	num3 = KeyboardButton('Апр')
	num4 = KeyboardButton('Март')
	num5 = KeyboardButton('Май')
	num6 = KeyboardButton('Июнь')
	num7 = KeyboardButton('Июль')
	num8 = KeyboardButton('Авг')
	num9 = KeyboardButton('Сен')
	num10 = KeyboardButton('Окт')
	num11 = KeyboardButton('Ноя')
	num12 = KeyboardButton('Дек')
	menu.add(num1,num2,num3).add(num4,num5,num6).add(num7,num8,num9).add(num10,num11,num12)
	return menu


def edit_place(arg):
	menu = InlineKeyboardMarkup(resize_keyboard=True)
	num1 = InlineKeyboardButton( text="Изменить", callback_data='edit_place_'+str(arg))
	num2 = InlineKeyboardButton( text="Удалить", callback_data='delete_place_'+str(arg))
	menu.add(num1,num2)
	return menu


def select_value():
	menu = InlineKeyboardMarkup(resize_keyboard=True)
	num1 = InlineKeyboardButton( text="Полное", callback_data='select_value_0')
	num2 = InlineKeyboardButton( text="Сокращённое", callback_data='select_value_1')
	menu.add(num1).add(num2)
	return menu


def new_place():
	menu = InlineKeyboardMarkup(resize_keyboard=True)
	num1 = InlineKeyboardButton( text="Добавить новую кнопку", callback_data='new_place')
	menu.add(num1)
	return menu


def cancel():
	menu = ReplyKeyboardMarkup(resize_keyboard=True)
	num1 = KeyboardButton('Отменить')
	menu.add(num1)
	return menu