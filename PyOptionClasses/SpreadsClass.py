from PyOptionClasses.OptionsClass import option, option_data, greeks
import numpy as np
import math


# Spread
class Spread:
    def __init__(self, options, ratio):
        self.options = options

        # Included for ratio spreads
        self.ratio = ratio

        self.greeks = self.generate_spread_greeks()
        self.cost = round(sum(op.curr_cost for op in options), 2)

        # Risk profile of spread
        self.underlying_price = options[0].curr_stock_price
        self.price_range = options[0].get_standard_deviation_price_move_range()
        self.payoff_profile = self.calc_spread_profit_payout()
        self.max_profit, self.max_loss, self.break_even_points = self.calc_spread_metrics()

    def calc_spread_profit_payout(self):

        # Need to go through and find if options have difference if so, difference = further options time
        calendar = False
        original_exp = self.options[0].annual_time_to_expiration
        for i in range(1, len(self.options)):
            if self.options[i].annual_time_to_expiration != original_exp:
                calendar = True

        if calendar:
            # Need to find how many are different
            time_to_exp = []
            for option in self.options:
                if option.annual_time_to_expiration not in time_to_exp:
                    time_to_exp.append(option.annual_time_to_expiration)

            min_time_to_exp = min(time_to_exp)

            # Group them together
            updated_option_list = []

            for option in self.options:
                updatedOption = option
                updatedOption.update_time_to_expiration(option.annual_time_to_expiration-min_time_to_exp)
                updated_option_list.append(updatedOption)

            if updated_option_list[0].strike_price == 44 and updated_option_list[1].strike_price == 44:
                if updated_option_list[0].option_type == 'call' and updated_option_list[1].option_type == 'call':

                    print('Test payoff profile')
                    print(f'For {updated_option_list[0].trade} | {updated_option_list[0].annual_time_to_expiration} : {updated_option_list[0].payoff_profile}')
                    print(f'For {updated_option_list[1].trade} | {updated_option_list[1].annual_time_to_expiration} : {updated_option_list[1].payoff_profile}')

            # Find the total payoff after updating the time to expiration
            total_payoff_profile = updated_option_list[0].payoff_profile
            for i in range(1, len(updated_option_list)):
                total_payoff_profile = [round(x + y, 2) for x, y in
                                        zip(total_payoff_profile, updated_option_list[i].payoff_profile)]
                # Used primarily for ratio spreads and if there is a specific ratio for a spread
                pre_value = total_payoff_profile[0]
                multiplier = self.ratio[i]
                total_payoff_profile = [element * multiplier for element in total_payoff_profile]

                # To make sure it worked
                assert (pre_value * multiplier == total_payoff_profile[0])

        else:
            total_payoff_profile = self.options[0].payoff_profile
            for i in range(1, len(self.options)):
                total_payoff_profile = [round(x + y, 2) for x, y in
                                        zip(total_payoff_profile, self.options[i].payoff_profile)]
                # Used primarily for ratio spreads and if there is a specific ratio for a spread
                pre_value = total_payoff_profile[0]
                multiplier = self.ratio[i]
                total_payoff_profile = [element * multiplier for element in total_payoff_profile]

                # To make sure it worked
                assert(pre_value * multiplier == total_payoff_profile[0])

        return total_payoff_profile

    def calc_spread_metrics(self):
        max_profit = round(max(self.payoff_profile), 2)
        max_loss = round(min(self.payoff_profile), 2)

        break_even_point = [self.price_range[i] for i, payoff in enumerate(self.payoff_profile) if payoff == 0]

        # risk_reward_ratio = -max_loss / max_profit if max_profit != 0 else None
        # risk_reward_ratio

        return max_profit, max_loss, break_even_point

    def print_risk_profile(self):
        print(f' Price range: {self.price_range}')
        print(f' Payoff profile: {self.payoff_profile}')
        print(f' Max profit: {self.max_profit}')
        print(f' Max loss: {self.max_loss}')
        print(f' Break even point(s): {self.break_even_points}')
        return

    def generate_spread_greeks(self):
        # Delta, Gamma, Theta, Vega, Rho
        # TODO: Fix once rho is added to data
        delta, gamma, theta, vega, rho = 0, 0, 0, 0, 0.01

        for op in self.options:
            delta += op.greeks.delta
            gamma += op.greeks.gamma
            theta += op.greeks.theta
            vega += op.greeks.vega

        return greeks(round(delta, 4), round(gamma, 4), round(theta, 4), round(vega, 4), round(rho, 4))


