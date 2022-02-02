from datetime import datetime
import json
from flask import Flask, request, render_template

app = Flask(__name__)

# dt_now = datetime.datetime.now()

# messages_list = [
#     {
#         "text": "Всем привет в этом чате!",
#         "sender": "Suka",
#         "date": "31-01-22 20:00",
#     },
#     {
#         "text": "Пошёл нах!",
#         "sender": "alladin",
#         "date": "31-01-22 20:01",
#     }
# ]

db_file = "./data/db.json"
json_db = open(db_file, "rb")  # Открываем файэл
data = json.load(json_db)  # Загружаем данные из файла
messages_list = data["messages_list"]  # Берем собщения из структуры и кладем в переменную


def save_messages():
    data = {
        "messages_list": messages_list,
    }
    json_db = open(db_file, "w")
    json.dump(data, json_db)  # Записать данные в файл


def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['date']}")
    print("-" * 20)


def add_message(name, txt):
    if len(txt) < 1: return "ERROR"
    if len(txt) > 3000: return "ERROR"
    if len(name) < 3: return "ERROR"
    if len(name) > 100: return "ERROR"
    message = {
        "text": txt,
        "sender": name,
        "date": datetime.now().strftime("%H:%M"),

    }
    messages_list.append(message)



#def long(txt):



# add_message("Gelmgoltz", "Эй, парернь, ковер купи")
# add_message("Sarkastic", "Летающий?")

for m in messages_list:
    print_message(m)


@app.route("/")
def index_page():
    return "Добро пожаловать в оазис!"


@app.route("/get_messages")
def get_messages():
    return {"messages": messages_list}


@app.route("/send_message")
def send_message():
    name = request.args["name"]
    text = request.args["text"]
    add_message(name, text)
    save_messages()
    return "OK"


@app.route("/form")
def form():
    return render_template("form.html")


app.run()
