import sys, getopt, time, math, os
from datetime import datetime
import json
from binance.client import Client
from binance.enums import *
import configparser

# make key.ini file for these to be read.
config = configparser.ConfigParser()
config.read('secrets.ini')
api_key = config['api']['key']
api_secret = config['api']['secret']

# DO NOT TOUCH AFTER THIS!
# BUT READ THE FOLLOWING
# USE AT YOUR OWN RISK.
# CHANGE AT YOUR OWN RISK.
# I DO NOT REFUND YOUR LOSSES.
# NOR I DO NOT NEED YOUR PROFITS.
# IT IS A GAME OF CHANGE.
# AND UP TO YOUR SETTINGS.
# AND CHANGES, SO PISS OF RANTING.
# I DO NOT TAKE RESPONSIBILITY.
# IT IS UP TO YOU TO USE THIS.
# Author Toni Lukkaroinen


pair = ""
kline_interval = Client.KLINE_INTERVAL_1MINUTE
emaa = "7"
emab = "25"
emaLength = "30"
emaOpen = "false"
getpairs = "false"
last = "none"
lastPrice = 0
rounding = 3
startingBalance = 0
allowNegative = "false"
negativeWay = "both"
lastTradeTime = 0
allowPanic = "false"
panicticks = 1
pairsearch = "none"
max = 0.0
sleeptime = 60
hilow = "false"
hilowp = 1.0
starttime = ""

def usage():
    print("This is Binance MA trading bot!")
    print("You can use this bot with your api keys, you need to change them in the script code api_key and api_secret.")
    print("After that you run the script again by giving the parameters needed for functionality.")
    print("--pair -c\t\tThe coin pair you trade on Binance. REQUIRED")
    print("--candlestick -i\t\tLength of the candlestick you want to use for MA calculations. Default 1m. ")
    print("\t\tValues for kline: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 3d, 1w, 1mo.")
    print("\t\tDefault 1m.")
    print("--emaa -a\t\tSmaller MA line value, such as default 7.")
    print("--emab -b\t\tBigger MA line value, such as default 25.")
    print("--length -l\tHow many candlesticks to use for calculating EMA. Default 30.")
    print("--max_amount -m\tMax amount of first coin, to trade. Example 0.1 or 1.5")
    print("--open -o\t\tDo you want to use open or closed price values. Default closed.")
    print("--allow_negative -n\tAllow doing negative trades, which do not make profit. No parameters.")
    print("--allow_panic -p\tAllow panic sell for the time of ticks you specify. No parameters.")
    print("--panic_ticks -t\tHow many candlesticks you check for panic sell. Default 1.")
    print("--get_pairs -g\tLists pairs used in binance. No parameters. Does not start the bot.")
    print("--pair_search -s\tSearch a pair with 3 letter string. For example BTC.")
    print("--rounding -x\tRound the trade amount to decimal places. Some pairs require only 2 decimals. Default 3.")
    print("--help -h\tShow this help. No parameters. Does not start the bot.")
    print("--hilow -d\tUse only HighLow trading and not EMA.")
    print("--hilowp -e\tHighLow trading mininum profit per trade.")
    sys.exit()

