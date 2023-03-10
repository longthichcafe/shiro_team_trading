from typing import Dict, List
from data_model import OrderDepth, TradingState, Order

import numpy as np


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
        pre_trade = []
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
                # Take the market price
                current_price = state.market_trades[product][len(product)-1].price

                pre_trade.append(current_price)

                # Calculate moving avg 7 and 20
                if len(pre_trade) > 19:
                    ma_7 = np.average(pre_trade[-7:])
                    ma_20 = np.average(pre_trade[-20:])

                    # bystate marks the number of states after the cross happened 
                    if abs((ma_7_pre - ma_20_pre) - (ma_7 - ma_20)) < abs(ma_7_pre - ma_20_pre) + abs(ma_7 - ma_20):
                        bystate = 1

                    else:
                        bystate += 1

                    ma_7_pre = ma_7
                    ma_20_pre = ma_20


                    
                # Note that this value of 1 is just a dummy value, you should likely change it!
                # acceptable_price = 1

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # BUY conditions
                    if ma_7 > ma_20 and current_price > ma_20 and bystate in range(1,6):

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
                    if ma_7 < ma_20 and current_price < ma_20 and bystate in range(1,6):
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(
                            Order(product, best_bid, -best_bid_volume))
                        


                ###    Execute any holding POSITIONS

                pct_change_1 = pre_trade[-2:]
                pct_change_2 = pre_trade[-3:-1]
                
                ## LONG position
                if state.position[product] > 0:

                    # Condition to close position (SELL)
                    if pct_change_1 < 0 and pct_change_2 < 0:

                    # Looking for buy orders
                        if len(order_depth.buy_orders) != 0:

                            sorted_bid = sorted(order_depth.buy_orders.keys(), reverse=True)

                            best_bid = sorted_bid[0]
                            best_bid_volume = order_depth.buy_orders[best_bid]
                        
                            if len(order_depth.buy_orders) > 1:
                                best_bid_2 = sorted_bid[1]
                                best_bid_volume_2 = order_depth.buy_orders[best_bid_2]                        
                        
                            print("BUY", str(state.position[product]) + "x", best_bid)
                            orders.append(
                                Order(product, best_bid, -state.position[product])
                            )

                            
                            # If position not fully executed
                            if state.position[product] > best_bid_volume:
                                
                                # position remaining volumn
                                position_r_vol = state.position[product] - best_bid_volume

                                # Check if the 2nd bid could meet all remaining volumn
                                if position_r_vol > best_bid_volume_2:
                                    print("BUY", str(best_bid_volume_2) + "x", best_bid_2)
                                    orders.append(
                                        Order(product, best_bid_2, -best_bid_volume_2)
                                    )
                                
                                else:
                                    print("BUY", str(position_r_vol) + "x", best_bid_2)
                                    orders.append(
                                        Order(product, best_bid_2, -position_r_vol)
                                    )

            

                ## SHORT position
                if state.position[product] < 0:

                    # Condition to close position
                    if pct_change_1 > 0 and pct_change_2 > 0:

                    # Looking for sell orders
                        if len(order_depth.sell_orders) != 0:

                            sorted_ask = sorted(order_depth.sell_orders.keys(), reverse=False)

                            best_ask = sorted_ask[0]
                            best_ask_volume = order_depth.sell_orders[best_ask]
                        
                            if len(order_depth.sell_orders) > 1:
                                best_ask_2 = sorted_ask[1]
                                best_ask_volume_2 = order_depth.sell_orders[best_ask_2]                        
                        
                            print("BUY", str(-state.position[product]) + "x", best_ask)
                            orders.append(
                                Order(product, best_ask, -state.position[product])
                            )

                            
                            # If position not fully executed
                            if abs(state.position[product]) > abs(best_ask_volume):
                                
                                # position remaining volumn
                                position_r_vol = state.position[product] - best_ask_volume # negative value

                                # Check if the 2nd ask could meet all remaining volumn
                                if abs(position_r_vol) > abs(best_ask_volume_2):        # not met all
                                    print("BUY", str(-best_ask_volume_2) + "x", best_ask_2)
                                    orders.append(
                                        Order(product, best_ask_2, -best_ask_volume_2)
                                    )
                                
                                else:    # met all
                                    print("BUY", str(-position_r_vol) + "x", best_ask_2)
                                    orders.append(
                                        Order(product, best_ask_2, -position_r_vol)
                                    )




                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result
