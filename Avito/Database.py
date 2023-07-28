import psycopg2
import logging

class Database:
    def __init__(self, host, port, dbname, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )

        logging.info(f'Successful database connection')

        self.cursor = self.connection.cursor()

        self.cursor.execute('SELECT item_id FROM items')

        self.items_id_list = set(item[0] for item in self.cursor.fetchall())

        self.cursor.execute('SELECT seller_id FROM sellers')

        self.seller_id_list = set(item[0] for item in self.cursor.fetchall())


    def add_seller(self, seller):
        seller_id = seller['userKey']
        seller_name = seller['name']
        is_shop = seller['isShop']
        url = f'https://www.avito.ru/user/{seller_id}/profile'

        self.cursor.execute(
            """
            INSERT INTO sellers (seller_id, seller_name, is_shop, url)
            VALUES (%s, %s, %s, %s)
            """, (seller_id, seller_name, is_shop, url))
        
        self.connection.commit()

        self.seller_id_list.add(seller_id)

        logging.info(f'Seller {seller_id} added to database')


    def add_items(self, items):

        for item in items:
            if item['sellerInfo']['userKey'] not in self.seller_id_list:
                self.add_seller(item['sellerInfo'])

            if str(item['item_id']) not in self.items_id_list:

                item_price = item['price'][:-2].replace(' ', '')
                item_price = item_price if item_price.isnumeric() else None
            
                self.cursor.execute(
                """
                INSERT INTO items (item_id, title, price, url, seller_id)
                VALUES (%s, %s, %s, %s, %s)
                """, (
                    item['item_id'],
                    item['title'],
                    item_price,
                    item['url'],
                    item['sellerInfo']['userKey'])
                )
                
                self.connection.commit()

                self.items_id_list.add(str(item['item_id']))

                logging.info(f'Item {item["item_id"]} added to database')
                

    def get_ignore_list(self):
        self.cursor.execute('SELECT seller_id FROM sellers WHERE in_black_list')

        return [item[0] for item in self.cursor.fetchall()]