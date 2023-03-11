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
    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination


class Order:
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"


# Orders sent by trading bots
class OrderDepth:
    # TODO: fix back later
    def __init__(self, buy_orders: Dict[int, int], sell_orders: Dict[int, int]):
        # key: price, value: quantities
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}


class Trade:
    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = "", seller: UserId = "") -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"


class TradingState(object):
    def __init__(self,
                 timestamp: Time,
                 listings: Dict[Symbol, Listing],
                 order_depths: Dict[Symbol, OrderDepth],
                 own_trades: Dict[Symbol, List[Trade]],
                 market_trades: Dict[Symbol, List[Trade]],
                 position: Dict[Product, Position],
                 observations: Dict[Product, Observation]):
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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


class ProsperityEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Trader:
    # def estimate_price(self, state: TradingState) -> int:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Initialize the list of previous trade and Moving Avg 7 and 20
        pre_trade = []  # keep track of previous trade to calculate ma7 - ma20
        ma_7 = 0
        ma_20 = 0
        ma_7_pre = 0
        ma_20_pre = 0
        bystate = 0

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                """
                The strategy starts here: 

                Enter position when MA7 cross MA20 (happen within 5 states)
                """
                # Take the market price (mid price)
                current_price = 0
                if order_depth.buy_orders and order_depth.sell_orders:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_ask = min(order_depth.sell_orders.keys())
                    current_price = np.average([best_ask, best_bid])

                elif order_depth.buy_orders:
                    current_price = min(order_depth.buy_orders.keys())

                elif order_depth.sell_orders:
                    current_price = min(order_depth.sell_orders.keys())

                pre_trade.append(current_price)

                # Calculate moving avg 7 and 20
                if len(pre_trade) > 19:
                    ma_7 = np.average(pre_trade[-7:])
                    ma_20 = np.average(pre_trade[-20:])

                    # bystate marks the number of states after the cross happened
                    if abs((ma_7_pre - ma_20_pre) - (ma_7 - ma_20)) < (abs(ma_7_pre - ma_20_pre) + abs(ma_7 - ma_20)):
                        bystate = 1

                    else:
                        bystate += 1

                    ma_7_pre = ma_7
                    ma_20_pre = ma_20

                # Note that this value of 1 is just a dummy value, you should likely change it!
                # acceptable_price = 1

                # If statement checks if there are any SELL orders in the PEARLS market
                if order_depth.sell_orders:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # BUY conditions
                    """
                    if ma_7 > ma_20 and current_price > ma_20 and bystate <= 5:
                    """
                    if len(pre_trade) > 19:

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
                    if ma_7 < ma_20 and current_price < ma_20 and bystate <= 5:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(
                            Order(product, best_bid, -best_bid_volume))

                # Execute any holding POSITIONS

                # LONG position
                if product in state.position.keys() and state.position[product] > 0:
                    pct_change_1 = (
                        pre_trade[-1] - pre_trade[-2]) / pre_trade[-2]
                    pct_change_2 = (
                        pre_trade[-2] - pre_trade[-3]) / pre_trade[-3]

                    # Condition to close position (SELL)
                    if pct_change_1 < 0 and pct_change_2 < 0:

                        # Looking for buy orders
                        if len(order_depth.buy_orders) != 0:

                            sorted_bid = sorted(
                                order_depth.buy_orders.keys(), reverse=True)

                            best_bid = sorted_bid[0]
                            best_bid_volume = order_depth.buy_orders[best_bid]

                            if len(order_depth.buy_orders) > 1:
                                best_bid_2 = sorted_bid[1]
                                best_bid_volume_2 = order_depth.buy_orders[best_bid_2]

                            print("BUY", str(
                                state.position[product]) + "x", best_bid)
                            orders.append(
                                Order(product, best_bid, -
                                      state.position[product])
                            )

                            # If position not fully executed
                            if state.position[product] > best_bid_volume:

                                # position remaining volumn
                                position_r_vol = state.position[product] - \
                                    best_bid_volume

                                # Check if the 2nd bid could meet all remaining volumn
                                if position_r_vol > best_bid_volume_2:
                                    print("BUY", str(
                                        best_bid_volume_2) + "x", best_bid_2)
                                    orders.append(
                                        Order(product, best_bid_2, -
                                              best_bid_volume_2)
                                    )

                                else:
                                    print("BUY", str(position_r_vol) +
                                          "x", best_bid_2)
                                    orders.append(
                                        Order(product, best_bid_2, -
                                              position_r_vol)
                                    )

                # SHORT position
                if product in state.position.keys() and state.position[product] < 0:
                    pct_change_1 = (
                        pre_trade[-1] - pre_trade[-2]) / pre_trade[-2]
                    pct_change_2 = (
                        pre_trade[-2] - pre_trade[-3]) / pre_trade[-3]

                    # Condition to close position
                    if pct_change_1 > 0 and pct_change_2 > 0:

                        # Looking for sell orders
                        if len(order_depth.sell_orders) != 0:

                            sorted_ask = sorted(
                                order_depth.sell_orders.keys(), reverse=False)

                            best_ask = sorted_ask[0]
                            best_ask_volume = order_depth.sell_orders[best_ask]

                            if len(order_depth.sell_orders) > 1:
                                best_ask_2 = sorted_ask[1]
                                best_ask_volume_2 = order_depth.sell_orders[best_ask_2]

                            print(
                                "BUY", str(-state.position[product]) + "x", best_ask)
                            orders.append(
                                Order(product, best_ask, -
                                      state.position[product])
                            )

                            # If position not fully executed
                            if abs(state.position[product]) > abs(best_ask_volume):

                                # position remaining volumn
                                # negative value
                                position_r_vol = state.position[product] - \
                                    best_ask_volume

                                # Check if the 2nd ask could meet all remaining volumn
                                if abs(position_r_vol) > abs(best_ask_volume_2):        # not met all
                                    print(
                                        "BUY", str(-best_ask_volume_2) + "x", best_ask_2)
                                    orders.append(
                                        Order(product, best_ask_2, -
                                              best_ask_volume_2)
                                    )

                                else:    # met all
                                    print("BUY", str(-position_r_vol) +
                                          "x", best_ask_2)
                                    orders.append(
                                        Order(product, best_ask_2, -
                                              position_r_vol)
                                    )

                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result
