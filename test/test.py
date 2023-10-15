import openai
import json
from sqlalchemy import *

# Common pricol
from conversation import conversation_Victoria
from config import *

openai.api_key = openai_api
chat_json = json.dumps(conversation_Victoria, ensure_ascii=False)
query_exec1 = f"""
create or replace procedure update_chat_info(in p_username varchar, in p_add json)
language plpgsql
as $$
begin
    if p_username not in (select user_name from chat_info) then
        insert into chat_info (user_name, chat) values (p_username, '{chat_json}'::json);
    else
         update chat_info SET chat = p_add where user_name = p_username;
    end if;
end;
$$;
"""
conn.execute(text(query_exec1))
conn.commit()
print("update_chat_info created or replaced...")


def update_history(message, role, user_name):
    message = message.replace("'", "`")
    info_json = chat_json
    info = conn.execute(
        text(f"SELECT chat FROM chat_info WHERE user_name = '{user_name}'")).fetchall()
    
    if info:
        new_message = {"role": role, "content": message}
        #print(f"UPDATING DATA as {role}")
        chat_list_json = info[0][0]  
        chat_list = json.loads(chat_list_json)
        chat_list.append(new_message)
        info_json = json.dumps(chat_list, ensure_ascii=False)
        conn.execute(
            text(f"CALL update_chat_info('{user_name}', '{info_json}')"))
        #print("DATA COMMITTED")
        conn.commit()
    else:
        conn.execute(
            text(f"CALL update_chat_info('{user_name}', '{info_json}')"))
        update_history(message, role, user_name)
        #print(f"No chat info found for user {user_name}")


def generate_response(conversation):
    #print(conversation)
    #print("GENERATING RESPONSE")
    if conversation == []:
        return "I don't know"
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.2
        )
    #print(f"generated: {response.choices[0].message.content}")
    return response.choices[0].message.content
