import requests
import json

class ApiMarketGifts():

    def __init__(self, api_key):
        self.api_key = api_key 
        self.BASE_URL = 'https://gifts.tm/api/'
        self.SECRET_KEY_URL_PART = f'/?key={self.api_key}'
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        self.headers = {
            'User-Agent':self.ua,
        }

#region Вспомогательные методы
    def get_json_resp(self, mid_params, ending_params=''):
        '''
        Принимает имя метода, за исключением нижнего подчеркивания, в котором вызывается, для отправки GET запроса по этому URL. 
        Необязательный аргумент - ending_params, параметры, которые идут в URL после Secret Key.
        '''

        r = requests.get(f'{self.BASE_URL}{mid_params}{self.SECRET_KEY_URL_PART}{ending_params}', headers=self.headers)
        response = json.loads(r.text)

        return response
    
    def get_json_resp_post(self, mid_params, data):
        '''
        Принимает имя метода, за исключением нижнего подчеркивания, в котором вызывается, 
        а так же параметры POST запроса. 
        '''
        r = requests.post(f'{self.BASE_URL}{mid_params}{self.SECRET_KEY_URL_PART}', headers=self.headers, data=data)
        response = json.loads(r.text)

        return response
#endregion
#region Продажа предметов
    def set_price(self, classid, instanceid, price, item_id=''):
        '''
        Выставить новый предмет на продажу. Что-бы получить список предметов для выставления, воспользуйтесь методом GetInv.

        Параметры запроса:
            [classid] — ClassID предмета в Steam, можно найти в описании вещей своего инвентаря в стиме.
            [instanceid] — InstanceID предмета в Steam, можно найти в описании вещей своего инвентаря в стиме.
            [price] — сумма в копейках (целое число)
            [item_id] — Этот ID можно найти в методе Trades или при первом выставлении на продажу. 
            Необязательный, используется для редактирования цены на уже выставленный предмет.
        '''

        if item_id:
            #редактирование цены на предмет
            return self.get_json_resp(f'SetPrice/{item_id}/{price}')
        else:
            #выставление нового предмета
            return self.get_json_resp(f'SetPrice/new_{classid}_{instanceid}/{price}')

    def remove_all(self):
        '''
        Снятие сразу всех предметов с продажи. 
        ВАЖНО! Предметы необходимо будет выставлять заново. Если Вы хотите остановить торговлю на время - используйте метод GOOFFLINE.
        '''

        return self.get_json_resp('RemoveAll')
    
    def item_request(self, botid=''):
        '''
        С помощью этого метода, Вы можете запросить передачу предмета который был куплен у Вас или куплен Вами. Вам будет отправлен 
        оффлайн трейдоффер в Steam, который необходимо принять в течении 2 минут. В одну операцию может попасть максимум 20 предметов.
        
        Параметры запроса:
            [botid] — Идентификатор бота, который можно узнать c помощью метода Trades - это поле ui_bid у предметов со статусом (ui_status) = 4
        
        ВАЖНО! Если параметр botid не указан, значит делается запрос на передачу проданных предметов, а не запрос на получение купленного предмета.

        В нашей системе можно создать только один запрос за определенное время. За один запрос можно получить вещи только с одного бота, 
        на котором они в данный момент находятся.

        Передача проданных Вами предметов не требует от Вас никаких дополнительных параметров, бот сам заберет у Вас 20 предметов. 
        Максимум через 1 минуту после принятия трейд оффера Вы получите деньги за эти предметы.
        '''

        return self.get_json_resp(f'ItemRequest/out/{botid}') if botid else self.get_json_resp('ItemRequest/in/1')

    def report_created_trade(self, requestid, tradeofferid):
        '''
        Оповещение системы об успещном создании трейда.

        Пояснение к запросу:
            requestId — ID оффера, полученное в ItemRequest.
            tradeOfferId - ID трейд оффера, созданного в Steam
        '''

        return self.get_json_resp(f'ReportCreatedTrade/{requestid}/{tradeofferid}')

    def report_failed_trade(self, requestid):
        '''
        Вызов этого метода необходим, если создание трейда невозможно из-за отсутствия необходимых предметов. В этом случае система 
        пересоздаст список предметов при следующем вызове ItemRequest.

        ВАЖНО! Не вызывайте этот метод, если не уверены, что оффер не создан
        '''

        return self.get_json_resp(f'ReportFailedTrade/{requestid}')

    def market_trade(self):
        'Получить список трейд офферов, которые в данный момент были высланы Маркетом на Ваш аккаунт и ожидают подтверждения в Steam.'

        return self.get_json_resp('MarketTrades')

    def mass_set_price(self, name, price):
        '''
        Изменить цену сразу на множество товаров, находящихся на продаже по названию предмета.

        Параметры запроса:
            [name] — ИЛИ Название предмета (Это может быть market_hash_name, market_name на английском или русском языке)
            [name] — ИЛИ classid_instanceid предмета.
            [price] — Цена в копейках (минимум 50).
        '''

        return self.get_json_resp(f'MassSetPrice/{name}/{price}')

    def mass_set_price_by_id(self, ui_id):
        '''
        Изменить цену сразу на множество товаров, находящихся на продаже - по [ui_id] предметов.

        Параметры запроса (POST):
            list[ui_id] = price (цена предмета в копейках, не меньше 50).
            Использовать так: list[156385570]=50&list[156385593]=50&...
        '''

        return self.get_json_resp_post('MassSetPriceById', ui_id)
