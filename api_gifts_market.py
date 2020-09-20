import requests
import json

api_key = 'ZbPE1lr1V7eHop2cUuhU11jaahnZPAI'

class ApiMarketGifts():
    BASE_URL = 'https://gifts.tm/api/'
    SECRET_KEY_URL_PART = f'/?key={api_key}'

    def __init__(self, api_key):
        self.api_key = api_key 
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        self.headers = {
            'User-Agent':self.ua,
        }

    def get_inv(self):
        r = requests.get(f'{self.BASE_URL}GetInv{self.SECRET_KEY_URL_PART}', headers=self.headers)
        response = json.loads(r.text)

        print(response)