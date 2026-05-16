import telebot
import requests

API_token = "8782304060:AAE9rzLC7UKF3GE4YhWwJQusPr4b4p8BvdY"

bot = telebot.TeleBot(API_token)

def get_coins(symbol):
    coins = {
                "BTC": "bitcoin",
                "ETH": "ethereum",
                "DOGE": "dogecoin",
            }
    if symbol not in coins:
        return f"""Coin not supported!
                please enter one of: {', '.join(coins.keys())}"""
    
    coin_id = coins[symbol]
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200 :  
            data = response.json()
            price = data[coin_id]["usd"]
            change_percent = data[coin_id]["usd_24h_change"]
            change_value = price * (change_percent / 100)
                
            result = f"""\nCoin: {symbol}
                    Current Price: ${price:,.2f}
                    24h Change Value: {change_value:.2f}$
                    24h Change Percent: {change_percent:.2f}%
                    """
            return result
        else:
            return "API hasn't result"
    except Exception as e:
        return "Error:", str(e)

# handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """
                 Hi there, I am shima.
                 This bot gives you information such as the current 
                 price and status of the CoinGecko cryptocurrency.
                 You can get the latest status with coin symbol
                 (e.g. /BTC, /ETH).
                 """)  

# Handle '/BTC' and '/ETH'
@bot.message_handler(func= lambda message:True)
def check_CoinGecko(message):
    try:
        symbol = message.text.replace("/", "")
        res = get_coins(symbol)
        bot.reply_to(message, res)
    except:
        bot.reply_to(message, "Problem with geting about the coingecko change.")       
    
bot.infinity_polling()