#endregion
#region Покупка предметов
    def buy(self, classid, instanceid, price, hash_='', partner='', token=''):
        '''
        Покупка предмета. В нашей системе возможно покупка только по одному предмету за запрос.

        Параметры запроса:
            [classid]_[instanceid] — идентификаторы предмета, который можно найти в ссылке на предмет. 
            [price] — цена в копейках (целое число), уже какого-то выставленного лота, или можно указать любую сумму 
            больше цены самого дешевого лота, во втором случае будет куплен предмет по самой низкой цене.
            [hash] - md5 от описания предмета. Вы можете найти его в ответе метода ItemInfo. Необязательный.
            partner=[partner]&token=[token] - параметры трейд ссылки аккаунта, который получит предмет. 
        '''

        if partner and token:
            return self.get_json_resp(f'Buy/{classid}_{instanceid}/{price}/{hash_}', f'(&partner={partner}&token={token})')
        else:
            return self.get_json_resp(f'Buy/{classid}_{instanceid}/{price}/{hash_}')

    
#endregion
#region Ордера на покупку
    def get_orders(self, page=''):
        '''
        Получить список своих ордеров, актуальных на данный момент.

        Параметры запроса:
            [page] — Номер страницы, на странице находится 500 предметов. Опциональный параметр, 
            если он не будет указан в ответ Вы получите только 2000 ваших заявок.
        '''

        return self.get_json_resp(f'GetOrders/{page}')

    def insert_order(self, classid, instanceid, price, hash_='', partner='', token=''):
        '''
        Создать новый запрос на автоматическую покупку предмета.

        Параметры запроса:
            [classid] — ClassID предмета в Steam, можно найти в ссылке на предмет
            [instanceid] — InstanceID предмета в Steam, можно найти в ссылке на предмет
            [price] — Цена в копейках, целое число
            [hash_] — Если хотите быть уверены в том, что покупаете (см. метод Buy), не обязательный - можно отправить пустую строку "[price]//?key=..."
            [partner] — Steam ID пользователя, кому будет передан купленный предмет (необязательный)
            [token] — Токен из ссылки для обмена пользователя, которому будет передан предмет (необязательный)
        '''
        if partner and token:
            return self.get_json_resp(f'InsertOrder/{classid}/{instanceid}/{price}/{hash_}', f'(&partner={partner}&token={token})')
        else:
            return self.get_json_resp(f'InsertOrder/{classid}/{instanceid}/{price}/{hash_}')

    def update_order(self, classid, instanceid, price, partner='', token=''):
        '''
        Изменить/удалить запрос на автоматическую покупку предмета.

        Параметры запроса:
            [classid] — ClassID предмета в Steam, можно найти в ссылке на предмет
            [instanceid] — InstanceID предмета в Steam, можно найти в ссылке на предмет
            [price] — Цена в копейках, целое число.
            [partner] — Steam ID пользователя, кому будет передан купленный предмет (необязательный)
            [token] — Токен из ссылки для обмена пользователя, которому будет передан предмет (необязательный)
        ВАЖНО! Для удаления заявки параметр [PRICE] должен равняться нулю (0).
        '''

        if partner and token:
            return self.get_json_resp(f'UpdateOrder/{classid}/{instanceid}/{price}', f'(&partner={partner}&token={token})')
        else:
            return self.get_json_resp(f'UpdateOrder/{classid}/{instanceid}/{price}')

    def process_order(self, classid, instanceid, price, partner='', token=''):
        '''
        С помощью этого метода можно создать, обновить и удалить запрос на автоматическую покупку предмета.

        Если запрос отсутствует - он будет создан, если присутствует - обновлен. При обновлении цены на 0 - ордер будет удален.

        ВНИМАНИЕ! Если будет присутствовать предмет на продаже ценой ниже или равной ордеру - предмет будет сразу куплен 
        (за цену предмета, ниже цены ордера или равна ему). Если ордер был впервые создан, записи о нем при покупке не появится в логе ордеров (GETORDERSLOG).
        
        ВАЖНО! В этом методе не требуется указание хэша, будет куплен предмет без учета проверки хэша.

        Параметры запроса:
            [classid] — ClassID предмета в Steam, можно найти в ссылке на предмет
            [instanceid] — InstanceID предмета в Steam, можно найти в ссылке на предмет
            [price] — Цена в копейках, целое число.
            [partner] — Steam ID пользователя, кому будет передан купленный предмет (необязательный)
            [token] — Токен из ссылки для обмена пользователя, которому будет передан предмет (необязательный)
        ВАЖНО! Для удаления заявки параметр [PRICE] должен равняться нулю (0).
        '''

        if partner and token:
            return self.get_json_resp(f'ProcessOrder/{classid}/{instanceid}/{price}', f'(&partner={partner}&token={token})')
        else:
            return self.get_json_resp(f'ProcessOrder/{classid}/{instanceid}/{price}')

    def delete_orders(self):
        'Удалить сразу все запросы на автоматическую покупку предмета.'

        return self.get_json_resp('DeleteOrders')

    def status_orders(self):
        'Узнать статус работы ордеров.'

        return self.get_json_resp('StatusOrders')

    def get_orders_log(self):
        'Этот метод помогает узнать историю срабатывания ордеров на автоматическую покупку. Отображается 100 последних ордеров.'

        return self.get_json_resp('GetOrdersLog')

    

