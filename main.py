import os
import telebot
import yfinance as yf
from youtubesearchpython import VideosSearch

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey! Hows it going?")


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['stock'])
def get_stocks(message):
    response = ""
    stocks = ['ftnt', 'tsla', 'nvda']
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='5d', interval='1d')
        data = data.reset_index()
        response += f"-----{stock}-----\n"
        stock_data.append([stock])
        columns = ['stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)
            format_date = row['Date'].strftime('%m/%d')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()

    response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
    response += "\nStock Data"
    print(response)
    bot.send_message(message.chat.id, response)


def stock_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "price":
        return False
    else:
        return True


@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5m', interval='1m')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id, data['Close'].to_string(header=False))
    else:
        bot.send_message(message.chat.id, "No data!?")


def check_blank(s):
    if s.isspace() or not s:
        return True
    else:
        return False


def youtube_search(message):
    prefixKeyWord = message.text.split()[0]
    input = message.text.split()
    query = ' '.join(input[1:])
    if check_blank(query):
        return

    # if prefixKeyWord is youtube
    if prefixKeyWord.lower() == 'youtube':
        videosSearch = VideosSearch(query, limit=3)
    else:
        return
    for i in range(5):
        print(videosSearch.result()['result'][i]['link'])
        bot.send_message(message.chat.id, videosSearch.result()['result'][i]['link'])


@bot.message_handler(func=youtube_search)
def send_video_links(message):
    youtube_search(message)


bot.polling()
