import requests
import api_gifts_market

api_key = 'ZbPE1lr1V7eHop2cUuhU11jaahnZPAI'

def main():
    api = api_gifts_market.ApiMarketGifts(api_key)
    print(api.get_inv())

if __name__ == '__main__':
    main()
