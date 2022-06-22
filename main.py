import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.Java
import time
from random import randrange
from fake_useragent import UserAgent

# from random import randrange
ua = UserAgent()
ua_ = ua.random

import sys
import time
from random import randrange

import asyncio
import aiohttp

import requests
from bs4 import BeautifulSoup
import lxml
import json
import time

import re

import pandas as pd


# url = 'https://www.flipkart.com/'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": f'{ua}'  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
    # like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

print('start...')

# # #         = 1 =
# # #
# # # # START of "Init..."
# # # #
chrome_path = "./chromedriver.exe"

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--incognito")
options.add_argument("start-maximized")
#
# options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
#
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=options, executable_path=chrome_path)

browser.implicitly_wait(1)
# # #
# # # END of "Init..."
# #
#
#
#
# start_ = True
#
# url_ = []
#
# for pg in range(1, 50):
#
#     if start_:
#         start_ = False
#         url = f'https://www.viator.com/Iceland/d55-ttd'
#     else:
#         url = f'https://www.viator.com/Iceland/d55-ttd/{pg}'
#
#     browser.get(url)
#
#     first_pg_xp = '//*[@id="pagination"]/li[2]/a'
#     start_time = time.time()
#     try:
#         WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, first_pg_xp)))
#     except:
#         pass
#     finish_time = time.time() - start_time
#     print(f'Page = {pg}     FP: {finish_time}')
#
#     source_html = browser.page_source
#     # # запись СПАРСЕНОЙ инфы в ХТМЛ-файл
#     # with open('index.html', 'w', encoding='utf-8') as file:
#     #     file.write(source_html)
#
#     soup = BeautifulSoup(source_html, 'lxml')
#
#     el_links_ = soup.find_all("h2", class_='product-card-row-title mb-0 pt-md-4')
#     for i in el_links_:
#         el_link_ = i.find('a').get('href')
#         el_link = f'https://www.viator.com{el_link_}'
#         url_.append(el_link)
#
# # запись ссылок из СПИСКА в файл
# with open('urls.txt', 'a', encoding='utf-8') as file:
#     for url in url_:
#         file.write(f'{url}\n')
# #
# # #         = End of 1 =
#
#
# breakpoint()

start_time = time.time()

ele_list = []
ele_info = []

tmp_ = 0


async def get_page_data(session, word_, str_num):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": f'{ua_}'
    }

    print(f"start...")

    global ele_list
    global ele_info
    global tmp_

    link_ = f'https://dict.leo.org/russisch-deutsch/{word_}?side=right'


    async with session.get(url=link_, headers=headers) as response:

        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')

        # # # ЗАЩИТА от БАНА!!!
        # time.sleep(randrange(1, 2))

        # print(f'str_num: {str_num}')

        url_ = link_
        print(f'{str_num} --> : {url_}')

        """
        data-dz-name

        subst --> Substantive --> существительные
        adjadv --> Adjektive / Adverbien --> прилагательные / наречия   
        verb --> Verben --> глаголы     
        praep --> Präpositionen / Pronomen / --> Предлоги / Местоимения /     
        phrase --> Phrasen --> фразы
        example --> Beispiele --> Примеры

        """
        pere = {'Substantive': 'subst',
                'Adjektive / Adverbien': 'adjadv',
                'Verben': 'verb',
                'Präpositionen / Pronomen': 'praep',
                'Phrasen': 'phrase',
                'Beispiele': 'example'
                }

        word__ = word_.replace('%20', ' ')

        ele_info.append(
            {
                "url": url_,
                "word": word__
            }
        )


        for k, v in pere.items():
            try:
                trs_ = soup.find('div', {'data-dz-name': f'{v}'}).find('tbody').find_all('tr', {'data-dz-ui': 'dictentry'})
                aaa = []
                for eles_ in trs_:
                    aaa.append(
                        {
                            f"ru": eles_.find('td', {'lang': 'ru'}).text.strip(),
                            f"de": eles_.find('td', {'lang': 'de'}).text.strip()
                        }
                    )

                ele_info.append(
                    {
                        f"{k}": aaa
                    }
                )
            except:
                ele_info.append(
                    {
                        f"{k}": "NONE"
                    }
                )


async def gather_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": f'{ua_}'
    }

    # # читаю ССЫЛКИ из ранее созданного файла
    # # !!! ОБРЕЗАЮ СИМВОЛ ПЕРЕНОСА СТРОКИ !!!
    # with open('urls.txt') as file:
    #     url_list = [line.strip() for line in file.readlines()]

    # page_count = len(url_list)
    # print(f'PAG.: {page_count}')

    async with aiohttp.ClientSession() as session:
        # try:
        #     ele_link_ = soup.find('a', {'name': 'business-unit-card'}).get('href')
        # except Exception as e:
        #     print(e)

        tasks = []


        with open('words.txt', encoding='utf-8') as file:
            words_list = [line.strip() for line in file.readlines()]

        str_num = 0


        for word__ in words_list:
            print(word__)

            word_ = word__.replace(' ', '%20')

            task = asyncio.create_task(get_page_data(session, word_, str_num))
            tasks.append(task)
            str_num += 1
            # break


        await asyncio.gather(*tasks)


        # # ЗАЩИТА от БАНА!!!
        # time.sleep(randrange(0, 2))
        # # print(f'Обработал {i} / {page_count}')















def json_to_csv():
    df = pd.read_json(r'_my_json555.json')
    df.to_csv(r'_my_json2022.csv', index=None)


def file_txt():
    # читаю ССЫЛКИ из ранее созданного файла
    # !!! ОБРЕЗАЮ СИМВОЛ ПЕРЕНОСА СТРОКИ !!!
    with open('words.txt') as file:
        words_list = [line.split('.')[1:] for line in file.readlines()]

    w_new = []
    for w in words_list:
        ww = str(w).split('-')[0].replace('[\' ', '').strip()
        w_new.append(ww)

    print(w_new)


def main():
    #file_txt()

    # json_to_csv()
    asyncio.run(gather_data())

    finish_time = time.time() - start_time

    # with open('test.txt', 'w+', encoding='utf-8') as file:
    #     file.write(ele_info)

    with open('_my_json2022.json.', 'w', encoding='utf-8') as file:
        json.dump(ele_info, file, indent=4, ensure_ascii=False)

    # with open('out.json', 'w+', encoding='utf-8') as file:
    #     json.dump(ele_list, file, indent=4, ensure_ascii=False)

    print(f"TIME: {finish_time}")
    # cur_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    # print(f"TIME_now: {cur_time}")

    browser.close()
    browser.quit()









if __name__ == "__main__":
    # print(sys.version_info[0])
    # ЗАПЛАТКА!!! Блок выпадания ОШИБКИ под виндой...
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # asyncio.run(main())
    main()


# # 1
# #
# # запись СПАРСЕНОЙ инфы в ХТМЛ-файл
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(source_html)
#pagination_count = soup.find('div', {"id": "ajaxPaging-product"}).find('ul', class_='product-pagination js-pagination').find_all('li', class_='pagination-item')[-1].text.strip()

# with open("index.html", "r", encoding='utf-8') as f:
#     source_html = f.read()
