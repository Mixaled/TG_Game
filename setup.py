import logging
import os
import telebot
import openai
from config import *
from sqlalchemy import *

openai.api_key = api
engine = create_engine(engine_sql)
engine.connect()
conn = engine.connect()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"] = telegram_api
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