def parseOpts(argv):
    global pair, kline_interval, emaa, emab, emaLength, emaOpen, getpairs, Client, rounding, allowNegative, negativeWay, allowPanic, panicticks, pairsearch, max, rounding, hilow, hilowp, starttime
    try:
        opts, args = getopt.gnu_getopt(argv, "c:i:a:b:l:r:t:s:m:x:w:d:e:oghnp",
        ["pair=", "candlestick=", "emaa=", "emab=", "length=", "rounding=", "panic_ticks=", "pair_search=",
        "max_amount=", "rounding=", "negative_way=", "hilow=", "hilowp=", "open", "get_pairs", "help", "allow_negative", "allow_panic"])
        for opt, arg in opts:
            if opt in ("-i", "--candlestick"):
                if arg == "1m" or arg == "1M":
                    kline_interval = Client.KLINE_INTERVAL_1MINUTE
                elif arg == "3m" or arg == "3M":
                    kline_interval = Client.KLINE_INTERVAL_3MINUTE
                elif arg == "5m" or arg == "5M":
                    kline_interval = Client.KLINE_INTERVAL_5MINUTE
                elif arg == "15m" or arg == "15M":
                    kline_interval = Client.KLINE_INTERVAL_15MINUTE
                elif arg == "30m" or arg == "30M":
                    kline_interval = Client.KLINE_INTERVAL_30MINUTE
                elif arg == "1h" or arg == "1H":
                    kline_interval = Client.KLINE_INTERVAL_1HOUR
                elif arg == "2h" or arg == "2H":
                    kline_interval = Client.KLINE_INTERVAL_2HOUR
                elif arg == "4h" or arg == "4H":
                    kline_interval = Client.KLINE_INTERVAL_4HOUR
                elif arg == "6h" or arg == "6H":
                    kline_interval = Client.KLINE_INTERVAL_6HOUR
                elif arg == "8h" or arg == "8H":
                    kline_interval = Client.KLINE_INTERVAL_8HOUR
                elif arg == "12h" or arg == "12H":
                    kline_interval = Client.KLINE_INTERVAL_12HOUR
                elif arg == "1d" or arg == "1D":
                    kline_interval = Client.KLINE_INTERVAL_1DAY
                elif arg == "3d" or arg == "3D":
                    kline_interval = Client.KLINE_INTERVAL_3DAY
                elif arg == "1w" or arg == "1W":
                    kline_interval = Client.KLINE_INTERVAL_1WEEK
                elif arg == "1mo" or arg == "1MO":
                    kline_interval = Client.KLINE_INTERVAL_1MONTH
            elif opt in ("-c", "--pair"):
                pair = arg
            elif opt in ("-r", "--rounding"):
                rounding = arg
            elif opt in ("-t", "--panic_ticks"):
                panicticks = arg
            elif opt in ("-a", "--emaa"):
                emaa = arg
            elif opt in ("-b", "--emab"):
                emab = arg
            elif opt in ("-l", "--length"):
                emaLength = arg
            elif opt in ("-m", "--max_amount"):
                max = float(arg)
            elif opt in ("-x", "--rounding"):
                rounding = arg
            elif opt in ("-o", "--open"):
                emaOpen = "true"
            elif opt in ("-g", "--get_pairs"):
                getpairs = "true"
            elif opt in ("-s", "--pair_search"):
                getpairs = "true"
                pairsearch = arg
            elif opt in ("-h", "--help"):
                usage()
            elif opt in ("-n", "--allow_negative"):
                allowNegative = "true"
            elif opt in ("-w", "--negative_way"):
                negativeWay = arg
            elif opt in ("-p", "--allow_panic"):
                allowPanic = "true"
            elif opt in ("-d", "--hilow"):
                hilow = arg
            elif opt in ("-e", "--hilowp"):
                hilowp = float(arg)
            else:
                usage()
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()

def currentTimeMillis():
    ctime = round(time.time() * 1000)
    return ctime

def timeFromCurrentTime(timestamp):
    ctime = currentTimeMillis() - int(timestamp)
    return ctime

def EMAStartTime(emaLength):
    ctime = timeFromCurrentTime(int(emaLength) * 24 * 60 * 60 * 60)
    return ctime

def calculateEMA(klines, days=5, smoothing=2):
    global emaOpen
    openId = 4
    if emaOpen == "true":
        openId = 2
    prices = []
    for x in klines:
        prices.append(float(x[openId]))
    ema = [sum(prices[:int(days)]) / int(days)]
    for price in prices[int(days):]:
        ema.append((price * (smoothing / (1 + int(days)))) + ema[-1] * (1 - (smoothing / (1 + int(days)))))
    return ema

def calculateLastEMA(klines, days=5, smoothing=2):
    EMA = calculateEMA(klines, days, smoothing)
    length = len(EMA)
    return EMA[length-1];

