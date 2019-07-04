
import time
import json


from config import *

from binance_api import *


def main():
    print('Starting tradingAlert...')

    start = time.time()
    print(time.strftime('start: ' +
                        '%Y-%m-%d %H:%M:%S', time.localtime(start)))
    print(time.strftime('utc: ' +
                        '%Y-%m-%d %H:%M:%S', time.gmtime(start)))
    #-#-#-#-#-#-#-#-#-#

    exchange_info = get_exchange_info()
    print(exchange_info)

    #-#-#-#-#-#-#-#-#-#
    print('')
    end = time.time()
    print(time.strftime('end: ' + '%Y-%m-%d %H:%M:%S', time.localtime(end)))
    print(time.strftime("total time elapsed: %H:%M:%S", time.gmtime(end - start)))


if __name__ == "__main__":
    main()
