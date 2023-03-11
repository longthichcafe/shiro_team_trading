from algo_test import *
import random

timestamp = 0

listings = {
    "PEARLS": Listing(
        symbol="PEARLS",
        product="PEARLS",
        denomination="SEASHELLS"
    ),

    # "PRODUCT2": Listing(
    #     symbol="PRODUCT2",
    #     product="PRODUCT2",
    #     denomination="SEASHELLS"
    # ),
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
    "PRODUCT1": 3,
    "PRODUCT2": -5
}

observations = {}


# ===============================  MAIN ===============================
# ===============================  MAIN ===============================
# ===============================  MAIN ===============================

checktime = 0

trader = Trader()
while checktime <= 100:
    rand_price = random.randint(-20, 20)
    rand_quantity = random.randint(0, 20)
    order_depths = {
        "PEARLS": OrderDepth(
            buy_orders={rand_quantity: rand_price, rand_quantity: rand_price},
            sell_orders={rand_quantity: rand_price, rand_quantity: rand_price}
        )
    }
    print(trader.run(state=TradingState(
        timestamp=timestamp,
        listings=listings,
        order_depths=order_depths,
        own_trades=own_trades,
        market_trades=market_trades,
        position=position,
        observations=observations
    )))

    checktime += 1
