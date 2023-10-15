import logging
import os
import telebot
import openai
from setup import *
from bottoms import *
from telebot import types
from sqlalchemy import *

def first_contact(prompt, chat_id):
    prev = conn.execute(text(f"SELECT history FROM id{chat_id}chats WHERE name = 'Robert'")).fetchone()
    prev = prev[0] if prev else ''
    if not prev:
        start_text = f"As a psychologist, I am here to work with you " \
                     "and help you work through any issues you may be facing. " \
                     "Please feel free to ask me any questions or share any concerns you may have. " \
                     "As your therapist, I promise to be empathetic, nonjudgmental, and supportive throughout this process. " \
                     "With that said, let's begin.".replace("'", "")
        conn.execute(text(f"UPDATE id{chat_id}chats SET history = '{start_text}' WHERE name = 'Robert'"))
        prev = start_text
    prompt = f"Psychologist: {prompt} Patient: "
    completions = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    if message.strip() == '':
        return "I don't get it, can you repeat?"
    result = prev + prompt + message.replace("\n", "")
    result = result.replace("'", "")
    conn.execute(text(f"UPDATE id{chat_id}chats SET history = '{result}' WHERE name = 'Robert'"))
    return message.strip()

def remove_quotes(name):
  if name[0] == '"' and name[-1] == '"':
    return name[1:-1]
  else:
    return name


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    result = conn.execute(text(f"SELECT to_regclass('public.id{chat_id}hero')"))
    table_exists = result.fetchone()[0]
    if not table_exists:
        conn.execute(text(f'create table id{chat_id}hero(name varchar,money int,outfit varchar);'))
        conn.execute(text(f'create table id{chat_id}chats(name varchar,sympathy int, active int, duration int, '
                          f'history TEXT NOT NULL, '
                          f'CONSTRAINT '
                          f'sympathy CHECK '
                          f'(sympathy BETWEEN 1 AND 10));'))
    bot.send_message(chat_id=chat_id, text="Please select your gender:", reply_markup=reply_choise)

def send_image(chat_id, image_path, gender):
    yes = types.InlineKeyboardButton("Yes", callback_data=f"{gender}_yes")
    no = types.InlineKeyboardButton("No", callback_data=f"{gender}_no")
    keyboard = [[yes, no]]
    reply_sure = types.InlineKeyboardMarkup(keyboard)
    bot.send_photo(chat_id, photo=open(image_path, 'rb'))
    bot.send_message(chat_id, "Are you sure?", reply_markup=reply_sure)

