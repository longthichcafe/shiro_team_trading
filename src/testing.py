from algo import *

import random
import pandas as pd
import numpy as np

timestamp = 0

listings = {
    "PEARLS": Listing(
        symbol="PEARLS",
        product="PEARLS",
        denomination="SEASHELLS"
    ),
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
    "BAGUETTE": Listing(
        symbol="BAGUETTE",
        product="BAGUETTE",
        denomination="SEASHELLS"
    ),
    "DIP": Listing(
        symbol="DIP",
        product="DIP",
        denomination="SEASHELLS"
    ),
    "UKULELE": Listing(
        symbol="UKULELE",
        product="UKULELE",
        denomination="SEASHELLS"
    ),
    "PICNIC_BASKET": Listing(
        symbol="PICNIC_BASKET",
        product="PICNIC_BASKET",
        denomination="SEASHELLS"
    ),
    "PICNIC_BASKET": Listing(
        symbol="PICNIC_BASKET",
        product="PICNIC_BASKET",
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
    "PEARLS": 0,
    "BANANAS": 0,
    "COCONUTS": 0,
    "PINA_COLADAS": 0,
    "BERRIES": 0,
    "DIVING_GEAR": 0,
    "BAGUETTE": 0,
    "DIP": 0,
    "UKULELE": 0,
    "PICNIC_BASKET": 0,
}

position_average = {
    "PEARLS": 0,
    "BANANAS": 0,
    "COCONUTS": 0,
    "PINA_COLADAS": 0,
    "BERRIES": 0,
    "DIVING_GEAR": 0,
    "BAGUETTE": 0,
    "DIP": 0,
    "UKULELE": 0,
    "PICNIC_BASKET": 0,
}

profit = {
    "PEARLS": 0,
    "BANANAS": 0,
    "COCONUTS": 0,
    "PINA_COLADAS": 0,
    "BERRIES": 0,
    "DIVING_GEAR": 0,
    "BAGUETTE": 0,
    "DIP": 0,
    "UKULELE": 0,
    "PICNIC_BASKET": 0,
}

observations = {}

# ==============================================================  TEST ==============================================================
# ==============================================================  TEST ==============================================================
# ==============================================================  TEST ==============================================================

filepath = "src/test.csv"
df = pd.read_csv(filepath, 
    delimiter = ';', 
    usecols = [
        'product', 
        'bid_price_1', 
        'bid_volume_1', 
        'bid_price_2', 
        'bid_volume_2',
        'bid_price_3', 
        'bid_volume_3', 
        'ask_price_1', 
        'ask_volume_1', 
        'ask_price_2', 
        'ask_volume_2', 
        'ask_price_3', 
        'ask_volume_3', 
        'mid_price'
    ]
)

checktime = 0
trader = Trader()
index = 0
row_index = 0
order_depths = {}

TIMESTAMP = 1000000

pearl = "PEARLS"
bananas = "BANANAS"
coconuts = "COCONUTS"
pina = "PINA_COLADAS"
berrie = "BERRIES"
diving = "DIVING_GEAR"
dolphin = "DOLPHIN_SIGHTINGS"
baguette = "BAGUETTE"
dip = "DIP"
uku = "UKULELE"
basket = "PICNIC_BASKET"


def assign(row, product):
    # assign diving gear
    dataframe = df[df['product'] == product]
    row = dataframe.iloc[row]
    if product == "DOLPHIN_SIGHTINGS":
        observations["DOLPHIN_SIGHTINGS"] = row["mid_price"]
    else:
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
            buy_orders = {
                bid_price_1: bid_volume_1,
                bid_price_2: bid_volume_2,
                bid_price_3: bid_volume_3
            },
            sell_orders = {
                ask_price_1: -ask_volume_1,
                ask_price_2: -ask_volume_2,
                ask_price_3: -ask_volume_3
            }
        )
    # print(order_depths[product].buy_orders)


while checktime <= TIMESTAMP:
    assign(index, pearl)
    assign(index, bananas)
    assign(index, coconuts)
    assign(index, pina)
    assign(index, berrie)
    assign(index, diving)
    assign(index, dolphin)
    assign(index, baguette)
    assign(index, dip)
    assign(index, uku)
    assign(index, basket)
    

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

            if np.sign(quantity) == np.sign(position_quant[item]) or position_quant[item] == 0:
                # calculate average
                position_average[item] = (
                    position_quant[item]*position_average[item] + quantity*price) / (quantity + position_quant[item])
                position_quant[item] += quantity

            if np.sign(quantity) + np.sign(position_quant[item]) == 0:
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
                elif abs(quantity) > abs(position_quant[item]):
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
                
                # Trade equals position
                else:
                    # Close all of Long position
                    if position_quant[item] > 0:

                        profit[item] += abs(quantity)*price - \
                            position_average[item]*abs(quantity)
                        position_quant[item] = 0
                        position_average[item] = 0

                    # Close part of Short position
                    else:
                        profit[item] += position_average[item] * \
                            abs(quantity) - \
                            abs(quantity)*price
                        position_quant[item] = 0
                        position_average[item] = 0


    # put the result in to output.csv file
    with open("output.csv", "a") as f:
        if result[pina]:
            print(
                checktime,
                pina,
                result[pina][0].price,
                result[pina][0].quantity,          
                profit[pina], 
                sep=';',
                file=f
            )
        if result[coconuts]:
            print(
                checktime,
                coconuts,
                result[coconuts][0].price,
                result[coconuts][0].quantity,          
                profit[coconuts], 
                sep=';',
                file=f
            )
            
        # TEST ALL:
        # print(
        #         checktime,
        #         result,
        #         profit,
        #         file=f
        #     )
        
            
    checktime += 100
    index += 1


print(profit)
# print(order_depths[coconnuts].buy_orders)
# print(order_depths[berrie].buy_orders)
# print(order_depths[diving].buy_orders)
# print(order_depths[pearl].buy_orders)
# print(order_depths[bananas].buy_orders)
# print(order_depths[pina].buy_orders)
