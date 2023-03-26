from algo import *

import random
import pandas as pd
import numpy as np

timestamp = 0

listings = {
    "BANANAS": Listing(
        symbol="BANANAS",
        product="BANANAS",
        denomination="SEASHELLS"
    ),
    "COCONUTS": Listing(
        symbol="COCONUTS",
        product="COCONUTS",
        denomination="SEASHELLS"
    ),
    "PINA_COLADAS": Listing(
        symbol="PINA_COLADAS",
        product="PINA_COLADAS",
        denomination="SEASHELLS"
    ),
    "BERRIES": Listing(
        symbol="BERRIES",
        product="BERRIES",
        denomination="SEASHELLS"
    ),
    "DIVING_GEAR": Listing(
        symbol="DIVING_GEAR",
        product="DIVING_GEAR",
        denomination="SEASHELLS"
    ),
}
# Orders sent by trading bots  == TEST INPUT


# the trades that the algorithm has done from previous TradingState
own_trades = {
    "PRODUCT1": [],
    "PRODUCT2": []
}

# the trades that other people has done from previous timestamp (ONLY 1)
market_trades = {
    "PRODUCT1": [
        Trade(
            symbol="PRODUCT1",
            price=11,
            quantity=4,
            buyer="",
            seller="",
        )
    ]
}

# what we have
position_quant = {
    "COCONUTS": 0,
    "BANANAS": 0,
    "PINA_COLADAS": 0,
    "BERRIES": 0,
    "DIVING_GEAR": 0
}

position_average = {
    "COCONUTS": 0,
    "BANANAS": 0,
    "PINA_COLADAS": 0,
    "BERRIES": 0,
    "DIVING_GEAR": 0
}

profit = {
    "COCONUTS": 0,
    "BANANAS": 0,
    "PINA_COLADAS": 0,
    "BERRIES": 0,
    "DIVING_GEAR": 0
}

observations = {}


# ==============================================================  TEST ==============================================================
# ==============================================================  TEST ==============================================================
# ==============================================================  TEST ==============================================================

filepath = "src/test.csv"
df = pd.read_csv(filepath, delimiter=';', usecols=['product', 'bid_price_1', 'bid_volume_1', 'bid_price_2', 'bid_volume_2',
                                                   'bid_price_3', 'bid_volume_3', 'ask_price_1', 'ask_volume_1', 'ask_price_2', 'ask_volume_2', 'ask_price_3', 'ask_volume_3', 'mid_price'])

checktime = 0

trader = Trader()
index = 0
row_index = 0

order_depths = {}

TIMESTAMP = 100000

coconnuts = "COCONUTS"
bananas = "BANANAS"
pina = "PINA_COLADAS"
berrie = "BERRIES"
diving = "DIVING_GEAR"

# while checktime <= 1:

bananas_df = df[df['product'] == bananas]
row = bananas_df.iloc[0]
bid_price_1 = row['bid_price_1']
bid_volume_1 = row['bid_volume_1']
bid_price_2 = row['bid_price_2']
bid_volume_2 = row['bid_volume_2']
bid_price_3 = row['bid_price_3']
bid_volume_3 = row['bid_volume_3']
ask_price_1 = row['ask_price_1']
ask_volume_1 = row['ask_volume_1']
ask_price_2 = row['ask_price_2']
ask_volume_2 = row['ask_volume_2']
ask_price_3 = row['ask_price_3']
ask_volume_3 = row['ask_volume_3']

order_depths[bananas] = OrderDepth(
    buy_orders={bid_price_1: bid_volume_1,
                bid_price_2: bid_volume_2,
                bid_price_3: bid_volume_3},
    sell_orders={ask_price_1: -ask_volume_1,
                 ask_price_2: -ask_volume_2,
                 ask_price_3: -ask_volume_3}
)
print(order_depths[bananas].buy_orders)
