from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
import yfinance as yf
import sqlite3
from datetime import datetime

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

stocks = {"apple": "AAPL", "microsoft": "MSFT", "tesla": "TSLA", "yandex": "YNDX", "facebook": "FB", 
"amazon": "AMZN", "google": "GOOGL", "netflix": "NFLX"}

@dispatcher.message_handler(commands=["start"])
async def start(message: types.Message):
	msg = "Hello, this bot can only show you current stock price of one of that companies, just write one of the names from the list:"
	for i in stocks:
		msg += "\n"
		msg += i
	await message.reply(msg)

@dispatcher.message_handler(commands=[i for i in stocks])
async def get_price(message: types.Message):
	company = message["text"][1:]
	ticker = yf.Ticker(stocks[company])
	price = ticker.info['regularMarketPrice']
	current_datetime = datetime.now().strftime("%B %d, %Y %I:%M%p")
	try:
		connection = sqlite3.connect("resources/stocks")
		cursor = connection.cursor()
		request = f'insert into stocks(datetime, name, price) values("{current_datetime}", "{company}", {price});'
		cursor.execute(request)
		print("Added")
		cursor.close()
	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite", error)
	finally:
		if (connection):
			connection.close()
			print("Соединение с SQLite закрыто")
	reply = message["text"][1:]+": "+str(price)+"$"
	await bot.send_message(message.from_user.id, reply)

if __name__ == "__main__":
	executor.start_polling(dispatcher)