#endregion
#region Уведомления
    def get_notifications(self):
        'Получить список включенных уведомлений о изменении цены.'

        return self.get_json_resp('GetNotifications')

    def update_notification(self, classid, instanceid, price):
        '''Создание/изменение/удаление уведомления о изменении цены на отcлеживаемый предмет.
        
        Параметры запроса:
            [classid] — ClassID предмета в Steam, можно найти в ссылке на предмет
            [instanceid] — InstanceID предмета в Steam, можно найти в ссылке на предмет
            [price] — Цена в копейках, целое число.
        
        ВАЖНО! Для удаления уведомления, параметр [PRICE] должен равняться нулю (0).
        '''

        return self.get_json_resp(f'UpdateNotification/{classid}/{instanceid}/{price}')
#endregion
#region Действия с аккаунтом

    def get_inv(self):
        '''
        Получение инвентаря Steam, только те предметы, которые Вы еще не выставили на продажу.
        Пояснение к ответу:
            ui_id — ID для выставления на продажу
            ui_status — статус предмета, всегда 1
            i_market_price — рекомендованная цена продажи (в рублях)
        '''
        return self.get_json_resp('GetInv')

    def trades(self):
        '''
        Список предметов на продаже, готовых к получению после покупки, предметов которые необходимо передать после продажи со страницы "Мои вещи".
        Возможные статусы:
            "ui_status" = 1 — Вещь выставлена на продажу.
            "ui_status" = 2 — Вы продали вещь и должны ее передать боту.
            "ui_status" = 3 — Ожидание передачи боту купленной вами вещи от продавца.
            "ui_status" = 4 — Вы можете забрать купленную вещь.
        Пояснение к ответу:
            ui_id — ID предмета в нашей системе.
            ui_status — статус предмета (см. выше).
            ui_price — ваша цена.
            position — позиция в очереди продажи (сортировка по наименьшей цене), в момент покупки выбирается самый дешевый предмет.
            ui_bid — ID бота, на котором находится предмет в статусе 4.
            ui_asset — ID предмета в инвентаре бота.
            placed — Время, когда изменился статус предмета/цена или он был выставлен на продажу.
            left — Времени осталось на передачу предмета, после этого операция будет отменена и деньги вернутся покупателю. Будут начислены штрафные баллы
            i_market_price — Рекомендуемая цена продаже (относительно ТП Steam).
        '''
        return self.get_json_resp('Trades')
    
    def get_money(self):
        'Получить сумму на балансе в копейках.'

        return self.get_json_resp('GetMoney')

    def ping_pong(self):
        'Выход в онлайн, необходимо отправлять раз в 3 минуты.'

        return self.get_json_resp('PingPong')

    def go_offline(self):
        'Моментально приостановить торги, рекомендуем отключиться от вебсокетов.'

        return self.get_json_resp('GoOffline')
    
    def set_steam_api_key(self, api_key):
        'Передать Steam API ключ вашего аккаунта'

        return self.get_json_resp(f'SetSteamAPIKey/{api_key}')

    def set_token(self, token):
        'Изменить трейд-ссылку на маркете для Вашего аккаунта'

        return self.get_json_resp(f'SetToken/{token}')

    def get_token(self):
        'Получить текущий токен из трейд-ссылки.'

        return self.get_json_resp(f'GetToken')

    def get_ws_auth(self):
        'Получить временный ключ-токен для авторизации на веб-сокет сервере'

        return self.get_json_resp(f'GetWSAuth')

    def update_inventory(self):
        'Запросить обновление кэша инвентаря (рекомендуется делать после каждого принятого трейд оффера).'

        return self.get_json_resp('UpdateInventory')

    def inventory_items(self):
        'Метод возвращающий информацию о статусе кэша инвентаря в нашей базе данных с количеством предметов и текущим статусом обновления.'

        return self.get_json_resp('InventoryItems')

    def operaion_history(self, start_time, end_time):
        '''Получить историю операций на всех маркетах за определенный период времени.
        
        Параметры запроса:
            [start_time] — unix time в секундах начала периода
            [end_time] — unix time в секундах конца периода
        '''

        return self.get_json_resp(f'OperationHistory/{start_time}/{end_time}')

    def get_discounts(self):
        '''
        Получить информацию о собственном обороте, скидках и комиссиях. 
        
        ВНИМАНИЕ! Скидки привязаны к маркету и не переносятся, например, с маркета Dota2 
        на маркет CS:GO. В пределах одного маркета возможен перенос скидок на другой аккаунт.
        '''
    
        return self.get_json_resp('GetDiscounts')

    def get_counters(self):
        'Получить счетчики, которые расположены на странице "Мои Вещи".'

        return self.get_json_resp('GetCounters')

    def get_my_profile_hash(self):
        'Получить хэш ссылку на собственный профиль.'

        return self.get_json_resp('GetMyProfileHash')

    def get_profile_items(self, hash_):
        '''Получить предметы на продаже из произвольного профиля.
        ВАЖНО! Предметы отображаются только тогда, когда продавец находится в сети и предметы находятся 
        на первом месте в очереди продаж (имеют самую низкую цену).

        Параметры запроса:
            [hash_] — Хэш ссылка, которую можно взять либо из метода GetMyProfileHash
        '''

        return self.get_json_resp(f'GetProfileItems/{hash_}')

    def get_my_sell_offers(self):
        'Получить только свои предметы, которые находятся на продаже на любом месте в очереди.'

        return self.get_json_resp('GetMySellOffers')

    def get_items_to_give(self):
        'Получить список предметов, которые были проданы и их необходимо передать боту маркета с помощью метода ItemRequest.'

        return self.get_json_resp('GetItemsToGive')

