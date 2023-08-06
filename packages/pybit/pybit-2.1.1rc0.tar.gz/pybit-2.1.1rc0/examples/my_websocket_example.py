"""
To see which endpoints and topics are available, check the Bybit API
documentation: https://bybit-exchange.github.io/docs/inverse/#t-websocket

There are several WSS URLs offered by Bybit, which pybit manages for you.
However, you can set a custom `domain` as shown below.
"""

from time import sleep

# Import your desired markets from pybit
from pybit import usdc_perpetual, usdt_perpetual, inverse_perpetual, spot

"""
An alternative way to import:
from pybit.inverse_perpetual import WebSocket, HTTP
"""

# Set up logging (optional)
import logging
logging.basicConfig(filename="pybit.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

api_key = "yrusSyuhtwc8zHAqfA"
api_secret = "QHcfc4YwvA2zzqXJBKu7FNz5uK55PmhhVQfH"

# Connect with authentication!
ws_inverse = usdt_perpetual.WebSocket(
    test=False,
    api_key=api_key,  # omit the api_key & secret to connect w/o authentication
    api_secret=api_secret,
    # to pass a custom domain in case of connectivity problems, you can use:
    #domain="bytick",  # the default is "bybit"
    trace_logging=True


)
def handle_orderbook(message):
    print(message)
    #orderbook_data = message["data"]
    #print(len(orderbook_data))

ws_inverse.trade_stream(handle_orderbook, "BTCUSDT")
#ws_inverse.position_stream(handle_orderbook)
#ws_inverse.order_stream(handle_orderbook)

while True:
    # Run your main trading logic here.
    sleep(1)
