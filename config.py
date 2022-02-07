from aiogram import  Bot , Dispatcher 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import data

# Токен телеграм бота, получается у BotFather
TOKEN = "Bot_token"

admins_list =[]#list of chat_id admins

list_hours = ['Нормальные',' ',  'Сверхурочные',' ', 'Выходные', ' ']
months = [' ', 'Янв', 'Фев','Март', 'Апр','Май','Июнь','Июль','Авг','Сен','Окт','Ноя','Дек']
connection = data.create_connection('db.sql')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