#endregion
#region Поиск предметов
    def mass_search_item_by_name(self, items):
        '''
        Поиск нескольких предметов (максимум 10) за один POST запрос.

        Параметры запроса (POST):
            list[0..9] = Название предмета на английском языке (market_hash_name).
            Использовать так: list[0]=StatTrak™ Glock-18 | Dragon Tattoo (Factory New)&list[1]=StatTrak™ AK-47 | Blue Laminate (Minimal Wear)&...
        '''

        return self.get_json_resp_post('MassSearchItemByName', items)

    def search_item_by_name(self, market_hash_name):
        '''
        Вариант для запроса по одному предмету

        Параметры запроса:
            [market_hash_name] - Название предмета, которое можно взять из инвентаря Steam.
        '''

        return self.get_json_resp(f'SearchItemByName/{market_hash_name}')
#endregion
#region Моментальные покупки (покупка без ожидания передачи предмета)
    def quick_items(self):
        '''
        Получить список предметов, которые можно купить прямо сейчас и забрать через пару секунд после покупки.

        Подробнее про эти предметы можно прочитать тут: https://gifts.tm/quick/
        '''

        return self.get_json_resp('QuickItems')

    def quick_buy(self, ui_id):
        '''
        Купить вещь из списка моментальных товаров. Забрать ее можно с помощью метода ItemRequest узнав ui_bid в методе Trades

        Параметры запроса:
            [ui_id] - Идентификатор предмета, который нужно взять из метода QuickItems.
        '''

        return self.get_json_resp(f'QuickBuy/{ui_id}')
