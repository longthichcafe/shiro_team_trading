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
position_quant = {
    "COCONUTS": 0,
    "BANANAS": 0,
    "PINA_COLADAS": 0
}

position_average = {
    "COCONUTS": 0,
    "BANANAS": 0,
    "PINA_COLADAS": 0
}

profit = {
    "COCONUTS": 0,
    "BANANAS": 0,
    "PINA_COLADAS": 0
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


coconnuts = "COCONUTS"
bananas = "BANANAS"
pina = "PINA_COLADAS"


while checktime <= 100000:

    bananas_df = df[df['product'] == bananas]

    # get the number of rows in the dataframe
    num_rows = len(bananas_df)

    # initialize the row index to 0

    # loop through each row and access values one at a time using a while loop
    while row_index < num_rows:
        row = bananas_df.iloc[row_index]

        # check if row contains BANANAS
        if row['product'] == bananas:
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

    order_depths[bananas] = OrderDepth(
        buy_orders={bid_price_1: bid_volume_1,
                    bid_price_2: bid_volume_2,
                    bid_price_3: bid_volume_3},
        sell_orders={ask_price_1: ask_volume_1,
                     ask_price_2: ask_volume_2,
                     ask_price_3: ask_volume_3}
    )

    coconuts_df = df[df['product'] == coconnuts]

    # get the number of rows in the dataframe
    num_rows = len(coconuts_df)

    # initialize the row index to 0

    # loop through each row and access values one at a time using a while loop
    while row_index < num_rows:
        row = coconuts_df.iloc[row_index]

        # check if row contains COCONUTS
        if row['product'] == coconnuts:
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

    pinas_df = df[df['product'] == pina]

    # get the number of rows in the dataframe
    num_rows = len(pinas_df)

    # initialize the row index to 0

    # loop through each row and access values one at a time using a while loop
    while row_index < num_rows:
        row = pinas_df.iloc[row_index]

        # check if row contains PINA_COLADAS
        if row['product'] == pina:
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

    order_depths[pina] = OrderDepth(
        buy_orders={bid_price_1: bid_volume_1,
                    bid_price_2: bid_volume_2,
                    bid_price_3: bid_volume_3},
        sell_orders={ask_price_1: ask_volume_1,
                     ask_price_2: ask_volume_2,
                     ask_price_3: ask_volume_3}
    )

    # call the function
    result = trader.run(state=TradingState(
        timestamp=timestamp,
        listings=listings,
        order_depths=order_depths,
        own_trades=own_trades,
        market_trades=market_trades,
        position=position_quant,
        observations=observations
    ))

    # get positon from orders

    for item in result:
        if result[item]:
            quantity = result[item][0].quantity
            price = result[item][0].price
            # profit = profit[item]

            if np.sign(quantity) == np.sign(position_quant[item]) or position_quant[item] == 0:
                # calculate average
                position_average[item] = (
                    position_quant[item]*position_average[item] + quantity*price) / (quantity + position_quant[item])
                position_quant[item] += quantity

            else:
                # Trade is smaller
                if abs(quantity) < abs(position_quant[item]):
                    # Close part of Long position
                    if position_quant[item] > 0:
                        profit[item] += abs(quantity)*price - \
                            position_average[item]*abs(quantity)
                        position_quant[item] += quantity
                        # Position avg price stay same

                    # Close part of Short position
                    else:
                        profit[item] += position_average[item] * \
                            abs(quantity) - abs(quantity)*price
                        position_quant[item] += quantity
                        # Position avg price stay same

                # Trade is larger
                else:
                    # Close all of Long position and turn to Short
                    if position_quant[item] > 0:

                        profit[item] += abs(position_quant)[item]*price - \
                            position_average[item]*abs(position_quant)[item]
                        position_quant[item] += quantity
                        position_average[item] = price

                    # Close part of Short position and turn to Long
                    else:
                        profit[item] += position_average[item] * \
                            abs(position_quant[item]) - \
                            abs(position_quant[item])*price
                        position_quant[item] += quantity
                        position_average[item] = price

            # put the result in to output.csv file
    with open("output.csv", "a") as f:
        print(checktime, result, file=f)
    checktime += 100

print(profit)