@bot.callback_query_handler(func=lambda query: True)
def button_callback(query):
    chat_id = query.message.chat.id
    if query.data == button_data("male_button"):
        send_image(chat_id, "characters/m_psychologist.png", "male")
    elif query.data == button_data("female_button"):
        send_image(chat_id, "characters/f_psychologist.png", "female")
    elif "yes" in query.data:
        if "female" in query.data:
            bot.send_message(chat_id, "Starting the game")
            conn.execute(text(f"insert into id{chat_id}hero values('Ava',0,'classic');"))
            result = conn.execute(text(f"SELECT name FROM id{chat_id}hero"))
            name = result.fetchone()[0]
            clean_name = remove_quotes(name)
            with open("texts/1prologue.txt", "r") as f:
                prologue = f.read()
            prologue = prologue.replace("{name}", clean_name)
            bot.send_message(chat_id, prologue, reply_markup=reply_markup2)
        else:
            bot.send_message(chat_id, "Starting the game")
            conn.execute(text(f"insert into id{chat_id}hero values('Ethan',0,'classic');"))
            result = conn.execute(text(f"SELECT name FROM id{chat_id}hero"))
            name = result.fetchone()[0]
            clean_name = remove_quotes(name)
            with open("texts/1prologue.txt", "r") as f:
                prologue = f.read()
            prologue = prologue.replace("{name}", clean_name)
            bot.send_message(chat_id, prologue, reply_markup=reply_markup2)
    elif query.data == button_data("continue1"):
        conn.execute(text(f"insert into id{chat_id}chats values('Robert', 7, 0, 10, '');"))
        with open("texts/2prologue.txt", "r") as f:
            prologue2 = f.read()
        bot.send_message(chat_id, prologue2, reply_markup=reply_markup3)
    elif query.data == button_data("continue2"):
        with open("texts/tutorial.txt", "r") as f:
            tutorial1 = f.read()
        bot.send_message(chat_id, tutorial1)
    elif "no" in query.data:
        bot.send_message(chat_id=chat_id, text="Please select your gender:", reply_markup=reply_choise)
    elif query.data == button_data("take_card"):
        with open("texts/4prologue.txt", "r") as f:
            prologue = f.read()
        with open('locations/office.jpg', 'rb') as f2:
            bot.send_photo(chat_id=chat_id, photo=f2)
        bot.send_message(chat_id=chat_id, text=prologue, reply_markup=reply_home)
    elif query.data == button_data("go_home"):
        with open('locations/home.png', 'rb') as f2:
            bot.send_photo(chat_id=chat_id, photo=f2)
        bot.send_message(chat_id=chat_id, text='Today was the day, I need some rest', reply_markup=reply_sleep)
    elif query.data == button_data("go_sleep"):
        with open('locations/home_m.png', 'rb') as f2:
            bot.send_photo(chat_id=chat_id, photo=f2)
        bot.send_message(chat_id=chat_id, text='So I woke up early morning for this? Anyway I dont want to sleep, so'
                                               'lets find out what is wrong with this academy', reply_markup=reply_academy)
    elif query.data == button_data("go_academy"):
        with open("texts/5prologue.txt", "r") as f:
            prologue = f.read()
        with open('locations/train_station.png', 'rb') as f2:
            bot.send_photo(chat_id=chat_id, photo=f2)
        bot.send_message(chat_id=chat_id, text=prologue,
                         reply_markup=reply_train)
    elif query.data == button_data("go_train"):
        bot.send_message(chat_id=chat_id, text="", reply_markup=reply_train)

@bot.message_handler(commands=['list'])
def speak_command(message):
    chat_id = message.chat.id
    result = conn.execute(text(f"SELECT name FROM id{chat_id}chats"))
    names = [row[0] for row in result]
    if not names:
        bot.send_message(chat_id, "You can't talk to anyone")
    else:
        bot.send_message(chat_id, f"You can speak with: {', '.join(names)}")

@bot.message_handler(content_types=['text'], func=lambda message: message.text.startswith('/speak'))
def speak_person(message):
    chat_id = message.chat.id
    text_message = message.text.split()
    if len(text_message) < 2:
        bot.send_message(chat_id, "Please enter a name after the `/speak` command")
    else:
        name = text_message[1]
        result = conn.execute(text(f"SELECT name FROM id{chat_id}chats"))
        names = [row[0] for row in result]
        if name not in names:
            bot.send_message(chat_id, f"You can't talk to {name}")
        else:
            bot.send_message(chat_id, f"You speak with {name}")
            conn.execute(text(f"UPDATE id{chat_id}chats SET active = 1 WHERE name = '{name}';"))

@bot.message_handler(content_types=['text'])
def callback_query(message):
    chat_id = message.chat.id
    result_r = conn.execute(text(f"SELECT active, duration FROM id{chat_id}chats where name = 'Robert'")).fetchone()
    if result_r and result_r[0] == 1 and int(result_r[1]) > 0:
        conn.execute(text(f"UPDATE id{chat_id}chats set duration = duration-1"))
        bot.send_message(chat_id, first_contact(message.text, chat_id))
    if result_r and result_r[0] == 1 and int(result_r[1]) == 0:
        name = conn.execute(text(f"SELECT name FROM id{chat_id}hero")).fetchone()[0]
        with open("texts/3prologue.txt", "r") as f:
            prologue = f.read()
        prologue = prologue.replace('name', name)
        conn.execute(text(f"UPDATE id{chat_id}chats set active = 0 where name = 'Robert'"))
        bot.send_message(chat_id, prologue, reply_markup=reply_card)

def main():
    bot.polling()

if __name__ == '__main__':
    main()
