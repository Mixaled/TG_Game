from test import generate_response, update_history
from conversation import conversation_Victoria
from config import conn
from sqlalchemy import text
import json


if __name__ == "__main__":
    i=0
    while i <= 10:
        user_input = input("You: ")
        update_history(user_input + "\nVictoria:", "user", "TestUser")
        chat_info = conn.execute(text("select chat from chat_info where user_name = 'TestUser'")).fetchone()
        chat_list = json.loads(chat_info[0]) if chat_info else []
        response = generate_response(chat_list)
        update_history(response, "system", "TestUser")
        print("AI: ",response)
        i+=1
