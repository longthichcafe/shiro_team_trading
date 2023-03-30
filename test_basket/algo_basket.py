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
        'RATIO_DIP':[],
        'BAGUETTE': [],
        'UKULELE': [],
        'PICNIC_BASKET': [],
        'DIFF_PICNIC': [],
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
        'RATIO_DIP':[],
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

        '''
        Strategy for PICNIC
        '''
        for product in state.order_depths.keys():
            if product == 'DIP':
                order_depth: OrderDepth = state.order_depths[product]
                # Take the market price (mid price)            
                pre_trade_dip, current_price_dip = get_pre_trade(
                    product,
                    order_depth
                )

            # Calculate moving avg 20 and 200
            # if len(pre_trade) > 99:
                # ma_20 = np.average(pre_trade[-20:])
                # Trader.pre_ma20s[product].append(ma_20)
                # ma_100 = np.average(pre_trade[-100:])
                # Trader.pre_ma100s[product].append(ma_100)
            # if len(pre_trade) > 199:
            #     ma_200 = np.average(pre_trade[-200:])
            #     Trader.pre_ma200s[product].append(ma_200)

            if product == 'BAGUETTE':
                order_depth: OrderDepth = state.order_depths[product]
                # Take the market price (mid price)            
                pre_trade_baguette, current_price_baguette = get_pre_trade(
                    product,
                    order_depth
                )

            # Calculate moving avg 20 and 200
            # if len(pre_trade) > 99:
                # ma_20 = np.average(pre_trade[-20:])
                # Trader.pre_ma20s[product].append(ma_20)
                # ma_100 = np.average(pre_trade[-100:])
                # Trader.pre_ma100s[product].append(ma_100)
            # if len(pre_trade) > 199:
            #     ma_200 = np.average(pre_trade[-200:])
            #     Trader.pre_ma200s[product].append(ma_200)

            if product == 'UKULELE':
                order_depth: OrderDepth = state.order_depths[product]
                # Take the market price (mid price)            
                pre_trade_ukulele, current_price_ukulele = get_pre_trade(
                    product,
                    order_depth
                )

            # Calculate moving avg 20 and 200
            # if len(pre_trade) > 99:
                # ma_20 = np.average(pre_trade[-20:])
                # Trader.pre_ma20s[product].append(ma_20)
                # ma_100 = np.average(pre_trade[-100:])
                # Trader.pre_ma100s[product].append(ma_100)
            # if len(pre_trade) > 199:
            #     ma_200 = np.average(pre_trade[-200:])
            #     Trader.pre_ma200s[product].append(ma_200)

            if product == 'PICNIC_BASKET':
                order_depth: OrderDepth = state.order_depths[product]
                # Take the market price (mid price)            
                pre_trade_picnic, current_price_picnic = get_pre_trade(
                    product,
                    order_depth
                )

            # Calculate moving avg 20 and 200
            # if len(pre_trade) > 99:
                # ma_20 = np.average(pre_trade[-20:])
                # Trader.pre_ma20s[product].append(ma_20)
                # ma_100 = np.average(pre_trade[-100:])
                # Trader.pre_ma100s[product].append(ma_100)
            # if len(pre_trade) > 199:
            #     ma_200 = np.average(pre_trade[-200:])
            #     Trader.pre_ma200s[product].append(ma_200)

        '''
        PICNIC BASKET
        '''
        
        # GET DIFFERENCE IN PICNIC
        current_sum = (
            4*current_price_dip + 2*current_price_baguette + current_price_ukulele
        )
        current_diff = current_price_picnic - current_sum - 366.9504
        Trader.pre_trades['DIFF_PICNIC'].append(current_diff)
        pre_diff = Trader.pre_trades['DIFF_PICNIC']

        # Calculate moving avg 20 and 200
        if len(pre_diff) > 99:
            ma_100 = np.average(pre_diff[-100:])
            Trader.pre_ma100s['DIFF_PICNIC'].append(ma_100)
            pre_ma100_diff = Trader.pre_ma100s['DIFF_PICNIC']

            if len(pre_ma100_diff) > 70:
                n_increase = 0
                n_decrease = 0
                trend_index_diff = []
                # compute the change in moving avg 200 
                for i in [5,10,15,20,25,30,40,50,60,70]:
                    trend_index_diff.append(
                        pre_ma100_diff[-1] - pre_ma100_diff[-i-1]
                    )
                for pct_change in trend_index_diff:
                    if pct_change < 0:
                        n_decrease += 1
                    if pct_change > 0:
                        n_increase += 1

                product_picnic = 'PICNIC_BASKET'
                product_baguette = 'BAGUETTE'
                product_ukulele = 'UKULELE'

                upperlimit_picnic = Trader.position_limit[product_picnic]
                lowerlimit_picnic = -Trader.position_limit[product_picnic]
                upperlimit_baguette = Trader.position_limit[product_baguette]
                lowerlimit_baguette = -Trader.position_limit[product_baguette] 
                upperlimit_ukulele = Trader.position_limit[product_ukulele]
                lowerlimit_ukulele = -Trader.position_limit[product_ukulele] 

                # SELL Basket, BUY Uku & Bag condition
                if current_diff > 100 and n_increase < 8:
                    # Basket
                    order_depth: OrderDepth = state.order_depths[product_picnic]
                    if order_depth.buy_orders:
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]      
                        remaining_position = limit_calculation(
                            product_picnic,
                            lowerlimit_picnic
                            )
                        result[product_picnic] = sell(
                            product_picnic,
                            best_bid_volume,
                            remaining_position,
                            best_bid
                        )

                    # Baguette
                    order_depth: OrderDepth = state.order_depths[product_baguette]
                    if order_depth.sell_orders:
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        remaining_position = limit_calculation(
                            product_baguette,
                            upperlimit_baguette
                        )
                        # remaining position is > 0
                        result[product_baguette] = buy(
                            product_baguette,
                            best_ask_volume,
                            remaining_position,
                            best_ask
                        )

                    # Ukulele
                    order_depth: OrderDepth = state.order_depths[product_ukulele]
                    if order_depth.sell_orders:
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        remaining_position = limit_calculation(
                            product_ukulele,
                            upperlimit_ukulele
                        )
                        # remaining position is > 0
                        result[product_ukulele] = buy(
                            product_ukulele,
                            best_ask_volume,
                            remaining_position,
                            best_ask
                        )

                # BUY Basket, SELL Uku & Bag condition
                if current_diff < 100 and n_decrease < 8:
                    # Picnic basket
                    order_depth: OrderDepth = state.order_depths[product_picnic]
                    if order_depth.sell_orders:
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        remaining_position = limit_calculation(
                            product_picnic,
                            upperlimit_picnic
                        )
                        # remaining position is > 0
                        result[product_picnic] = buy(
                            product_picnic,
                            best_ask_volume,
                            remaining_position,
                            best_ask
                        )

                    # Baguette
                    order_depth: OrderDepth = state.order_depths[product_baguette]
                    if order_depth.buy_orders:
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]      
                        remaining_position = limit_calculation(
                            product_baguette,
                            lowerlimit_baguette
                            )
                        result[product_baguette] = sell(
                            product_baguette,
                            best_bid_volume,
                            remaining_position,
                            best_bid
                        )

                    # Ukulele
                    order_depth: OrderDepth = state.order_depths[product_ukulele]
                    if order_depth.buy_orders:
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]      
                        remaining_position = limit_calculation(
                            product_ukulele,
                            lowerlimit_ukulele
                            )
                        result[product_ukulele] = sell(
                            product_ukulele,
                            best_bid_volume,
                            remaining_position,
                            best_bid
                        )

        '''
        DIP

        Buy/sell based on average line
        '''
        product = 'DIP'
        
        ratio_dip_mean = 0.3829186
        ratio_dip = (4*current_price_dip / current_price_picnic - ratio_dip_mean)*100

        Trader.pre_trades['RATIO_DIP'].append(ratio_dip)
        pre_ratio_dip = Trader.pre_trades['RATIO_DIP']

        # Calculate moving avg 20 and 200
        if len(pre_ratio_dip) > 99:
            ma_100 = np.average(pre_ratio_dip[-100:])
            Trader.pre_ma100s['RATIO_DIP'].append(ma_100)
            pre_ma100_r_dip = Trader.pre_ma100s['RATIO_DIP']

            if len(pre_ma100_r_dip) > 70:
                n_increase = 0
                n_decrease = 0
                trend_index_r_dip = []
                # compute the change in moving avg 100 
                for i in [5,10,15,20,25,30,40,50,60,70]:
                    trend_index_r_dip.append(
                        pre_ma100_r_dip[-1] - pre_ma100_r_dip[-i-1]
                    )
                for pct_change in trend_index_r_dip:
                    if pct_change < 0:
                        n_decrease += 1
                    if pct_change > 0:
                        n_increase += 1

                upperlimit = Trader.position_limit[product]
                lowerlimit = -Trader.position_limit[product] 
                order_depth: OrderDepth = state.order_depths[product]
                
                # SELL when higher than 0
                if ratio_dip > 0.1 and n_increase < 9:
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
                # BUY when lower than 0
                if ratio_dip < -0.1 and n_decrease < 9:
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
        return result
