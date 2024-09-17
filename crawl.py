import requests

import time 
import schedule

from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

from telebot.credentials import bot_token, bot_user_name, URL, chat_id

def job():
    TOKEN = bot_token

    options = webdriver.ChromeOptions() 
    options.add_argument('--headless=new')

    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 

    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)

    file = open('stocks.txt', 'r')
    stocks = file.read().split("\n")

    for stock in stocks:
        stock = stock.strip()

        url = "https://dstock.vndirect.com.vn/tong-quan/" + stock
        
        driver.get(url) 
        time.sleep(5)

        current_price = driver.find_element(By.CSS_SELECTOR ,"[class*=stock-price__current]")
        current_percent = driver.find_element(By.CSS_SELECTOR, "[class*=stock-price__percent]")
        
        print(current_price.text)
        print(current_percent.text)

        # create text and send to channel telegram
        text = "(@{}) {} current price: {} ({})".format(bot_user_name, stock, current_price.text, current_percent.text)
        requests.post("https://api.telegram.org/bot{}/sendMessage".format(TOKEN), json={'chat_id': chat_id, 'text': text})

schedule.every(5).minutes.until("16:30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)