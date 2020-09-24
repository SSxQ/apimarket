import requests
import api_market
import threading
import time


api_key = 'ZbPE1lr1V7eHop2cUuhU11jaahnZPAI'

class PingPongThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'PingPongThread'

    def run(self):
        """Запуск потока"""

def main():
    api = api_market.ApiMarket(api_key, 'https://gifts.tm/api/')
    print(api.get_inv())

if __name__ == '__main__':
    main()
