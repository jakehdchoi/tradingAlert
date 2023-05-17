import time
import json


from config import *

from api_binance import *
from api_telegram import *

# ddd
# telegram (use config)
# my_token = '708058741:AAE_Adii3xQhfZTxo4hxbHxj9nYpBeuHmsw'
# chat_id = '386497377'

# 뭔가를 열심히 적어

interval_symbol = "1w"
period_list = [20, 55]

full_symbol_list = []
above_20w_list = []
above_55w_list = []

tier_1_list = []  # above 20w & 55w
tier_2_list = []  # above 20w - tier_1


def main():
    print("Starting tradingAlert...")

    start = time.time()
    print(time.strftime("start: " + "%Y-%m-%d %H:%M:%S", time.localtime(start)))
    print(time.strftime("utc: " + "%Y-%m-%d %H:%M:%S", time.gmtime(start)))
    # -#-#-#-#-#-#-#-#-#

    # create full symbol list
    exchange_info = get_exchange_info()
    for exchange_symbol in exchange_info["symbols"]:
        market_symbol = exchange_symbol["symbol"]
        if market_symbol.endswith("BTC") == True:
            full_symbol_list.append(market_symbol)
    # print(full_symbol_list)

    # logic
    endTime = int(timestamp())  # for candle data
    for period in period_list:
        for market_symbol in full_symbol_list:
            print(
                "processing[{}w]: {} [{}/{}]".format(
                    period,
                    market_symbol,
                    int(full_symbol_list.index(market_symbol)) + 1,
                    len(full_symbol_list),
                )
            )
            candle_data = get_period_candles(
                market_symbol, interval_symbol, endTime, period
            )

            # passing market symbols that aren't enough candle data
            if len(candle_data) == period + 1:
                # del candle_data[-1]
                pass
            else:
                print("not enough candle data:", len(candle_data))
                continue

            # print('candle_data:', len(candle_data))

            close_sum = 0
            for candle in candle_data:
                close_sum += float(candle[4])
            sma = close_sum / (period + 1)
            # print(sma)

            if float(candle_data[-1][4]) > sma:
                if period == 20:
                    above_20w_list.append(market_symbol)
                else:
                    above_55w_list.append(market_symbol)

    print("above_20w_list:", above_20w_list)
    print("above_55w_list:", above_55w_list)

    for ele in above_55w_list:
        if ele in above_20w_list:
            tier_1_list.append(ele)

    print("tier_1_list:", tier_1_list)

    for ele in above_20w_list:
        if ele not in tier_1_list:
            tier_2_list.append(ele)

    print("tier_2_list:", tier_2_list)

    # generate telegram message
    msg = (
        time.strftime("%Y-%m-%d", time.localtime(start))
        + "\n\ntier_1_list: \n"
        + str(tier_1_list)
        + "\n\ntier_2_list: \n"
        + str(tier_2_list)
    )

    # sendMessage to telegram
    sendMessage(msg)

    # -#-#-#-#-#-#-#-#-#
    print("")
    end = time.time()
    print(time.strftime("end: " + "%Y-%m-%d %H:%M:%S", time.localtime(end)))
    print(time.strftime("total time elapsed: %H:%M:%S", time.gmtime(end - start)))


if __name__ == "__main__":
    main()