class Straddle(Spread):
    def __init__(self, strike_price, call_option, put_option, expiration):
        super().__init__([call_option, put_option], [1, 1])
        self.name = 'Straddle'
        self.strike_price = strike_price
        self.call_option = call_option
        self.put_option = put_option
        self.expiration = expiration

    def print_straddle(self):
        print(f'Strike price: {self.strike_price} at date {self.expiration}')
        print(
            f'Call option {self.call_option.trade}, Cost: {self.call_option.curr_cost}, Greeks {self.call_option.greeks.get_greeks()}')
        print(
            f'Put option {self.put_option.trade},, Cost: {self.put_option.curr_cost}, Greeks {self.put_option.greeks.get_greeks()}')
        print(f'Straddle, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class Strangle(Spread):
    def __init__(self, strangle_range, option_1, option_2, expiration):
        super().__init__([option_1, option_2], [1, 1])
        self.name = 'Strangle'
        self.strangle_range = strangle_range
        self.mid_price = abs(option_1.strike_price - option_2.strike_price)
        self.option_1 = option_1
        self.option_2 = option_2
        self.expiration = expiration

    def print_strangle(self):
        print(f'Mid price: {self.mid_price} and Range: {self.strangle_range} at date {self.expiration}')
        print(
            f'Option 1 {self.option_1.trade}, Type: {self.option_1.option_type}, Strike: {self.option_1.strike_price}, '
            f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(
            f'Option 2 {self.option_2.trade}, Type: {self.option_2.option_type}, Strike: {self.option_2.strike_price}, '
            f'Cost: {self.option_2.curr_cost}, Greeks {self.option_2.greeks.get_greeks()}')
        print(f'Strangle, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class Butterfly(Spread):

    def __init__(self, butterfly_range, option_1, option_2_1, option_2_2, option_3, expiration):
        super().__init__([option_1, option_2_1, option_2_2, option_3], [1, 1, 1, 1])
        self.name = 'Butterfly'
        self.butterfly_range = butterfly_range
        self.center_price = option_2_1.strike_price
        self.option_1 = option_1
        # Inherently has 2 middle options
        self.option_2_1 = option_2_1
        self.option_2_2 = option_2_2
        self.option_3 = option_3
        self.expiration = expiration

    def print_butterfly(self):
        print(f'Center price: {self.center_price} and Range: {self.butterfly_range} at date {self.expiration}')
        print(
            f'Option 1, Type: {self.option_1.option_type} | {self.option_1.trade}, Strike: {self.option_1.strike_price}, '
            f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(
            f'Option 2_1, Type: {self.option_2_1.option_type} | {self.option_2_1.trade}, Strike: {self.option_2_1.strike_price}, '
            f'Cost: {self.option_2_1.curr_cost}, Greeks {self.option_2_1.greeks.get_greeks()}')
        print(
            f'Option 2_2, Type: {self.option_2_2.option_type} | {self.option_2_2.trade}, Strike: {self.option_2_2.strike_price}, '
            f'Cost: {self.option_2_2.curr_cost}, Greeks {self.option_2_2.greeks.get_greeks()}')
        print(
            f'Option 3, Type: {self.option_3.option_type} | {self.option_3.trade}, Strike: {self.option_3.strike_price}, '
            f'Cost: {self.option_3.curr_cost}, Greeks {self.option_3.greeks.get_greeks()}')
        print(f'Butterfly, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class Condor(Spread):
    def __init__(self, condor_outer_range, condor_inner_range, option_1, option_2, option_3, option_4, expiration):
        super().__init__([option_1, option_2, option_3, option_4], [1, 1, 1, 1])
        self.name = 'Condor'
        self.condor_outer_range = condor_outer_range
        self.condor_inner_range = condor_inner_range
        self.center_price = abs(option_3.strike_price - option_2.strike_price)
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.expiration = expiration

    def print_condor(self):
        print(f'Center price: {self.center_price}, Outer Range: {self.condor_outer_range}, Inner Range: '
              f'{self.condor_inner_range} at date {self.expiration}')
        print(
            f'Option 1, Type: {self.option_1.option_type} | {self.option_1.trade}, Strike: {self.option_1.strike_price}, '
            f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(
            f'Option 2, Type: {self.option_2.option_type} | {self.option_2.trade}, Strike: {self.option_2.strike_price}, '
            f'Cost: {self.option_2.curr_cost}, Greeks {self.option_2.greeks.get_greeks()}')
        print(
            f'Option 3, Type: {self.option_3.option_type} | {self.option_3.trade}, Strike: {self.option_3.strike_price}, '
            f'Cost: {self.option_3.curr_cost}, Greeks {self.option_3.greeks.get_greeks()}')
        print(
            f'Option 4, Type: {self.option_4.option_type} | {self.option_4.trade}, Strike: {self.option_4.strike_price}, '
            f'Cost: {self.option_4.curr_cost}, Greeks {self.option_4.greeks.get_greeks()}')
        print(f'Condor, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class IronCondor(Spread):
    def __init__(self, condor_outer_range, condor_inner_range, option_1, option_2, option_3, option_4, expiration):
        super().__init__([option_1, option_2, option_3, option_4], [1, 1, 1, 1])
        self.name = 'Iron Condor'
        self.condor_outer_range = condor_outer_range
        self.condor_inner_range = condor_inner_range
        self.center_price = abs(option_3.strike_price - option_2.strike_price)
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.expiration = expiration

    def print_iron_condor(self):
        print(f'Center price: {self.center_price}, Outer Range: {self.condor_outer_range}, Inner Range: '
              f'{self.condor_inner_range} at date {self.expiration}')
        print(
            f'Option 1, Type: {self.option_1.option_type} | {self.option_1.trade}, Strike: {self.option_1.strike_price}, '
            f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(
            f'Option 2, Type: {self.option_2.option_type} | {self.option_2.trade}, Strike: {self.option_2.strike_price}, '
            f'Cost: {self.option_2.curr_cost}, Greeks {self.option_2.greeks.get_greeks()}')
        print(
            f'Option 3, Type: {self.option_3.option_type} | {self.option_3.trade}, Strike: {self.option_3.strike_price}, '
            f'Cost: {self.option_3.curr_cost}, Greeks {self.option_3.greeks.get_greeks()}')
        print(
            f'Option 4, Type: {self.option_4.option_type} | {self.option_4.trade}, Strike: {self.option_4.strike_price}, '
            f'Cost: {self.option_4.curr_cost}, Greeks {self.option_4.greeks.get_greeks()}')
        print(f'Iron Condor, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class RatioSpread(Spread):
    def __init__(self, option_1, option_2, expiration, ratio_range):
        self.op1_ratio, self.op2_ratio = self.get_whole_num_ratio(option_1, option_2)
        super().__init__([option_1, option_2], [self.op1_ratio, self.op2_ratio])
        self.name = 'Ratio'
        self.option_1 = option_1
        self.option_2 = option_2
        self.ratio_range = ratio_range
        self.expiration = expiration

    def get_whole_num_ratio(self, option_1, option_2):
        numerator = int(abs(option_1.greeks.delta * 100))
        denominator = int(abs(option_2.greeks.delta * 100))

        gcd = math.gcd(numerator, denominator)

        ratio_num_one = numerator // gcd
        ratio_num_two = denominator // gcd
        ratios = [ratio_num_one, ratio_num_two]
        ratios.sort()

        # If option 1 has smaller delta give it
        # the larger ratio number and vis versa
        if abs(option_1.greeks.delta) < abs(option_2.greeks.delta):
            return ratios[1], ratios[0]
        else:
            return ratios[0], ratios[1]


class ChristmasTree(Spread):
    def __init__(self, option_1, option_2, option_3, expiration, christmas_range):
        super().__init__([option_1, option_2, option_3], [1, 1, 1])
        self.name = 'Christmas Tree'
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.center_price = self.option_2.strike_price
        self.christmas_range = christmas_range
        self.expiration = expiration

    def print_christmas_tree(self):
        print(f'Center price: {self.center_price} and Range: {self.christmas_range} at date {self.expiration}')
        print(
            f'Option 1, Type: {self.option_1.option_type} | {self.option_1.trade}, Strike: {self.option_1.strike_price}, '
            f'Cost: {self.option_1.curr_cost}, Greeks {self.option_1.greeks.get_greeks()}')
        print(
            f'Option 2, Type: {self.option_2.option_type} | {self.option_2.trade}, Strike: {self.option_2.strike_price}, '
            f'Cost: {self.option_2.curr_cost}, Greeks {self.option_2.greeks.get_greeks()}')
        print(
            f'Option 3, Type: {self.option_3.option_type} | {self.option_3.trade}, Strike: {self.option_3.strike_price}, '
            f'Cost: {self.option_3.curr_cost}, Greeks {self.option_3.greeks.get_greeks()}')
        print(f'Christmas Tree, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')


class CalenderSpread(Spread):
    def __init__(self, option_1, option_2, expiration_1, expiration_2):
        super().__init__([option_1, option_2], [1, 1])
        self.name = 'Straddle Calender Spread'
        self.option_1 = option_1
        self.expiration_1 = expiration_1
        self.option_2 = option_2
        self.expiration_2 = expiration_2

    def print_calender_spread(self):
        print(f'{self.name}')
        print(
            f'Option 1, Type: {self.option_1.option_type} | {self.option_1.trade}, Strike: '
            f'{self.option_1.strike_price}, Cost: {self.option_1.curr_cost}, Greeks '
            f'{self.option_1.greeks.get_greeks()}, at expiration {self.expiration_1}')
        print(
            f'Option 2, Type: {self.option_2.option_type} | {self.option_2.trade}, Strike: '
            f'{self.option_2.strike_price}, Cost: {self.option_2.curr_cost}, Greeks '
            f'{self.option_2.greeks.get_greeks()}, at expiration {self.expiration_2}')
        print(f'Calender Spread, Cost: {self.cost}, Greeks {self.greeks.get_greeks()} \n')