def round_decimals_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        print("decimal places must be an integer")
    elif decimals < 0:
        print("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def buy(client, pair, qty, price):
    global last, rounding, max, sleeptime
    qty = round_decimals_down(float(qty) * 0.95, int(rounding))
    if float(qty) <= 0.001 and pair == "ETHBTC":
        last = "bought"
        return
    if max != 0:
        if float(qty) > float(max):
            qty = float(max)
    print("Buy quantity " + str(qty))
    print("Byuing " + pair[:3] + " at " + price + " amount " + str(qty))
    order = client.create_order(
        symbol=pair,
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=qty,
        price=price)
    last = "bought"
    time.sleep(sleeptime)

def sell(client, pair, qty, price):
    global last, rounding, sleeptime
    qty = round_decimals_down(float(qty) * 0.95, int(rounding))
    if float(qty) <= 0.001 and pair == "ETHBTC":
        last = "sold"
        return
    print("Sell quantity " + str(qty))
    print("Selling " + pair[:3] + " at " + price + " amount " + str(qty))
    order = client.create_order(
        symbol=pair,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=qty,
        price=price)
    last = "sold"
    time.sleep(sleeptime)

def getStartingBalance(client):
    global startingBalance
    balance = client.get_asset_balance(asset=pair[3:])
    if balance != None:
        startingBalance = balance['free']

def trade():
    global pair, kline_interval, emaa, emab, emaLength, emaOpen, getpairs, last, startingBalance, allowNegative, negativeWay, allowPanic, lastTradeTime, panicticks, pairsearch, max, sleeptime, hilow, hilowp, starttime
    parseOpts(sys.argv[1:])
    client = Client(api_key, api_secret, testnet=False)
    if getpairs == "true":
        coin_info = client.get_all_tickers()
        if pairsearch != "none":
            for coin in coin_info:
                if len(coin['symbol']) == 6:
                    if coin['symbol'].find(pairsearch) > 0:
                        print(json.dumps(coin, indent=4, sort_keys=False))
            return
        else:
            for coin in coin_info:
                if len(coin['symbol']) == 6:
                    print(json.dumps(coin, indent=4, sort_keys=False))
            return
    if pair == "" or api_key == "" or api_secret == "":
        usage()
    time_res = client.get_server_time()
    getStartingBalance(client)
    starttime = time.ctime()
    while 'serverTime' in time_res:
        os.system('cls||clear')
        print("-------------------------------------------------------")
        print("")
        balA = 0
        balB = 0
        if len(pair) == 6:
            balanceA = client.get_asset_balance(asset=pair[:3])
            if balanceA != None:
                balA = balanceA['free']
            balanceB = client.get_asset_balance(asset=pair[3:])
            if balanceB != None:
                balB = balanceB['free']
        elif len(pair) == 7:
            balanceA = client.get_asset_balance(asset=pair[:3])
            if balanceA != None:
                balA = balanceA['free']
            balanceB = client.get_asset_balance(asset=pair[4:])
            if balanceB != None:
                balB = balanceB['free']
        print("Balances: " + str(balA) + " " + pair[:3] + ", " + str(balB) + " " + pair[3:])
        print("Started trading:      " + starttime)
        print("Current time:         " + time.ctime())
        start = EMAStartTime(emaLength)
        end = currentTimeMillis()
        klines = client.get_historical_klines(pair, kline_interval, start, end)
        print("Candlestick interval: " + kline_interval)
        EMAA = float(calculateLastEMA(klines, emaa))
        if hilow != "true":
            print("EMA " + str(emaa) + ":                " + str(EMAA))
        EMAB = float(calculateLastEMA(klines, emab))
        if hilow != "true":
            print("EMA " + str(emab) + ":               " + str(EMAB))
        emadiff = float(EMAA) - float(EMAB)
        if hilow != "true":
            print("EMA difference:       " + str(emadiff))
        if max != 0:
            print("Max trade enabled:    true " + str(max) + " " + pair[:3])
        if hilow != "true":
            print("Allow negative trade: " + allowNegative)
        if hilow != "true":
            print("Allow panic trade:    " + allowPanic)
        print("Allow high/low trade: " + hilow)
        openOrders = client.get_open_orders(symbol=pair)
        if len(openOrders) == 0:
            orders = client.get_all_orders(symbol=pair)
            lastPrice = 0
            lastOrder = 0
            if len(orders) > 0:
                for i in reversed(orders):
                    if i['status'] == "CANCELED":
                        continue
                    else:
                        lastPrice = float(i['price'])
                        lastOrder = i
                        if i['side'] == "BUY":
                            last = "bought"
                        elif i['side'] == "SELL":
                            last = "sold"
                        break
            prices = client.get_all_tickers()
            price = 0
            for p in prices:
                if p['symbol'] == pair:
                    price = p['price']
                    break
            print("Curr price:           " + str(price))
            if last == "bought":
                print("Last price:           " + str(lastPrice) + " + 0.01% = " + str(float(lastPrice) + (float(lastPrice) * 0.001)))
            elif last == "sold":
                print("Last price:           " + str(lastPrice) + " + 0.01% = " + str(float(lastPrice) + (float(lastPrice) * 0.001)))
            else:
                print("Last price:           " + str(float(lastPrice)))
            print("Last trade was:       " + last)
            allTimeProfit = 0
            if len(orders) > 0:
                lastP = 0
                for order in orders:
                    if order['status'] == "CANCELED":
                        continue
                    elif float(order['price']) == 0:
                        continue
                    elif lastP == 0:
                        lastP = float(order['price'])
                        continue
                    else:
                        if order['side'] == "BUY":
                           allTimeProfit = allTimeProfit + (lastP - float(order['price'])) / float(order['price']) * 100
                        elif order['side'] == "SELL":
                           allTimeProfit = allTimeProfit + (float(order['price']) - lastP) / lastP * 100
                        lastP = float(order['price'])
            print("All time profit:      " + str(round_decimals_down(allTimeProfit, 2)) + "%")
            if float(price) != 0 and float(lastPrice) != 0:
                if last == "bought":
                    print("Profit next trade:    " + str(round_decimals_down((float(price) - float(lastPrice)) / float(lastPrice) * 100, 2)) + "%")
                elif last == "sold":
                    print("Profit next trade:    " + str(round_decimals_down((float(lastPrice) - float(price)) / float(price) * 100, 2)) + "%")
            if float(startingBalance) != 0:
                if (float(balB) - float(startingBalance)) / float(startingBalance) * 100 > 500:
                    getStartingBalance(client)
                #print("Runtime profit:       " + str(round_decimals_down((float(startingBalance) - float(balB)) / float(balB) * 100, 2)) + "%")
            panictime = 0
            if kline_interval == Client.KLINE_INTERVAL_1MINUTE:
                panictime = 60000 * float(panicticks)
                sleeptime = 60
            elif kline_interval == Client.KLINE_INTERVAL_3MINUTE:
                panictime = 3 * 60000 * float(panicticks)
                sleeptime = 3 * 60
            elif kline_interval == Client.KLINE_INTERVAL_5MINUTE:
                panictime = 5 * 60000 * float(panicticks)
                sleeptime = 5 * 60
            elif kline_interval == Client.KLINE_INTERVAL_15MINUTE:
                panictime = 15 * 60000 * float(panicticks)
                sleeptime = 15 * 60
            elif kline_interval == Client.KLINE_INTERVAL_30MINUTE:
                panictime = 30 * 60000 * float(panicticks)
                sleeptime = 30 * 60
            elif kline_interval == Client.KLINE_INTERVAL_1HOUR:
                panictime = 60 * 60000 * float(panicticks)
                sleeptime = 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_2HOUR:
                panictime = 2 * 60 * 60000 * float(panicticks)
                sleeptime = 2 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_4HOUR:
                panictime = 4 * 60 * 60000 * float(panicticks)
                sleeptime = 4 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_6HOUR:
                panictime = 6 * 60 * 60000 * float(panicticks)
                sleeptime = 6 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_8HOUR:
                panictime = 8 * 60 * 60000 * float(panicticks)
                sleeptime = 8 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_12HOUR:
                panictime = 12 * 60 * 60000 * float(panicticks)
                sleeptime = 12 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_1DAY:
                panictime = 24 * 60 * 60000 * float(panicticks)
                sleeptime = 24 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_3DAY:
                panictime = 3 * 24 * 60 * 60000 * float(panicticks)
                sleeptime = 3 * 24 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_1WEEK:
                panictime = 7 * 24 * 60 * 60000 * float(panicticks)
                sleeptime = 7 * 24 * 60 * 60
            elif kline_interval == Client.KLINE_INTERVAL_1MONTH:
                panictime = 30 * 24 * 60 * 60000 * float(panicticks)
                sleeptime = 30 * 24 * 60 * 60
            if panictime != 0:
                if lastOrder != 0:
                    if hilow != "true":
                        pt = datetime.fromtimestamp((float(lastOrder['time']) + float(panictime)) / 100)
                        print("Panic time:           " + pt.ctime())
            dt = datetime.fromtimestamp(float(time_res['serverTime']) / 1000)
            print("Server time:          " + dt.ctime())
            if hilow == "true":
                if last == "none":
                    if float(balA) > 0: # Sell first coin of pair if has balance for it.
                        if lastOrder != 0:
                            if lastOrder['executedQty'] <= balA:
                                sell(client, pair, balA, price)
                            else:
                                sell(client, pair, lastOrder['executedQty'], price)
                        else:
                            sell(client, pair, balA, price)
                    elif float(balB) > 0: # Buy first coin of pair if has balance for it.
                        buy(client, pair, float(balB) / float(price), price)
                elif last == "bought":
                    prof = (float(price) - float(lastPrice)) / float(lastPrice) * 100
                    if prof >= hilowp:
                        if lastOrder['executedQty'] <= balA:
                            sell(client, pair, balA, price)
                        else:
                            sell(client, pair, lastOrder['executedQty'], price)
                elif last == "sold":
                    prof = (float(lastPrice) - float(price)) / float(price) * 100
                    if prof >= hilowp:
                        if float(balB) > 0:
                            buy(client, pair, float(balB) / float(price), price)
            elif hilow == "false":
                print("Trading mode:         EMA")
                if last == "none":
                    if emadiff < 0 and float(balA) > 0: # sell first coin of pair if has balance for it
                        if lastOrder != 0:
                            if allowPanic == "true" and float(lastOrder['time']) + 604800000 < float(time_res['serverTime']) or lastPrice == 0.0:
                                if lastOrder['executedQty'] <= balA:
                                    sell(client, pair, lastOrder['executedQty'], price)
                                else:
                                    sell(client, pair, balA, price)
                        if float(price) > float(lastPrice) + (float(lastPrice) * 0.001) or lastPrice == 0.0 or (allowNegative == "true" and (negativeWay == "both" or negativeWay == "sell")):
                            if lastOrder['executedQty'] <= balA:
                                sell(client, pair, lastOrder['executedQty'], price)
                            else:
                                sell(client, pair, balA, price)
                    elif emadiff > 0 and float(balB) > 0: # buy first coin of pair if has balance for it
                        if lastOrder != 0:
                            if allowPanic == "true" and float(lastOrder['time']) + 604800000 < float(time_res['serverTime']) or lastPrice == 0.0:
                                buy(client, pair, float(balB) / float(price), price)
                        if float(price) < float(lastPrice) - (float(lastPrice) * 0.001) or lastPrice == 0.0 or (allowNegative == "true" and (negativeWay == "both" or negativeWay == "buy")):
                            buy(client, pair, float(balB) / float(price), price)
                elif last == "bought":
                    if emadiff < 0: # sell first coin of pair if has balance for it
                        if lastOrder != 0:
                            if panictime > 0 and float(lastOrder['time']) + float(panictime) > float(time_res['serverTime']) and allowPanic == "true":
                                if lastOrder['executedQty'] <= balA:
                                    sell(client, pair, balA, price)
                                else:
                                    sell(client, pair, lastOrder['executedQty'], price)
                        if float(price) > float(lastPrice) + (float(lastPrice) * 0.001) or lastPrice == 0.0 or  (allowNegative == "true" and (negativeWay == "both" or negativeWay == "sell")): # Current price bigger than last price when bought
                                if lastOrder['executedQty'] <= balA:
                                    sell(client, pair, balA, price)
                                else:
                                    sell(client, pair, lastOrder['executedQty'], price)
                elif last == "sold":
                    if emadiff > 0: # buy first coin of pair if has balance for it
                        if lastOrder != 0:
                            if panictime > 0 and float(lastOrder['time']) + float(panictime) > float(time_res['serverTime']) and allowPanic == "true":
                                buy(client, pair, float(balB) / float(price), price)
                        if float(price) < float(lastPrice) - (float(lastPrice) * 0.001) or lastPrice == 0.0 or (allowNegative == "true" and (negativeWay == "both" or negativeWay == "buy")): # Current price smaller than last price when sold
                            buy(client, pair, float(balB) / float(price), price)
        else:
            for o in openOrders:
                print("Open ID " + str(o['orderId']) + ", " + o['symbol'] + " " + o['side'] + " order, at price " + str(o['price']))
                print("Order time + 5min:     " + str(o['time'] + (5 * 60 * 60)))
                print("Server time:           " + str(time_res['serverTime']))
                if float(o['time']) + (5 * 60000) < float(time_res['serverTime']):
                    print("Cancelling order" + str(o['orderId']) + " ID, because 5 minutes has passed.")
                    client.cancel_order(symbol=o['symbol'], orderId=o['orderId'])
        time.sleep(sleeptime / 6)

def main():
    global getpairs
    while True:
        try:
            trade()
            if getpairs == "true":
                return
        except Exception:
            time.sleep(60*10)
            pass

if __name__ == "__main__":
    #trade()
    main()
