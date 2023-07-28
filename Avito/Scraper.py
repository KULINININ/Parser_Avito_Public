import requests
import json
import logging


import item_filters
from ScraperErrors import Avito_4xx_Error


class Scraper:
    def __init__(self, avito_api, ignore_list):

        self.session = requests.session()

        self.headers = {
            'headers': 'headers'
        }
        
        self.avito_api = avito_api
        self.ignore_list = ignore_list

    
    def get_avito_response(self, request_data):

        try:
            avito_response = self.session.get(self.avito_api + request_data['api_parametrs'], headers = self.headers)
        except Exception as e:
            logging.error(f'Request error')
            logging.error(e)
            return []

        if avito_response.status_code != 200:
            if avito_response.status_code in [403, 429]:
                logging.error(f'403/429 error')
                raise Avito_4xx_Error(
                    status_code = avito_response.status_code, \
                    chat_id = request_data['chat_id'], \
                    bot_token = request_data['bot_token'], \
                    error = avito_response.text)
            elif avito_response.status_code/100 == 5:
                logging.error(avito_response)
            else:
                logging.error(f'Unknown error')
                logging.error(avito_response)

            return []
        
        json_response = avito_response.json()

        items = json_response['result']['items']

        logging.info(f'Recived {len(items)} items')

        return items


    def search_new_items(self, request_data):

        items = (self.get_avito_response(request_data))

        new_items = []

        items = item_filters.filter_item_type(items)
        logging.info(f'{len(items)} items after filtering by item type')

        items = item_filters.filter_viewed_items(items, request_data['viewed_ids'])
        logging.info(f'{len(items)} items after viewed items filter')

        items = item_filters.filter_old_time_items(items)
        logging.info(f'{len(items)} items after old time filter')

        items = item_filters.filter_ignore_list(items, self.ignore_list)
        logging.info(f'{len(items)} items after ignore list filter')

        items = item_filters.filter_by_region(items, request_data['region'])
        logging.info(f'{len(items)} items after region filter')

        for item in items:
            item_id = item['value']['id']
            title = item['value']['title']
            url = 'https://www.avito.ru' + item['value']['uri_mweb']
            price = item['value']['price']
            sellerInfo = item['value']['sellerInfo']

            new_items.append({
                'item_id' : item_id,
                'title' : title,
                'url' : url,
                'price' : price,
                'sellerInfo' : sellerInfo
                })
            
        if len(new_items) > 5:
            logging.info(f'Too many new items: {len(new_items)}')

        logging.info(f'{len(new_items)} new items')

        return new_items
