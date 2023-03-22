import json
from typing import Dict, List
from json import JSONEncoder

from typing import Dict, List
# from strategy_test.data_model import OrderDepth, TradingState, Order

import numpy as np


Time = int
Symbol = str
Product = str
Position = int
UserId = str
Observation = int


# Listing class provide trading pairs available
class Listing:
    def __init__(
        self, 
        symbol: Symbol, 
        product: Product, 
        denomination: Product
    ):

        self.symbol = symbol
        self.product = product
        self.denomination = denomination


class Order:
    def __init__(
        self, symbol: Symbol, 
        price: int, 
        quantity: int
    ) -> None:

        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return (
            "(" + self.symbol + 
            ", " + str(self.price) + 
            ", " + str(self.quantity) + ")"
        )

    def __repr__(self) -> str:
        return (
            "(" + self.symbol + 
            ", " + str(self.price) + 
            ", " + str(self.quantity) + ")"
        )

# Orders sent by trading bots
class OrderDepth:
    # TODO: fix back later
    def __init__(
        self, 
        buy_orders: Dict[int, int], 
        sell_orders: Dict[int, int]
    ):
        # key: price, value: quantities
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders


class Trade:
    def __init__(
        self, 
        symbol: Symbol, 
        price: int, 
        quantity: int, 
        buyer: UserId = "", 
        seller: UserId = ""
    ) -> None:

        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller

    def __str__(self) -> str:
        return (
            "(" + self.symbol + 
            ", " + self.buyer + 
            " << " + self.seller + 
            ", " + str(self.price) + 
            ", " + str(self.quantity) + ")"
        )

    def __repr__(self) -> str:
        return (
            "(" + self.symbol + 
            ", " + self.buyer + 
            " << " + self.seller + 
            ", " + str(self.price) + 
            ", " + str(self.quantity) + ")"
        )


class TradingState(object):
    def __init__(
        self,
        timestamp: Time,
        listings: Dict[Symbol, Listing],
        order_depths: Dict[Symbol, OrderDepth],
        own_trades: Dict[Symbol, List[Trade]],
        market_trades: Dict[Symbol, List[Trade]],
        position: Dict[Product, Position],
        observations: Dict[Product, Observation]
    ): 

        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths

        # the trades that the algorithm has done from previous TradingState
        self.own_trades = own_trades

        # the trades that other people has done from previous TradingState
        self.market_trades = market_trades
        self.position = position
        self.observations = observations

    def toJSON(self):
        return json.dumps(
            self, 
            default=lambda o: o.__dict__, 
            sort_keys=True
        )


class ProsperityEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Trader:
    # def estimate_price(self, state: TradingState) -> int:

    pre_trades = {'PEARLS': [],
                  'BANANAS': []}
    pre_ma20s = {'PEARLS': [],
                  'BANANAS': []}
    pre_ma100s = {'PEARLS': [],
                  'BANANAS': []}

    def run(
        self, 
        state: TradingState
    ) -> Dict[str, List[Order]]:

        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []
                pre_trade: Trader.pre_trade[product] = []

                if order_depth.sell_orders:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # BUY conditions
                    if best_ask < 10000:
                        # In case the conditions met,
                        # BUY!
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with "same quantity"
                        # We expect this order to trade with the sell order
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(
                            Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    # SELL conditions
                    if best_bid > 10000:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(
                            Order(product, best_bid, -best_bid_volume))

                result[product] = orders

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':
                """
                The strategy starts here: 

                Enter position when current price cross MA20 (trend is considered)
                """
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Take the market price (mid price)
                if order_depth.buy_orders and order_depth.sell_orders:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_ask = min(order_depth.sell_orders.keys())
                    current_price = np.average([best_ask, best_bid])

                elif order_depth.buy_orders:
                    current_price = best_ask

                elif order_depth.sell_orders:
                    current_price = best_bid

                Trader.pre_trades[product].append(current_price)
                pre_trade = Trader.pre_trades[product] 

                # Calculate moving avg 7 and 20
                if len(pre_trade) > 99:
                    ''' ma_7 = np.average(pre_trade[-7:]) '''
                    ma_20 = ( 
                        0.08 * pre_trade[-1] +
                        0.3 * np.average(pre_trade[-5:-1]) + 
                        0.27 * np.average(pre_trade[-9:-5]) + 
                        0.21 * np.average(pre_trade[-13:-9]) + 
                        0.11 * np.average(pre_trade[-17:-13]) + 
                        0.03 * np.average(pre_trade[-20:-17]) 
                    )
                    Trader.pre_ma20s[product].append(ma_20)
                    pre_ma20 = Trader.pre_ma20s[product]

                    adaptive_ma20 = (
                        1.0 * ma_20 +
                        1.5 * (pre_ma20[-1] - pre_ma20[-2]) +
                        1.0 * (pre_ma20[-1] - pre_ma20[-3]) +
                        0.5 * (pre_ma20[-1] - pre_ma20[-4]) 
                    )

                    ma_100 = np.average(pre_trade[-100:])
                    Trader.pre_ma100s[product].append(ma_100)
                    pre_ma100 = Trader.pre_ma100s[product]
                    
                if len(pre_trade) > 119:
                    i_trend = []
                    # compute the %change in moving avg 100 
                    for i in [1,2,3,5,10,15,20,30]:
                        i_trend.append(
                            (pre_ma100[-1] - pre_ma100[-i - 1]) / pre_ma100[-i - 1]
                        )                    

                # If statement checks if there are any SELL orders in the BANANAS market
                    if order_depth.sell_orders:

                        # Sort all the available sell orders by their price,
                        # and select only the sell order with the lowest price
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]

                        n_decrease = 0
                        for pct_change in i_trend:
                            if pct_change < 0:
                                n_decrease += 1

                        # UPward trend and undefined trend
                        if not n_decrease >= 6:
                            if best_ask < adaptive_ma20:
                                print("BUY", str(-best_ask_volume) + "x", best_ask)
                                orders.append(
                                    Order(product, best_ask, -best_ask_volume))

                        # DOWNward trend                        
                        else:
                            if product in state.position.keys() and state.position[product] < 0:
                                if best_ask < adaptive_ma20:
                                    print("BUY", str(-state.position[product]) + "x", best_ask)
                                    orders.append(
                                        Order(product, best_ask, -state.position[product]))

                    # The below code block is similar to the one above,
                    # the difference is that it find the highest bid (buy order)
                    if order_depth.buy_orders:
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]
                        n_increase = 0
                        for pct_change in i_trend:
                            if pct_change > 0:
                                n_increase += 1

                        # DOWNward trend and undefined
                        if not n_increase >= 6:
                            if best_bid > adaptive_ma20:
                                print("SELL", str(best_bid_volume) + "x", best_bid)
                                orders.append(
                                    Order(product, best_bid, -best_bid_volume))

                        # UPward trend        
                        else:
                            if product in state.position.keys() and state.position[product] > 0:
                                if best_bid > adaptive_ma20:
                                    print("SELL", str(state.position[product]) + "x", best_bid)
                                    orders.append(
                                        Order(product, best_bid, -state.position[product]))
            
                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result
