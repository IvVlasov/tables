import yadisk
import openpyxl
from datetime import datetime, date, time 
import calendar



ident = 'yandex_token'
secret = 'other_yandex_token'
TOKEN = 'and_again_other_yandex_token'

y = yadisk.YaDisk(ident, secret, TOKEN)
words = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AJ']
week= ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб','Вс']

def doc_name():
	date = datetime.today().date()
	name = str(date).split('-')[0] +'-'+ str(date).split('-')[1]
	return name


def open_doc():
	name = doc_name()
	y.download("/KonturTable/"+name+".xlsx", name+'.xlsx')
	print(name+ '.xlsx')
	book = openpyxl.load_workbook(name + '.xlsx')
	return book


def find_col(book):
	sheet = book['1']
	for el in sheet['2']:
		if str(el.value).split(' ')[0] == str(datetime.today().date()):
			return words[el.column]

def find_row(fio,book):
	sheet = book['1']
	rows = []
	for el in sheet['A']:
		if el.value == fio:
			rows.append(el.row)
	return rows


def update_excel_file():
	name = doc_name()
	y.remove("/KonturTable/"+name+".xlsx")
	y.upload(name+".xlsx", "/KonturTable/"+name+".xlsx")
	

def set_new_value(value, arg,place, comment, fio):
	book = open_doc()
	name = doc_name()
	row = find_row(fio, book)
	col = find_col(book)
	if comment:
		result = 'Место:' + str(place) + '\nКомментарий: ' + str(comment)
	else:
		result = 'Место:' + str(place)

	book['1'][col+str(row[arg])] = str(value)
	book['1'][col+str(row[arg+1])] = str(result)
	book.save(name+'.xlsx')
	book.close()
	update_excel_file()


def create_new_table(arg):
	name = arg
	book = open_doc()
	sheet = book['1']
	cal = calendar.Calendar().itermonthdates(int(name.split('-')[0]),int(name.split('-')[1]))
	for el in sheet.rows:
		for i in el:
			if i.column in range(3,40):
				i.value =' '
	counter = 1
	for i, el in enumerate(cal):
		if el.month == int(name.split('-')[1]):
			counter+=1
			sheet['2'][counter].value = el
			sheet['1'][counter].value = week[el.weekday()]


	book.save(name+'.xlsx')
	y.upload(name+".xlsx", "/KonturTable/"+name+".xlsx")

