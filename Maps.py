from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import os


def search_clinic(adress):
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options = options)
    browser.get('https://yandex.ru/maps/213/moscow/')

    # Ввод адреса
    adress_info = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/form/div[2]/div/span/span/input')
    adress_info.send_keys('Поликлиника ' + adress)
    adress_info.send_keys(Keys.RETURN)
    sleep(5)

    # Получение информации о клинике
    clinics = []
    soup = bs(browser.page_source, 'lxml')
    all_info = soup.find('ul', class_ = 'search-list-view__list')
    for clinic in all_info.findAll('li', class_ ='search-snippet-view'):
        clinic_ = clinic.find('div', class_ ='search-business-snippet-view')
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