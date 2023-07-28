import requests

class TelegramBot:

    def new_items(self, items, chat_id, bot_token):
        for item in items:
            message = f"""
<u><b>{item['title']}</b></u>
------------------------------------------------------
<b><u>Цена:</u> {item['price']}</b>
------------------------------------------------------
{item['url']}
        """
                
            requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=HTML')


    def avito_ban(self, exception):
        message = f'Бан по IP: {exception.error}'
        requests.get(f'https://api.telegram.org/bot{exception.bot_token}/sendMessage?chat_id={exception.chat_id}&text={message}&parse_mode=HTML')