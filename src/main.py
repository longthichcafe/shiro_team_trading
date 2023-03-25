from algo import *

import random
import pandas as pd

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
    denomination="PINA_COLADAS"
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
position = {
    "PRODUCT1": 0,
    "PRODUCT2": 0
}

observations = {}


# ==============================================================  TEST ==============================================================
# ==============================================================  TEST ==============================================================
# ==============================================================  TEST ==============================================================

filepath = "src/test.csv"
df = pd.read_csv(filepath, delimiter=';', usecols=['product', 'bid_price_1', 'bid_volume_1', 'bid_price_2', 'bid_volume_2',
                                                   'bid_price_3', 'bid_volume_3', 'ask_price_1', 'ask_volume_1', 'ask_price_2', 'ask_volume_2', 'ask_price_3', 'ask_volume_3'])

checktime = 0

trader = Trader() 
index = 0
row_index = 0

order_depths = {}

# TODO: profit


while checktime <= 100000:

    bananas_df = df[df['product'] == 'BANANAS']

    # get the number of rows in the dataframe
    num_rows = len(bananas_df)

    # initialize the row index to 0

    # loop through each row and access values one at a time using a while loop
    while row_index < num_rows:
        row = bananas_df.iloc[row_index]

        # check if row contains BANANAS
        if row['product'] == 'BANANAS':
            product = row['product']
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
            break
        else:
            row_index += 1
    row_index += 1

    order_depths["BANANAS"] = OrderDepth(
        buy_orders={bid_price_1: bid_volume_1,
                    bid_price_2: bid_volume_2,
                    bid_price_3: bid_volume_3},
        sell_orders={ask_price_1: ask_volume_1,
                        ask_price_2: ask_volume_2,
                        ask_price_3: ask_volume_3}
    )
    

    coconuts_df = df[df['product'] == 'COCONUTS']

    # get the number of rows in the dataframe
    num_rows = len(coconuts_df)

    # initialize the row index to 0

    # loop through each row and access values one at a time using a while loop
    while row_index < num_rows:
        row = coconuts_df.iloc[row_index]

        # check if row contains COCONUTS
        if row['product'] == 'COCONUTS':
            product = row['product']
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
            break
        else:
            row_index += 1
    row_index += 1

    order_depths["COCONUTS"] = OrderDepth(
        buy_orders={bid_price_1: bid_volume_1,
                    bid_price_2: bid_volume_2,
                    bid_price_3: bid_volume_3},
        sell_orders={ask_price_1: ask_volume_1,
                        ask_price_2: ask_volume_2,
                        ask_price_3: ask_volume_3}
    )


    pinas_df = df[df['product'] == 'PINA_COLADAS']

    # get the number of rows in the dataframe
    num_rows = len(pinas_df)

    # initialize the row index to 0

    # loop through each row and access values one at a time using a while loop
    while row_index < num_rows:
        row = pinas_df.iloc[row_index]

        # check if row contains PINA_COLADAS
        if row['product'] == 'PINA_COLADAS':
            product = row['product']
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
            break
        else:
            row_index += 1
    row_index += 1

    order_depths["PINA_COLADAS"] = OrderDepth(
        buy_orders={bid_price_1: bid_volume_1,
                    bid_price_2: bid_volume_2,
                    bid_price_3: bid_volume_3},
        sell_orders={ask_price_1: ask_volume_1,
                        ask_price_2: ask_volume_2,
                        ask_price_3: ask_volume_3}
    )


    # print(bid_price_1, bid_volume_1, bid_price_2, bid_volume_2)
    print(checktime, trader.run(state=TradingState(
        timestamp=timestamp,
        listings=listings,
        order_depths=order_depths,
        own_trades=own_trades,
        market_trades=market_trades,
        position=position,
        observations=observations
    )))

    checktime += 100

