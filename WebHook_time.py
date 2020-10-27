# The main code
from flask import Flask, request, make_response, jsonify, render_template
import time as t
from random import randrange as rnd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import os
import requests

app = Flask(__name__)

def search_clinic(adress):
    # Открытие браузера и
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'accept': '*/*'}

    input_str = ('поликлинника ' + adress).replace(' ', '%20')
    html_code = requests.get('https://yandex.ru/maps/213/moscow/search/' + input_str, headers=HEADERS, params=None).text
    '''
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options = options)
    browser.get('https://yandex.ru/maps/213/moscow/')

    # Ввод адреса
    adress_info = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/form/div[2]/div/span/span/input')
    adress_info.send_keys('Поликлиника ' + adress)
    adress_info.send_keys(Keys.RETURN)
    sleep(5)
    '''
    # Получение информации о клинике
    clinics = []
    soup = bs(html_code, 'lxml')
    all_info = soup.find('ul', class_ = 'search-list-view__list')
    for clinic in all_info.findAll('li', class_ ='search-snippet-view'):
        clinic_ = clinic.find('div', class_ ='search-business-snippet-view__header')
        name = clinic_.find('a', class_ ='link-wrapper').text
        clinic_info = clinic.find('div', class_='search-business-snippet-view__description').text
        work_time = clinic.find('div', class_ ='search-business-snippet-view__footer').text
        rating = clinic.find('div', class_ ='search-business-snippet-view__rating').text.split()[0]
        clinics.append({
            'name':name,
            'clinic_info': clinic_info,
            'rating':rating,
            'work_time':work_time
        })
    return clinics

@app.route('/')
def index():
    return 'Яндекс круче!' # Just a joke

def shutting_down():
    post = request.get_json()
    time = post['queryResult']['parameters']['time']
    timer = time.split('T')
    hours = timer[1].split(':')
    minutes = int(hours[1])
    hour = int(hours[0])
    text = 'Вам надо уснуть в любое из этих времен: '

    for i in range(6):
        if minutes == str(minutes):
            minutes = '' + minutes[-1]
            minutes = int(minutes)
        hour -= 1.5

        if hour % 1 != 0:
            hour -= 0.5
            minutes += 30
            if minutes >= 60:
                minutes -= 60
                hour += 1
        if hour < 0:
            hour += 24

        if minutes <= 9:
            minutes = '0' + str(minutes)

        sleep = str(int(hour)) + ':' + str(minutes)
        if i < 5:
            text = text + sleep + '; '
        else:
            text = text + sleep
    return {'fulfillmentText': text}

def wake_up():
    post = request.get_json()
    time = post['queryResult']['parameters']['time']
    timer = time.split('T')
    hours = timer[1].split(':')
    minutes = int(hours[1])
    hour = int(hours[0])
    text = 'Проснитесь в любое из этих времен: '

    for i in range(6):
        if minutes == str(minutes):
            minutes = '' + minutes[-1]
            minutes = int(minutes)
        hour += 1.5

        if hour % 1 != 0:
            hour -= 0.5
            minutes += 30
            if minutes >= 60:
                minutes -= 60
                hour += 1
        if hour >= 24:
            hour = hour - 24

        if minutes <= 9:
            minutes = '0' + str(minutes)

        sleep = str(int(hour)) + ':' + str(minutes)
        if i < 5:
            text = text + sleep + '; '
        else:
            text = text + sleep
    return {'fulfillmentText': text}

def hi_man(): # Idk for what we create this function
    time_str = str(t.localtime())
    time_hour = int(time_str.split(',')[3].split('=')[1])
    curHr = time_hour

    Hello_list = ['Приветик', 'Здорово', 'Приветствую Вас', 'Здравствуй, хозяин', 'Здравствуй!', 'Привет!']
    random = rnd(0, 7)

    if (curHr < 12):
        Hello_list.append('Доброе утро!')
        hello = Hello_list[random]
        Hello_list.pop(6)
        return({'fulfillmentText': hello})
    elif (curHr < 17):
        Hello_list.append('Добрый день!')
        hello = Hello_list[random]
        Hello_list.pop(6)
        return({'fulfillmentText': hello})

    elif (curHr < 24):
        Hello_list.append('Добрый вечер!')
        hello = Hello_list[random]
        Hello_list.pop(6)
        return({'fulfillmentText': hello})
    else:
        Hello_list.append('Доброй ночи!')
        hello = Hello_list[random]
        Hello_list.pop(6)
        return({'fulfillmentText': hello})


def getting_clinics():
    post = request.get_json()
    adress = post['queryResult']['parameters']['location']['street-address']
    clinics = search_clinic(adress)
    text = ''
    for clinic in clinics:
        text += '\n\n' + clinic['name'] + ', ' + clinic['clinic_info'] + ',\nчасы работы: ' + clinic['work_time'] + ',\nрейтинг: ' + clinic['rating']
    return ({'fulfillmentText': text})



@app.route('/webhook', methods = ['POST'])
def webhook():
    post = request.get_json()
    json_name = post['queryResult']['intent']['displayName']
    if json_name == 'time up':
        return make_response(jsonify(shutting_down()))
    elif json_name == 'hi_man':
        return  make_response(jsonify(hi_man()))
    elif json_name == 'Поликлиники':
        return make_response(jsonify(getting_clinics()))
    elif json_name == 'time down':
        return make_response(jsonify(wake_up()))



if __name__ == '__main__':
    app.run()
