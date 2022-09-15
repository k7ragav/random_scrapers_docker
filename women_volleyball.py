from typing import Any

import requests


import telegram
from dotenv import load_dotenv
import os


def send_message(message:str):
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id="-648193235", text=message)


def get_json_response() -> Any:
        json_response = requests.get("https://tickets.wkvolleybal.nl/getFilteredProductsJSON.th?nohistory=true&eventCategoryFather=6&eventVenueList=1051").json()
        return json_response

def extract_table_data(soup) -> Any:
        data = []
        div_content = soup.find('div', {'class': 'availabilityContainer'})
        return div_content.text

soup = get_json_response()
status = soup['products'][0]['cdSellingStatus']
if status != 'SOLD_OUT':
        messaage = 'Still sold out... :('
        send_message(messaage)