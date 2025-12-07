from datetime import datetime

# Глобальні лічильники для ID
user_id_counter = 1
category_id_counter = 1
record_id_counter = 1

# Сховища
users = {}
categories = {}
records = {}

def get_next_user_id():
    global user_id_counter
    current_id = user_id_counter
    user_id_counter += 1
    return current_id

def get_next_category_id():
    global category_id_counter
    current_id = category_id_counter
    category_id_counter += 1
    return current_id

def get_next_record_id():
    global record_id_counter
    current_id = record_id_counter
    record_id_counter += 1
    return current_id
