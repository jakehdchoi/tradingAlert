# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md

import time
import requests
import hashlib
import hmac
import json


from config import *

# from binance_api_requests import *

# from market_symbol_list import market_symbol_list


# def apply_lot_size(quantity, stepSize):
#     remainder = quantity % float(stepSize)
#     return quantity - remainder

# def apply_price_filter(price, tickSize):
#     remainder = price % float(tickSize)
#     return price - remainder


# ### Trade
# def trading_stop_loss_limit(flags_data): # not used anymore
#     if enable_debug_mode == True:
#         print('trading_stop_loss_limit_0')
#     try:
#         for i in range(5):
#             flags_data['BTC'] = get_balance_list_of('BTC')
#             quantity = float(flags_data['BTC']['free'])
#             filtered_quantity = apply_lot_size(quantity, flags_data['quantity_stepSize'])
#             if enable_debug_mode == True:
#                 print('filtered_quantity: ' + str(filtered_quantity))
#             if filtered_quantity > float(flags_data['quantity_stepSize']):
#                 break
#             else:
#                 if enable_debug_mode == True:
#                     print('trading_stop_loss_limit_1: sleep for 1 sec')
#                 time.sleep(1)

#         price = float(flags_data['trailing_stop_price'])
#         filtered_price = apply_price_filter(price, flags_data['price_tickSize'])
#         if enable_debug_mode == True:
#             print('filtered_price: ' + str(filtered_price))

#         if enable_production_mode == True:
#             url = 'https://www.binance.com/api/v3/order?'
#         else:
#             url = 'https://www.binance.com/api/v3/order/test?'
#         query = 'symbol=' + flags_data['market_symbol'] + '&side=SELL' + '&type=STOP_LOSS_LIMIT' + '&timeInForce=GTC' + '&quantity=' + format_float(filtered_quantity) + '&price=' + format_float(filtered_price) + '&stopPrice=' + format_float(filtered_price)
#         return signed_request(url, query, type='post')
#     except:
#         print('Binance error in public request: trade_stop_loss_limit for ' + flags_data['market_symbol'])
#         return 'error'


# def trading_logic_limit_order(flags_data): # 약간의 테스트 더 필요
#     flags_data['trading_counter'] = 0

#     if enable_debug_mode == True:
#         print('trading_logic_limit_order_0')
#     try:
#         if enable_debug_mode == True:
#             print('trading_logic_limit_order_1')
#         while True:
#             if enable_debug_mode == True:
#                 print('trading_logic_limit_order_2')

#             cancel_order(flags_data['market_symbol'])
#             time.sleep(3)

#             if enable_debug_mode == True:
#                 print('trading_logic_limit_order_3')
#             current_candle = get_period_candles(flags_data['market_symbol'], flags_data['interval_symbol'], timestamp(), 0)
#             price = float(current_candle[0][4])
#             filtered_price = apply_price_filter(price, flags_data['price_tickSize'])

#             balance_list = get_balance_list_full()
#             if flags_data['side'] == 'BUY':
#                 flags_data['USDT'] = cut_balance_list_of(balance_list, 'USDT')
#                 usdt_free = float(flags_data['USDT']['free'])
#                 quantity = usdt_free / filtered_price
#             else:
#                 flags_data['BTC'] = cut_balance_list_of(balance_list, 'BTC')
#                 quantity = float(flags_data['BTC']['free'])


#             filtered_quantity = apply_lot_size(quantity, flags_data['quantity_stepSize'])
#             if enable_print_mode == True:
#                 print('filtered_quantity: ' + str(filtered_quantity))

#             if filtered_quantity <= float(flags_data['quantity_stepSize']):
#                 break
#             elif flags_data['trading_counter'] >= 100:
#                 break

#             if enable_production_mode == True:
#                 url = 'https://www.binance.com/api/v3/order?'
#             else:
#                 url = 'https://www.binance.com/api/v3/order/test?'
#             query = 'symbol=' + flags_data['market_symbol'] + '&side=' + flags_data['side'] + '&type=LIMIT' + '&timeInForce=GTC' + '&quantity=' + format_float(filtered_quantity) + '&price=' + format_float(filtered_price)
#             signed_request(url, query, type='post')

#             flags_data['trading_counter'] += 1
#             if enable_debug_mode == True:
#                 print('trading_counter: ' + str(flags_data['trading_counter']))
#             # filtered_quantity가 현재 보유량보다 많은 경우가 생길 수 있을까?
#             # 에러 처리하는 logic 필요

#             time.sleep(27)

#         return True
#     except:
#         print('Binance error in public request: trade_limit_order for ' + flags_data['market_symbol'])
#         return False

# def cancel_order(market_symbol): # 7초 걸리던데..
#     try:
#         open_orders = get_open_orders(market_symbol)
#         # print(pjson(open_orders))
#         for i in open_orders:
#             if i['symbol'] == market_symbol:
#                 orderId = i['orderId']

#                 url = 'https://www.binance.com/api/v3/order?'
#                 query = 'symbol=' + market_symbol + '&orderId=' + str(orderId)
#                 print(signed_request(url, query, type='delete'))

#         return True
#     except:
#         print('Binance error in private request: cancel_order for ' + market_symbol)
#         return False

# def get_open_orders(market_symbol):
#     try:
#         url = 'https://www.binance.com/api/v3/openOrders?'
#         query = 'symbol=' + market_symbol
#         return signed_request(url, query)
#     except:
#         print('Binance error in private request: get_open_orders for ' + market_symbol)
#         return 'error'

