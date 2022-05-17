from environs import Env
import os

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

#pip install python-dotenv      | from dotenv import load_dotenv | load_dotenv()

BOT_TOKEN = env.str('BOT_TOKEN')  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

