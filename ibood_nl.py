from typing import Any
import requests
import os

from bs4 import BeautifulSoup
import mysql.connector
import telegram
from dotenv import load_dotenv


def sql_connection():
    load_dotenv()
    mydb = mysql.connector.connect(host="87.106.113.205",
                                   user = os.getenv('DB_USER'),
                                   password = os.getenv('DB_PASSWORD'),
                                   database = 'random_scrapers_db'
                                   )

    mycursor = mydb.cursor(prepared=True)
    return mydb, mycursor

def check_urls():
    mydb, mycursor = sql_connection()
    sql_query= "SELECT url from ibood_nl"
    mycursor.execute(sql_query)
    result = [item[0] for item in mycursor.fetchall()]
    if result:
        return result
    else:
        return []

def insert_result_in_table(result):
    mydb, mycursor = sql_connection()
    sql_query = "INSERT INTO ibood_nl (`url`) " \
                "VALUES (%s)"
    mycursor.execute(sql_query, result)
    mydb.commit()

def send_message(message:str):
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id="-846684255", text=message)


def get_json_response(keyword: str) -> Any:
        HEADERS = {
            'Authority': 'api.ibood.io',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4544.0 Safari/537.36 Edg/93.0.933.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.ibood.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.ibood.com',
            'Accept-Language': 'en-US,en;q=0.9',
            'ibex-language': 'en',
            'ibex-shop-id': 'b22a484d-fd20-570a-adf6-22edf2fdaf79',
            'ibex-tenant-id':'eafb3ef2-e1ba-4f01-b67a-b0447bea74eb',
            'dnt': '1',
            'sec-gpc': '1',
        }
        json_response = requests.post(f"https://api.ibood.io/search/offers/live?q={keyword}&skip=0&take=50", headers=HEADERS).json()
        return json_response


def extract_table_data(soup) -> Any:
        div_content = soup.find('div', {'class': 'ant-spin-container'})
        return div_content.text


def get_soup_content(main_url: str) -> Any:

        main_url = f"{main_url}"
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

        html_content = requests.get(main_url, headers=HEADERS)

        soup = BeautifulSoup(html_content.content.decode('utf-8'), 'lxml')
        return soup


# soup = get_soup_content(main_url='https://www.ibood.com/offers/nl/find-offer?q=baby')
# text = extract_table_data(soup)
def main():
    print(1)
    keywords = ['baby', 'pampers', 'luier']
    url_list = check_urls()
    items_message = ""
    for keyword in keywords:
        items = get_json_response(keyword)['data']['items']
        if items:
            for item in items:
                offerId = item['offerItemClassicId']
                url = f"https://www.ibood.com/nl/nl/product-specs/00000/{offerId}/"
                name_of_product = item['image'].split("/")[-1].replace(".jpg", "")
                url_to_insert = (str(url),)
                if url not in url_list:
                    insert_result_in_table(url_to_insert)
                    items_message += f"{name_of_product} here is the link: {url} \n"

    if items_message != "":
        final_message = f"There might be some new stuff for Coco: \n" \
                        f"{items_message}"
        send_message(final_message)

if __name__ == "__main__":
    main()