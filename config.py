from aiogram import  Bot , Dispatcher 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import data





# Токен телеграм бота, получается у BotFather
TOKEN = "1881930823:AAEgqcodVvh-im7UjgxgKbUzgRpugZbHs2Y"

admins_list = [383987028, 1649920181]


list_hours = ['Нормальные',' ',  'Сверхурочные',' ', 'Выходные', ' ']


months = [' ', 'Янв', 'Фев','Март', 'Апр','Май','Июнь','Июль','Авг','Сен','Окт','Ноя','Дек']
connection = data.create_connection('db.sql')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