# 미완성인 현재 캔들까지해서 period + 1 개 캔들을 불러온다 (현재 캔들은 open price 용도)
def get_period_candles(market_symbol, interval_symbol, endTime, period):
    try:
        startTime = endTime - \
            ((period + 1) * int(interval_symbol_lists[interval_symbol]))
        candle_data = simple_request('https://www.binance.com/api/v1/klines?symbol=' + market_symbol +
                                     '&interval=' + interval_symbol + '&startTime=' + str(startTime) + '&endTime=' + str(endTime))
        # return historical_data[-period:]
        return candle_data
    except:
        print('Binance error in public request: klines for ' + market_symbol)
        return 'error'
        # [
        #   [
        #     1499040000000,      // [0] Open time
        #     "0.01634790",       // [1] Open
        #     "0.80000000",       // [2] High
        #     "0.01575800",       // [3] Low
        #     "0.01577100",       // [4] Close
        #     "148976.11427815",  // [5] Volume
        #     1499644799999,      // [6] Close time
        #     "2434.19055334",    // [7] Quote asset volume 'BTC Volume'
        #     308,                // [8] Number of trades
        #     "1756.87402397",    // [9] Taker buy base asset volume
        #     "28.46694368",      // [10] Taker buy quote asset volume
        #     "17928899.62484339" // [11] Can be ignored
        #   ], ... []
        # ]


def get_exchange_info():
    return simple_request('https://www.binance.com/api/v1/exchangeInfo')


def get_btcusdt_market_info():
    exchange_info = simple_request(
        'https://www.binance.com/api/v1/exchangeInfo')['symbols']
    for symbol_info in exchange_info:
        if symbol_info['symbol'] == 'BTCUSDT':
            return symbol_info


def timestamp():
    try:
        timestamp = simple_request('https://www.binance.com/api/v1/time?')
        if timestamp is None or len(timestamp) == 0:
            return timestamp()
        else:
            return timestamp['serverTime']  # returning <int>
    except:
        print('Binance error in public request: timestamp')
        return 'error'


########## requests ##########

# def signed_request(url, query_input, type='get'):
#     # status_code 400: insufficient recvWindow
#     # status_code 404: wrong url
#     try:
#         recvWindow = 5000

#         while True:

#             query = query_input + '&recvWindow=' + str(recvWindow) + '&timestamp=' + str(timestamp())
#             signature = hmac.new((api_secret).encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
#             headers = {'X-MBX-APIKEY': api_key}

#             if type == 'get':
#                 r = requests.get(url + query + '&signature=' + signature, headers=headers)
#             elif type == 'post':
#                 r = requests.post(url + query + '&signature=' + signature, headers=headers)
#             elif type =='delete':
#                 r = requests.delete(url + query + '&signature=' + signature, headers=headers)

#             if r.status_code == 200: # successful
#                 return r.json()

#             else:
#                 if enable_debug_mode == True:
#                     print('recvWindow: ' + str(recvWindow))
#                     print(r.status_code)
#                     print('')

#                 t = time.time()
#                 log_t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
#                 log_status_code = str(r.status_code)


#                 try:
#                     with open(log_signed_error_file_location, 'r') as f:
#                         f.read()
#                     with open(log_signed_error_file_location, 'a') as f:
#                         f.write('\n' + log_t + ' ' + url + ' ' + query + ' ' + log_status_code + ' ' + str(recvWindow))
#                 except:
#                     log_error_data = 'local_date local_time signed_request_error_url signed_request_error_query status_code recvWindow'
#                     with open(log_signed_error_file_location, 'w') as f:
#                         f.write(log_error_data + '\n' + log_t + ' ' + url + ' ' + query + ' ' + log_status_code + ' ' + str(recvWindow))

#                 if recvWindow >= 20000: # requests failed
#                     raise SystemExit

#                 time.sleep(1)
#                 recvWindow += 1000

#     except:
#         print('Binance error in public request: signed_request')
#         raise SystemExit
#         print('SystemExit successful')


def simple_request(url):
    request_counter = 0
    while True:
        r = requests.get(url)
        if r.status_code == 200:  # successful
            return r.json()
        elif request_counter > 10:  # write log_trace & SystemExit
            t = time.time()
            log_t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            log_status_code = str(r.status_code)
            with open(log_trace_file_location, 'a') as f:
                f.write('\n' + log_t + ' simple_request_error ' +
                        url + ' status_code ' + log_status_code)
            raise SystemExit
        else:  # write log_simple_error
            request_counter += 1
            t = time.time()
            log_t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            log_status_code = str(r.status_code)
            try:
                with open(log_simple_error_file_location, 'r') as f:
                    f.read()
                with open(log_simple_error_file_location, 'a') as f:
                    f.write('\n' + log_t + ' ' + url + ' ' +
                            log_status_code + ' ' + str(request_counter))
            except:
                log_error_data = 'local_date local_time simple_request_error_url status_code request_counter'
                with open(log_simple_error_file_location, 'w') as f:
                    f.write(log_error_data + '\n' + log_t + ' ' + url +
                            ' ' + log_status_code + ' ' + str(request_counter))
            if enable_debug_mode == True:
                print(r)
            time.sleep(10)


########## utilities ##########

def cut_btc(symbol):
    return symbol.replace('BTC', '')


def format_float(a):
    return "%.8f" % a


def pjson(a):  # a = r.json()
    return json.dumps(a, indent=2, sort_keys=True, ensure_ascii=False)


def str2bool(a):  # 내가 직접 테스트 해보지는 않았음
    return a.lower() in ("yes", "true", "t", "1")
