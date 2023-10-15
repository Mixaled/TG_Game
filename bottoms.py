from telebot import types

class Button:
    def __init__(self, name, callback_data):
        self.name = name
        self.callback_data = callback_data

    def get_button(self):
        return types.InlineKeyboardButton(self.name, callback_data=self.callback_data)

button_map = {}

def button(button_id, button_title):
    button_map[button_id] = Button(button_title, button_id)

def button_data(button_id):
    return button_map[button_id].callback_data

def button_reply(button_id):
    return button_map[button_id].name

button("male_button", "Male")
button("female_button", "Female")
button("continue1", "Continue")
button("continue2", "Continue")
button("continue3", "Continue")
button("take_card", "Take card")
button("continue4", "Continue")
button("continue5", "Continue")
button("go_home", "Go Home")
button("go_academy", "Go to Academy")
button("go_sleep", "Go to Sleep")
button("go_train", "Go to Train")
button("continue6", "Continue")

reply_choise = types.InlineKeyboardMarkup([[button_map["male_button"].get_button(), button_map["female_button"].get_button()]])
reply_markup2 = types.InlineKeyboardMarkup([[button_map["continue1"].get_button()]])
reply_markup3 = types.InlineKeyboardMarkup([[button_map["continue2"].get_button()]])
reply_markup4 = types.InlineKeyboardMarkup([[button_map["continue3"].get_button()]])
reply_markup5 = types.InlineKeyboardMarkup([[button_map["continue4"].get_button()]])
reply_home = types.InlineKeyboardMarkup([[button_map["go_home"].get_button()]])
reply_academy = types.InlineKeyboardMarkup([[button_map["go_academy"].get_button()]])
reply_sleep = types.InlineKeyboardMarkup([[button_map["go_sleep"].get_button()]])
reply_card = types.InlineKeyboardMarkup([[button_map["take_card"].get_button()]])
reply_train = types.InlineKeyboardMarkup([[button_map["go_train"].get_button()]])
