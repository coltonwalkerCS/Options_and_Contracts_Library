class greeks:
    def __init__(self, delta, gamma, theta, vega, rho):
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho

    def update_greeks(self, delta, gamma, theta, vega, rho):
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho

    def get_greeks(self):
        return self.delta, self.gamma, self.theta, self.vega, self.rho


# Desc:
class option:
    def __init__(self, option_type, strike_price, cost, curr_greeks):
        # 1 for call, -1 for put
        self.option_type = option_type
        self.strike_price = strike_price
        self.curr_cost = cost
        self.greeks = curr_greeks