#endregion
#region Дополнительно
    def test(self):
        '''
        Проверить все возможные препятствия к успешной продаже вещей.

        ВАЖНО! Все параметры должны быть "true", иначе продажа вещей невозможна.

        Пояснение к ответу:
            user_token — Установлена ли трейд ссылка
            trade_check — Пройдена ли проверка доступности трейд офферов - https://gifts.tm/check/
            site_online — Находитесь ли Вы в онлайне на сайте (Используйте метод PingPong)
            site_notmpban — Индикатор отсутствия бана за не передачу проданных вещей (на сутки)
        '''

        return self.get_json_resp('Test')

    def get_chat_log(self):
        '''
        Получить последние сообщения из чата Маркета. Это полезно, когда хочется найти интересные предложения в профилях 
        пользователей или просто следить за отправленными предметами в чат.
        '''

        return self.get_json_resp('GetChatLog')

    def check_bot_status(self, ui_bid):
        '''
        Проверить бота маркета на доступность для получения вещей. Если бот был забанен с купленной Вами вещью, Вы получите возврат денег.
        
        Параметры запроса:
            [ui_bid] — Идентификатор бота, который можно узнать c помощью метода Trades.
        '''

        return self.get_json_resp(f'CheckBotStatus/{ui_bid}')
#endregion


