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
    rand_price_bid = random.randint(10, 20)
    rand_quantity_bid = random.randint(0, 20)
    rand_price_ask = rand_price_bid + random.randint(1, 2)
    rand_quantity_ask = random.randint(-20, 0)
    order_depths = {
        "PEARLS": OrderDepth(
            buy_orders={rand_price_bid: rand_quantity_bid,
                        rand_price_bid - 1: rand_quantity_bid},
            sell_orders={rand_price_ask: rand_quantity_ask,
                         rand_price_ask + 1: rand_quantity_ask}
        )
    }

    print(checktime, trader.run(state=TradingState(
        timestamp=timestamp,
        listings=listings,
        order_depths=order_depths,
        own_trades=own_trades,
        market_trades=market_trades,
        position=position,
        observations=observations
    )))

    checktime += 1
