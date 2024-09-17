import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print(update)
    
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    command = update.message.text.encode('utf-8').decode()

    print_command(command)

    if command == "/start":
       bot_welcome = "Welcome to stock notification bot!"
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
    
    else:
        with open('stocks.txt', "w") as stock_files:
            data = stock_files.read()
            stocks = data.split("\n")

            if command == "/list-stock":
                str = "".join([stock + "\n" for stock in stocks])
                bot.sendMessage(chat_id=chat_id, text=str, reply_to_message_id=msg_id)
            elif command.startswith("/add-stock"):
                stock = command.replace("/add-stock", "").strip()
                stocks.append(stock)
                write_stocks_to_file(stocks)

                str = "Add successfully! New list stocks: \n\n"
                str = "".join([stock + "\n" for stock in stocks])
                bot.sendMessage(chat_id=chat_id, text=str, reply_to_message_id=msg_id)
            else: 
                bot.sendMessage(chat_id=chat_id, text="Command not true!", reply_to_message_id=msg_id)

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    result = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if result:
        return "webhook setup ok!"
    else:
        return "webhook setup failed!"

@app.route('/')
def index():
    return 'Hello!'

def print_command(str): 
    print("Command: " + str + "\n")

def write_stocks_to_file(file, stocks):
    cnt = 0
    lens = len(stocks)
    for stock in stocks:
        cnt += 1
        if cnt == lens:
            break

        file.write(stock + "\n")

    file.write(stocks[lens - 1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)