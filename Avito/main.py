import time
import logging
from multiprocessing import Process

import requests_info_loader
from TelegramBot import TelegramBot
from Scraper import Scraper
from ScraperErrors import Avito_4xx_Error
from Database import Database
from config import *

logging.basicConfig(
    level = logging.DEBUG, \
    format="%(asctime)s [%(levelname)s] %(message)s", \
    handlers = [
        logging.FileHandler('Avito//logs//logs.log'),
        logging.StreamHandler()
    ])


def main():

    database = Database(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_DBNAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )

    scraper = Scraper(AVITO_API, ignore_list=database.get_ignore_list())
    telegram_bot = TelegramBot()

    requests_list = requests_info_loader.get_requests_list()

    while True:

        for request_data in requests_list:
        
            try:
                new_items = scraper.search_new_items(request_data)

                telegram_bot_process = Process(
                    target=telegram_bot.new_items,
                    args=(
                        new_items,
                        request_data['chat_id'],
                        request_data['bot_token'],
                    )
                )
                
                telegram_bot_process.start()
                    
                database.add_items(new_items)
                
                logging.info(f'Sleeping for 10 seconds')
                time.sleep(10)

            except Avito_4xx_Error as exception:
                logging.error(exception) 
                telegram_bot.avito_ban(exception)
                time.sleep(3600)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as exception:
            logging.error(repr(exception))
            logging.info(f'Sleeping for 120 seconds')
            time.sleep(120)