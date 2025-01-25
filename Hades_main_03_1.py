import os
import sqlite3
import telebot
import requests
import hashlib
from telebot import types


BOT_TOKEN = '8109252390:AAHj4zJFKVaQlkSVKs0cxqwh-0e4sHN2HOA'
API_KEY = '8cc50dc027bf6ecbbb43c26cddfef271'


bot = telebot.TeleBot(BOT_TOKEN)


DB_NAME = 'stalker.sdb'


def create_user_table():
    conn = sqlite3.connect(DB_NAME)
    with conn:
        conn.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                pass_hash TEXT
            )
        ''')
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


@bot.message_handler(commands=['start', 'main', 'hello'])
def start_registration(message):
    create_user_table()
    bot.send_message(message.chat.id, 'Hello! Let’s start the registration. What is your name?')
    bot.register_next_step_handler(message, get_user_name)

def get_user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter your password:')
    bot.register_next_step_handler(message, get_user_password)

def get_user_password(message):
    password = message.text.strip()
    password_hash = hash_password(password)


    conn = sqlite3.connect(DB_NAME)
    with conn:
        conn.execute('INSERT INTO users (name, pass_hash) VALUES (?, ?)', (name, password_hash))
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('List of users', callback_data='users'))
    bot.send_message(message.chat.id, 'You have been successfully registered!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'users')
def show_users(call):
    conn = sqlite3.connect(DB_NAME)
    with conn:
        users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    info = '\n'.join([f'Name: {user[1]}, Password: {user[2]}' for user in users])
    bot.send_message(call.message.chat.id, info)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '<b>Help:</b> <em>Information about the bot</em>', parse_mode='html')
    

    help_file_path = 'List of Features and Help.txt'
    

    if os.path.exists(help_file_path):
        with open(help_file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "Help file not found.")


@bot.message_handler(func=lambda message: message.text.lower() == 'hi')
def greet_user(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}!')

@bot.message_handler(func=lambda message: message.text.lower() == 'my id')
def send_user_id(message):
    bot.reply_to(message, f'Your ID: {message.from_user.id}')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Go to website', url='https://google.com'))
    markup.add(types.InlineKeyboardButton('Delete photo', callback_data='delete'))
    markup.add(types.InlineKeyboardButton('Edit text', callback_data='edit'))
    bot.reply_to(message, 'Photo received!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Text has been changed', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['weather'])
def ask_city(message):
    bot.send_message(message.chat.id, 'Enter the name of your city to get the weather forecast:')

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text.strip().lower()
    if city == '/weather':
        return

    bot.send_message(message.chat.id, f'Getting weather data for the city: {city.capitalize()}...')

    try:
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en')

        if res.status_code == 200:
            data = res.json()
            if "main" in data:
                temp = data["main"]["temp"]
                weather_description = data["weather"][0]["description"]

                bot.reply_to(message, f'Temperature in {city.capitalize()}: {temp}°C. Weather: {weather_description}.')

                image = 'free-icon-sun-4814275.png' if temp > 25.0 else 'free-icon-sunny-4810371.png'

                if os.path.exists(image):
                    with open(image, 'rb') as file:
                        bot.send_photo(message.chat.id, file)
                else:
                    bot.send_message(message.chat.id, "Image not found.")
            else:
                bot.reply_to(message, "Failed to get weather data for this city.")
        else:
            bot.reply_to(message, "Error retrieving data from OpenWeather API. Try again later.")
    except Exception as e:
        bot.reply_to(message, "An error occurred while making the request. Try again later.")
        print(f"Error: {e}")


def start_bot():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Error with the bot: {e}")
            time.sleep(15)


if __name__ == '__main__':
    start_bot()
