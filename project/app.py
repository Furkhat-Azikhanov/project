from flask import Flask, request, jsonify  # Импорт Flask для создания веб-приложения
from tinydb import TinyDB, Query  # Импорт TinyDB для работы с базой данных
import re  # Импорт модуля регулярных выражений для валидации
import logging  # Импорт модуля логирования
import traceback  # Импорт модуля для обработки ошибок
import os  # Импорт модуля для работы с файловой системой

# Инициализация Flask приложения
app = Flask(__name__)

# Проверяем, существует ли файл базы данных, если нет, создаем его
if not os.path.exists('forms_db.json'):
    with open('forms_db.json', 'w') as f:
        f.write('{}')  # Создаем пустую базу данных

# Инициализация базы данных TinyDB
db = TinyDB('forms_db.json')  # Открываем или создаем файл базы данных
forms_table = db.table('forms')  # Создаем или получаем таблицу "forms" из базы

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Устанавливаем уровень логирования на INFO
logger = logging.getLogger(__name__)  # Создаем объект логгера

# Начальные данные для таблицы (шаблоны форм)
default_forms = [
    {
        "name": "User Registration",  # Название шаблона
        "user_email": "email",  # Поле с типом email
        "user_phone": "phone"  # Поле с типом phone
    },
    {
        "name": "Order Form",  # Название шаблона
        "order_date": "date",  # Поле с типом date
        "customer_email": "email"  # Поле с типом email
    }
]

# Заполняем таблицу, если она пуста
try:
    if not forms_table.all():  # Проверяем, есть ли данные в таблице
        forms_table.insert_multiple(default_forms)  # Добавляем начальные шаблоны
        logger.info("Default forms added to the database.")  # Логируем успешное добавление
except Exception as e:
    logger.error(f"Error initializing database: {e}")  # Логируе