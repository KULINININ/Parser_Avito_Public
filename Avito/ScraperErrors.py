class Avito_4xx_Error(Exception):
    def __init__(self, status_code, chat_id, bot_token, error):
        self.status_code = status_code
        self.chat_id = chat_id
        self.bot_token = bot_token
        self.error = error

    def __str__(self):
        return f'{self.status_code} error: {self.error}'