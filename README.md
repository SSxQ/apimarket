# apimarket

API для сайтов https://market.csgo.com/, https://gifts.tm/, https://market.dota2.net/ и производным этой платформы. 
Комментарии в коде скопированы из официальной документации, методы API у них универсальные, от одного сайта подходят 
и под другой, но могут быть некоторые отличия. 

Тестировал на gifts.tm, имейте ввиду  

Пример использования:

import api_market

api_key = 'APIKEY'

#В качестве второго аргумента указываем ссылку на апи сайта, с которым работаем
api = api_market.ApiMarket(api_key, 'https://gifts.tm/api/')

print(api.get_inv())
