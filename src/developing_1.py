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
        'DIVING_GEAR': []
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
        'DOLPHIN_SIGHTINGS': []
    }
    pre_ma100s = {
        'PEARLS': [],
        'BANANAS': [],
        'COCONUTS': [],
        'PINA_COLADAS': [],
        'BERRIES': [],
        'DIVING_GEAR': [],
        'DOLPHIN_SIGHTINGS': []
    }
    pre_ma200s = {
        'COCONUTS': [],
        'PINA_COLADAS': [],
        'BERRIES': [],
        'DIVING_GEAR': [],
        'DOLPHIN_SIGHTINGS': []
    }
    position_limit = {
        'PEARLS': 20,
        'BANANAS': 20,
        'COCONUTS': 600,
        'PINA_COLADAS': 300,
        'BERRIES': 250,
        'DIVING_GEAR': 50
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
            'DIVING_GEAR': []
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
                print(
                    "BUY", str(remaining_position) + "x", best_ask
                )
                orders.append(
                    Order(product, best_ask, remaining_position)
                )
            else:
                print(
                    "BUY", str(-best_ask_volume) + "x", best_ask
                )
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
                print(
                    "SELL", str(-remaining_position) + "x", best_bid
                )
                orders.append(
                    Order(product, best_bid, remaining_position)
                )
            else:
                print(
                    "SELL", str(best_bid_volume) + "x", best_bid
                )
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
            if product == 'PEARLS':
                """
                The strategy for PEARLS starts here: 

                Enter position when current price cross 10000
                """
                order_depth: OrderDepth = state.order_depths[product]
                upperlimit = Trader.position_limit[product]
                lowerlimit = -Trader.position_limit[product]

                if order_depth.sell_orders:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    # BUY conditions
                    if best_ask < 10000:
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

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    # SELL conditions
                    if best_bid > 10000:
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
            
            if product == 'BANANAS':
                """
                The strategy for BANANAS starts here: 
                Enter position when current price cross MA20 (long trend is not considered)
                """
                order_depth: OrderDepth = state.order_depths[product]
                pre_trade, current_price = get_pre_trade(
                    product,
                    order_depth
                )
                upperlimit = Trader.position_limit[product]
                lowerlimit = -Trader.position_limit[product]                

                if len(pre_trade) > 19:
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
                    """ma_100 = np.average(pre_trade[-100:])
                    Trader.pre_ma100s[product].append(ma_100)
                    pre_ma100 = Trader.pre_ma100s[product]"""
                # if len(pre_trade) > 129:
                if len(pre_trade) > 24:
                    adaptive_ma20 = (
                            1.0 * ma_20 +
                            1.5 * (pre_ma20[-1] - pre_ma20[-2]) +
                            1.0 * (pre_ma20[-1] - pre_ma20[-3]) +
                            0.5 * (pre_ma20[-1] - pre_ma20[-4]) 
                    )
                    """i_trend = []
                    # compute the %change in moving avg 100 
                    for i in [1,2,3,5,10,15,20,30]:
                        i_trend.append(
                            (pre_ma100[-1] - pre_ma100[-i - 1]) / pre_ma100[-i - 1]
                        )     """               
                    if order_depth.sell_orders:
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        if best_ask < adaptive_ma20:
                            remaining_position = limit_calculation(
                                product,
                                upperlimit
                            )
                            # remaining position is > 0
                            result[product] = buy(
                                product,
                                best_ask_volume,
                                remaining_position,
                                best_ask
                            )
                    if order_depth.buy_orders:
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]
                        if best_bid > adaptive_ma20:       
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

            if product == 'BERRIES':
                """
                The strategy for BERRIES starts here: 
                Enter position based on MA100 (favor Long before 450000, favor Short after 550000)
                """
                order_depth: OrderDepth = state.order_depths[product]
                pre_trade, current_price = get_pre_trade(
                    product,
                    order_depth
                )
                if len(pre_trade) > 99:
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
                    ma_100 = np.average(pre_trade[-100:])
                    Trader.pre_ma100s[product].append(ma_100)
                    pre_ma100 = Trader.pre_ma100s[product]
                """if len(pre_trade) > 199:                   
                    ma_200 = np.average(pre_trade[-200:])
                    Trader.pre_ma200s[product].append(ma_200)
                    pre_ma200 = Trader.pre_ma200s[product]
                if len(pre_trade) > 299:"""
                if len(pre_trade) > 149:
                    adaptive_ma20 = (
                            1.0 * ma_20 +
                            1.5 * (pre_ma20[-1] - pre_ma20[-2]) +
                            1.0 * (pre_ma20[-1] - pre_ma20[-3]) +
                            0.5 * (pre_ma20[-1] - pre_ma20[-4]) 
                    )
                    trend_index = []
                    # compute the %change in moving avg 100 
                    for i in [1,2,3,5,10,15,20,30,40,50]:
                        trend_index.append(
                            (pre_ma100[-1] - pre_ma100[-i - 1]) / pre_ma100[-i - 1]
                        )
                    """trend_index = []
                    # compute the %change in moving avg 200 
                    for i in [10,20,30,40,50,60,70,80,90,100]:
                        trend_index.append(
                            (pre_ma200[-1] - pre_ma200[-i - 1]) / pre_ma200[-i - 1]
                        )"""
                    # initialise variables to identify trend
                    bullish_index = 8
                    bearish_index = 8
                    n_increase = 0
                    n_decrease = 0

                    for pct_change in trend_index:
                        if pct_change < 0:
                            n_decrease += 1
                        if pct_change > 0:
                            n_increase += 1
                    if state.timestamp in range(200000, 450001):
                        # favor Long
                        bullish_index = 7            
                        if state.timestamp in range(400000, 450001):
                            # higher restriction for Short
                            bearish_index = 9
                    elif state.timestamp in range(550000, 800001):
                        # favor Short
                        bearish_index = 7
                        if state.timestamp in range(550000, 600001):
                            # higher restriction for Long
                            bullish_index = 9 
                    if order_depth.sell_orders:
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        # UPward trend
                        if n_increase >= bullish_index and np.sum(trend_index) > 0.0002:
                            remaining_position = limit_calculation(
                                product,
                                upperlimit
                            )
                            # remaining position is > 0
                            result[product] = buy(
                                product,
                                best_ask_volume,
                                remaining_position,
                                best_ask
                            )
                        """# Close any Short position
                        if product in state.position.keys() and state.position[product] < 0:
                            # The Down trend is reversing
                            if np.sum(trend_index[0:8]) - np.sum(trend_index[8:]) > 0:
                                print(
                                    "BUY", str(-state.position[product]) + "x", best_ask)
                                orders.append(
                                    Order(product, best_ask, -state.position[product]))"""
                    if order_depth.buy_orders:
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]
                        # DOWNward trend and undefined
                        if n_decrease >= bearish_index and np.sum(trend_index) > 0.0002:
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

                    """# Close any Long position
                    if product in state.position.keys() and state.position[product] > 0:
                        # The Up trend is reversing
                        if np.sum(trend_index[0:8]) - np.sum(trend_index[8:]) < 0:
                            print("SELL", str(
                                state.position[product]) + "x", best_bid)
                            orders.append(
                                Order(product, best_bid, -state.position[product]))"""

            if product == 'DIVING_GEAR':
                order_depth: OrderDepth = state.order_depths[product]
                pre_trade, current_price = get_pre_trade(
                    product,
                    order_depth
                )
                # rescale the price
                mean = 100000
                sd = 400.8272
                current_price = (current_price - mean) / sd
                Trader.pre_trades[product].append(current_price)
                pre_trade = Trader.pre_trades[product]
                """Calculate moving avg 20 and 200
                if len(pre_trade) > 99:
                    ma_20 = np.average(pre_trade[-20:])
                    Trader.pre_ma20s[product].append(ma_20)

                    ma_100 = np.average(pre_trade[-100:])
                    Trader.pre_ma100s[product].append(ma_100)"""
                if len(pre_trade) > 199:
                    ma_200 = np.average(pre_trade[-200:])
                    Trader.pre_ma200s[product].append(ma_200)

            if product == 'COCONUTS':
                order_depth: OrderDepth = state.order_depths[product]
                pre_trade, current_price = get_pre_trade(
                    product,
                    order_depth
                )
                # rescale the price
                mean = 8000
                sd = 44.08487
                current_price = (current_price - mean) / sd
                Trader.pre_trades[product].append(current_price)
                pre_trade = Trader.pre_trades[product]              
                # Calculate moving avg 20 and 200
                if len(pre_trade) > 199:
                    ma_20 = np.average(pre_trade[-20:])
                    Trader.pre_ma20s[product].append(ma_20)
                    ma_200 = np.average(pre_trade[-200:])
                    Trader.pre_ma200s[product].append(ma_200)
         
            if product == 'PINA_COLADAS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]
                # Take the market price (mid price)
                pre_trade, current_price = get_pre_trade(
                    product,
                    order_depth
                )
                # rescale the price
                mean = 15000
                sd = 84.45238
                current_price = (current_price - mean)/sd
                Trader.pre_trades[product].append(current_price)
                pre_trade = Trader.pre_trades[product]             
                # Calculate moving avg 200
                if len(pre_trade) > 199:                    
                    ma_20 = np.average(pre_trade[-20:])
                    Trader.pre_ma20s[product].append(ma_20)

                    ma_200 = np.average(pre_trade[-200:])
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
        if len(pre_ma200_coco) > 100:
            i_trend = []
            # compute the %change in moving avg 200 
            for i in [10,20,30,40,50,60,70,80,90,100]:
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
                if n_increase > 7:
                    if pre_ma20_coco[-1] > pre_ma20_pina[-1]:
                        product = 'PINA_COLADAS'
                    else:
                        product = 'COCONUTS'
                    order_depth: OrderDepth = state.order_depths[product]

                    if order_depth.sell_orders:
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        remaining_position = limit_calculation(
                            product,
                            upperlimit
                        )
                        # remaining position is > 0
                        result[product] = buy(
                            product,
                            best_ask_volume,
                            remaining_position,
                            best_ask
                        )
                    
                # DOWNward trend
                elif n_decrease > 7:
                    if pre_ma20_coco[-1] < pre_ma20_pina[-1]:
                        product = 'PINA_COLADAS'
                    else:
                        product = 'COCONUTS'
                    upperlimit = Trader.position_limit[product]
                    lowerlimit = -Trader.position_limit[product]
                    order_depth: OrderDepth = state.order_depths[product]

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
            for product in ['COCONUTS', 'PINA_COLADAS']:
                upperlimit = Trader.position_limit[product]
                lowerlimit = -Trader.position_limit[product]
                order_depth: OrderDepth = state.order_depths[product]

                if product in state.position.keys() and state.position[product] != 0:
                    if abs(pre_ma20_coco[-1] - pre_ma20_pina[-1]) < 0.05:
                        if state.position[product] > 0:
                            best_bid = max(order_depth.buy_orders.keys())
                            best_bid_volume = order_depth.buy_orders[best_bid]

                            print("SELL", str(state.position[product]) + "x", best_bid)
                            orders: list[Order] = []  
                            orders.append(
                                Order(product, best_bid, -state.position[product]))
                        else:
                            best_ask = min(order_depth.sell_orders.keys())
                            best_ask_volume = order_depth.sell_orders[best_ask]

                            print("BUY", str(-state.position[product]) + "x", best_ask)
                            orders: list[Order] = []
                            orders.append(
                                Order(product, best_ask, -state.position[product]))
                        result[product] = orders
        '''
        Strategy for DIVING_GEAR starts here
        Long/Short immediately if Dolphins number increase/decrease
        Close positions when ma100 (ma200) show weaker trend
        '''
        for observe in state.observations.keys():
            if observe == 'DOLPHIN_SIGHTINGS':
                current_obs = state.observations[observe]
                mean = 3000
                sd = 29.60632
                current_obs = (current_obs - mean)/sd
                Trader.pre_observes[observe].append(current_obs)
                pre_observe = Trader.pre_observes[observe]
                """Calculate moving avg
                if len(pre_observe) > 99:
                    ma_20 = np.average(pre_observe[-20:])
                    Trader.pre_ma20s[observe].append(ma_20)

                    ma_100 = np.average(pre_observe[-100:])
                    Trader.pre_ma100s[observe].append(ma_100)"""
                if len(pre_observe) > 199:
                    ma_200 = np.average(pre_observe[-200:])
                    Trader.pre_ma200s[observe].append(ma_200)
        
        # pre_ma20_gear = Trader.pre_ma20s['DIVING_GEAR']
        # pre_ma100_gear = Trader.pre_ma100s['DIVING_GEAR']
        pre_ma200_gear = Trader.pre_ma200s['DIVING_GEAR']
        
        # pre_ma20_dolphin = Trader.pre_ma20s['DOLPHIN_SIGHTINGS']
        # pre_ma100_dolphin = Trader.pre_ma100s['DOLPHIN_SIGHTINGS']
        pre_ma200_dolphin = Trader.pre_ma200s['DOLPHIN_SIGHTINGS']
        
        product = 'DIVING_GEAR'

        upperlimit = Trader.position_limit[product]
        lowerlimit = -Trader.position_limit[product]
        if len(pre_ma200_dolphin) > 100:
            trend_index_dophin = []
            # compute the change in moving avg 200 
            for i in [50,100]:
                trend_index_dophin.append(
                    pre_ma200_dolphin[-1] - pre_ma200_dolphin[-i-1]
                )
            n_increase = 0
            n_decrease = 0
            trend_index_gear = []
            # compute the change in moving avg 200 
            for i in [10,20,30,40,50,60,70,80,90,100]:
                trend_index_gear.append(
                    pre_ma200_gear[-1] - pre_ma200_gear[-i-1]
                )
            for pct_change in i_trend:
                if pct_change < 0:
                    n_decrease += 1
                if pct_change > 0:
                    n_increase += 1
            order_depth: OrderDepth = state.order_depths[product]
            orders: list[Order] = []
            if order_depth.buy_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
            if order_depth.sell_orders:
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
            # === Check dolphins ===
            # Increase in dolphins
            if np.average(trend_index_dophin) > 0.35:
                # BUY               
                remaining_position = limit_calculation(
                    product,
                    upperlimit
                )
                # remaining position is > 0
                result[product] = buy(
                    product,
                    best_ask_volume,
                    remaining_position,
                    best_ask
                )
            # Decrease in dolphins
            elif np.average(trend_index_dophin) < 0.35:
                # SELL               
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
            # CLOSE positions for DIVING_GEAR
            elif product in state.position.keys() and state.position[product] != 0:
                # Close LONG
                if state.position[product] > 0:
                    # when uptrend weaken
                    if not n_increase >= 6:
                        print(
                            "SELL", str(state.position[product]) + "x", best_bid
                        )
                        orders.append(
                            Order(product, best_bid, -state.position[product])
                        )                       
                # Close SHORT
                elif state.position[product] < 0:
                    # when downtrend weaken
                    if not n_decrease >= 6:
                        print(
                            "BUY", str(-state.position[product]) + "x", best_ask
                        )
                        orders.append(
                            Order(product, best_ask, -state.position[product])
                        )
            result[product] = orders
        return result