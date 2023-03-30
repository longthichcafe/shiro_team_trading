import json
import numpy as np

from typing import Dict, List
from json import JSONEncoder
from typing import Dict, List


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

        # the trades that the algorithm has done 
        # from previous TradingState
        self.own_trades = own_trades

        # the trades that other people has done 
        # from previous TradingState
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

    pre_trades = {
        'PEARLS': [],
        'BANANAS': [],
        'COCONUTS': [],
        'PINA_COLADAS': [],
        'BERRIES': [],
        'DIVING_GEAR': [],
        'DIP': [],
        'BAGUETTE': [],
        'UKULELE': [],
        'PICNIC_BASKET': [],
        'DIFF_PICNIC': []
    }
    pre_observes = {
        'DOLPHIN_SIGHTINGS': []
    }
    pre_ma20s = {
        'PEARLS': [],
        'BANANAS': [],
        'COCONUTS': [],
        'PINA_COLADAS': [],
        'BERRIES': [],
        'DIVING_GEAR': [],
        'DOLPHIN_SIGHTINGS': [],
        'DIP': [],
        'BAGUETTE': [],
        'UKULELE': [],
        'PICNIC_BASKET': [],
        'DIFF_PICNIC': []
    }
    pre_ma100s = {
        'PEARLS': [],
        'BANANAS': [],
        'COCONUTS': [],
        'PINA_COLADAS': [],
        'BERRIES': [],
        'DIVING_GEAR': [],
        'DOLPHIN_SIGHTINGS': [],
        'DIP': [],
        'BAGUETTE': [],
        'UKULELE': [],
        'PICNIC_BASKET': [],
        'DIFF_PICNIC': []
    }
    pre_ma200s = {
        'COCONUTS': [],
        'PINA_COLADAS': [],
        'BERRIES': [],
        'DIVING_GEAR': [],
        'DOLPHIN_SIGHTINGS': [],
        'DIP': [],
        'BAGUETTE': [],
        'UKULELE': [],
        'PICNIC_BASKET': [],
        'DIFF_PICNIC': []
    }
    position_limit = {
        'PEARLS': 20,
        'BANANAS': 20,
        'COCONUTS': 600,
        'PINA_COLADAS': 300,
        'BERRIES': 250,
        'DIVING_GEAR': 50,
        'DIP': 300,
        'BAGUETTE': 150,
        'UKULELE': 70,
        'PICNIC_BASKET': 70
    }

    def run(
        self, 
        state: TradingState
    ) -> Dict[str, List[Order]]:

        """
        Only method required. It takes all buy and 
        sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {
            'PEARLS': [],
            'BANANAS': [],
            'COCONUTS': [],
            'PINA_COLADAS': [],
            'BERRIES': [],
            'DIVING_GEAR': [],
            'DIP': [],
            'BAGUETTE': [],
            'UKULELE': [],
            'PICNIC_BASKET': []
        }

        # Iterate over all the keys (the available products) 
        # contained in the order dephts
        def buy(
            product,
            best_ask_volume,
            remaining_position,
            best_ask
        ) -> list: 
            """
            Buy function
            """
            orders: list[Order] = []

            if (-best_ask_volume) > remaining_position:
                # print(
                #     "BUY", str(remaining_position) + "x", best_ask
                # )
                orders.append(
                    Order(product, best_ask, remaining_position)
                )
            else:
                # print(
                #     "BUY", str(-best_ask_volume) + "x", best_ask
                # )
                orders.append(
                    Order(product, best_ask, -best_ask_volume)
                )
            return orders

        def sell(
            product,
            best_bid_volume,
            remaining_position,
            best_bid
        ) -> list:
            """
            Sell function
            """
            orders: list[Order] = []

            if best_bid_volume > (-remaining_position):
                # print(
                #     "SELL", str(-remaining_position) + "x", best_bid
                # )
                orders.append(
                    Order(product, best_bid, remaining_position)
                )
            else:
                # print(
                #     "SELL", str(best_bid_volume) + "x", best_bid
                # )
                orders.append(
                    Order(product, best_bid, -best_bid_volume)
                )
            return orders

        def get_pre_trade(
            product,
            order_depth
        ):
            if order_depth.buy_orders and order_depth.sell_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_ask = min(order_depth.sell_orders.keys())
                current_price = np.average([best_ask, best_bid])
            elif order_depth.buy_orders:
                current_price = best_ask
            elif order_depth.sell_orders:
                current_price = best_bid

            Trader.pre_trades[product].append(current_price)
            return Trader.pre_trades[product], current_price

        def limit_calculation(
            product,
            limit
        ) -> int:
            """
            Calculate limit
            """
            if product in state.position.keys() and state.position[product] != 0:  
                remaining_position = limit - state.position[product]
            else: 
                remaining_position = limit
            
            return remaining_position

        for product in state.order_depths.keys():
            """
            Start trading
            """
            if product == 'COCONUTS':
                order_depth: OrderDepth = state.order_depths[product]
                
                # Take the market price (mid price)
                if order_depth.buy_orders and order_depth.sell_orders:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_ask = min(order_depth.sell_orders.keys())
                    current_price = np.average([best_ask, best_bid])

                elif order_depth.buy_orders:
                    current_price = best_ask

                elif order_depth.sell_orders:
                    current_price = best_bid
                # rescale the price
                # rescale the price
                mean = 8000
                sd = 44.08487
                current_price = (current_price - mean) / sd
                Trader.pre_trades[product].append(current_price)
                pre_trade = Trader.pre_trades[product]              
                # Calculate moving avg 20 and 200
                if len(pre_trade) > 299:
                    ma_20 = np.average(pre_trade[-20:])
                    Trader.pre_ma20s[product].append(ma_20)
                    ma_200 = np.average(pre_trade[-300:])
                    Trader.pre_ma200s[product].append(ma_200)
         
            if product == 'PINA_COLADAS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]
                # Take the market price (mid price)
                if order_depth.buy_orders and order_depth.sell_orders:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_ask = min(order_depth.sell_orders.keys())
                    current_price = np.average([best_ask, best_bid])

                elif order_depth.buy_orders:
                    current_price = best_ask

                elif order_depth.sell_orders:
                    current_price = best_bid
                # rescale the price
                mean = 15000
                sd = 84.45238
                current_price = (current_price - mean)/sd
                Trader.pre_trades[product].append(current_price)
                pre_trade = Trader.pre_trades[product]             
                # Calculate moving avg 200
                if len(pre_trade) > 299:                    
                    ma_20 = np.average(pre_trade[-20:])
                    Trader.pre_ma20s[product].append(ma_20)

                    ma_200 = np.average(pre_trade[-300:])
                    Trader.pre_ma200s[product].append(ma_200)
        """
        The strategy for COCONUTS and PINA_COLADAS starts here: 

        Pairs trading:
        - Rescale
        - Long/Short on widened Gap with trend identified
        - Close positions when Gap narrows

        """
        pre_ma200_coco = Trader.pre_ma200s['COCONUTS']
        pre_ma200_pina = Trader.pre_ma200s['PINA_COLADAS']

        pre_ma20_coco = Trader.pre_ma20s['COCONUTS']
        pre_ma20_pina = Trader.pre_ma20s['PINA_COLADAS']

        # Identify trend
        """if len(pre_ma200_coco) > 200:
            i_trend = []
            # compute the change in moving avg 200 
            for i in [20,40,60,80,100,120,140,160,180,200]:"""
        if len(pre_ma200_coco) > 300:
            i_trend = []
            # compute the change in moving avg 200 
            for i in [30,60,90,120,150,180,210,240,270,300]:
                i_trend.append(
                    (np.average([pre_ma200_coco[-1],pre_ma200_pina[-1]]) 
                     - np.average([pre_ma200_coco[-i-1],pre_ma200_pina[-i-1]]))
                )
            n_increase = 0
            n_decrease = 0

            for pct_change in i_trend:
                if pct_change < 0:
                    n_decrease += 1
                if pct_change > 0:
                    n_increase += 1

            # --- STRATEGY ---
            # Identify GAP
            if abs(pre_ma20_coco[-1] - pre_ma20_pina[-1]) > 0.3:
                # UPward trend
                if n_increase > 6:
                    if pre_ma20_coco[-1] > pre_ma20_pina[-1]:
                        product = 'PINA_COLADAS'
                        order_depth: OrderDepth = state.order_depths[product]
                        upperlimit = Trader.position_limit[product]
                        lowerlimit = -Trader.position_limit[product]                    

                        if order_depth.sell_orders:
                            best_ask = min(order_depth.sell_orders.keys())
                            best_ask_volume = order_depth.sell_orders[best_ask]
                            remaining_position = limit_calculation(
                                product,
                                upperlimit
                            )
                            result[product] = buy(
                                product,
                                best_ask_volume,
                                remaining_position,
                                best_ask
                            )
                    
                # DOWNward trend
                elif n_decrease > 6:
                    if pre_ma20_coco[-1] < pre_ma20_pina[-1]:
                        product = 'PINA_COLADAS'
                        order_depth: OrderDepth = state.order_depths[product]
                        upperlimit = Trader.position_limit[product]
                        lowerlimit = -Trader.position_limit[product]

                        if order_depth.buy_orders:
                            best_bid = max(order_depth.buy_orders.keys())
                            best_bid_volume = order_depth.buy_orders[best_bid]
                            remaining_position = limit_calculation(
                                product,
                                lowerlimit
                                )
                            result[product] = sell(
                                product,
                                best_bid_volume,
                                remaining_position,
                                best_bid
                            )

            # CLOSE positions
            
            for product in ['PINA_COLADAS']:
                upperlimit = Trader.position_limit[product]
                lowerlimit = -Trader.position_limit[product]
                order_depth: OrderDepth = state.order_depths[product]
                if product in state.position.keys() and state.position[product] != 0:
                    if abs(pre_ma20_coco[-1] - pre_ma20_pina[-1]) < 0.01:
                        if state.position[product] > 0:
                            best_bid = max(order_depth.buy_orders.keys())
                            best_bid_volume = order_depth.buy_orders[best_bid]
                            # print("SELL", str(state.position[product]) + "x", best_bid)
                            orders: list[Order] = []  
                            orders.append(
                                Order(product, best_bid, -state.position[product]))
                        else:
                            best_ask = min(order_depth.sell_orders.keys())
                            best_ask_volume = order_depth.sell_orders[best_ask]
                            # print("BUY", str(-state.position[product]) + "x", best_ask)
                            orders: list[Order] = []
                            orders.append(
                                Order(product, best_ask, -state.position[product]))
                        result[product] = orders

        return result
