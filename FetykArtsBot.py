import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8602833587:AAFN7QObHBM-tRX-IvZGC-XdYTvzFoWYgLk'
API_KEY = 'e47c6a3e8f686acca7b6eae7cc17b4fd'
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'
EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀️',
              801: '🌤',
              802: '☁️',
              803: '☁️',
              804: '☁️'}

bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_weather = KeyboardButton('Получить погоду', request_location=True)
btn_about = KeyboardButton('О проекте')
keyboard.add(btn_weather, btn_about)

def get_weather(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru',
        'units': 'metric',
        'appid': API_KEY
    }
    try:
        response = requests.get(URL_WEATHER_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        city = data.get('name', 'неизвестный город')
        weather = data['weather'][0]
        desc = weather.get('description', '')
        w_id = weather.get('id', 0)
        temp = data['main'].get('temp', 0)
        feels_like = data['main'].get('feels_like', 0)
        humidity = data['main'].get('humidity', 0)
        emoji = EMOJI_CODE.get(w_id, '🌈')
        message = (
            f"Погода в: {city}\n"
            f"{emoji} {desc.capitalize()}.\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Влажность: {humidity}%"
        )
        return message
    except requests.exceptions.RequestException:
        return "Ошибка при запросе к серверу погоды. Попробуйте позже."
    except (KeyError, IndexError, ValueError):
        return "Не удалось обработать данные о погоде. Попробуйте позже."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "Привет! Я бот, который расскажет о погоде.\n"
        "Отправь мне своё местоположение, и я скажу погоду."
    )
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(func=lambda msg: msg.text == 'О проекте')
def send_about(message):
    about = (
        "Проект «Telegram‑бот для погоды»\n"
        "Автор: Илья Б.\n"
        "Бот создан с использованием:\n"
        "телеграмма, пайтона и API источников.\n"
        "Для вопросов не предназначен."
    )
    bot.send_message(message.chat.id, about, reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    lat = message.location.latitude
    lon = message.location.longitude
    weather_info = get_weather(lat, lon)
    bot.send_message(message.chat.id, weather_info, reply_markup=keyboard)

@bot.message_handler(func=lambda msg: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Используй кнопочки",
        reply_markup=keyboard
    )

if __name__ == '__main__':
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()