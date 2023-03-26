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


def assign(row, product):
    # todo: do dolphin case
    dataframe = df[df['product'] == product]
    row = dataframe.iloc[row]
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

    order_depths[product] = OrderDepth(
        buy_orders={bid_price_1: bid_volume_1,
                    bid_price_2: bid_volume_2,
                    bid_price_3: bid_volume_3},
        sell_orders={ask_price_1: -ask_volume_1,
                     ask_price_2: -ask_volume_2,
                     ask_price_3: -ask_volume_3}
    )
    # print(order_depths[product].buy_orders)


while checktime <= TIMESTAMP:
    assign(index, coconnuts)
    assign(index, bananas)
    assign(index, pina)
    assign(index, berrie)
    assign(index, diving)

    result = trader.run(state=TradingState(
        timestamp=checktime,
        listings=listings,
        order_depths=order_depths,
        own_trades=own_trades,
        market_trades=market_trades,
        position=position_quant,
        observations=observations
    ))

    for item in profit:
        if result[item]:
            quantity_temp = result[item][0].quantity
            if np.sign(quantity_temp) == 1:
                if quantity_temp > -list(order_depths[item].sell_orders.values())[0]:
                    quantity = - \
                        list(order_depths[item].sell_orders.values())[0]
                else:
                    quantity = quantity_temp
            elif np.sign(quantity_temp) == -1:
                if quantity_temp < -list(order_depths[item].buy_orders.values())[0]:
                    quantity = -list(order_depths[item].buy_orders.values())[0]
                else:
                    quantity = quantity_temp
            else:
                quantity = 0

            price = result[item][0].price

            # profit = profit[item]

            if np.sign(quantity) == np.sign(position_quant[item]) or position_quant[item] == 0 or quantity == 0:
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

                        profit[item] += abs(position_quant[item])*price - \
                            position_average[item]*abs(position_quant[item])
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
        print(checktime, result, profit, file=f)

    checktime += 100
    index += 1
print(profit)
print(order_depths[bananas].buy_orders)
