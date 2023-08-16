# TODO: -Create risk management class
import math
import numpy as np

# TODO: -Find the min and max for the spread
#       -Calc break even point @ expiration
#       -Analyze risk and reward


class OptionRiskProfile:

    def __init__(self, option_curr):
        self.option = option_curr
        self.price_range = self.get_standard_deviation_price_move_range()

    def get_standard_deviation_price_move_range(self):
        standard_deviation = (self.option.curr_stock_price * (self.option.current_volatility/100) *
                              math.sqrt(self.option.annual_time_to_expiration * 365)) / math.sqrt(365)

        price_range_lower_bound = self.option.curr_stock_price - (3 * standard_deviation)
        price_range_upper_bound = self.option.curr_stock_price + (3 * standard_deviation)
        num_points = int((price_range_upper_bound - price_range_lower_bound) * 100)

        price_range_list = np.linspace(price_range_lower_bound, price_range_upper_bound, num_points)

        return price_range_list


# class RiskProfile:
#     def __init__(self, spread):
#         self.spread = spread
#         self.options_list = spread.returnOptions()
#