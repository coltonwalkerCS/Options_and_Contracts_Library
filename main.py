import pandas as pd

from Commodities_Future_Pricing_Lib import getConvenienceYield_XMoContract, stockForwardPrice, generateDivPayments, \
    simpleStockForwardPrice, generateCouponMonthPayments, bondForwardPrice
from PricingModels import call_option_expected_value, get_theoretical_value_of_contract, put_option_expected_value, \
    get_scaled_volatility, black_scholes_model_option_price, calc_theta_for_atm_option
from DynamicHedging import delta_neutrality_stock
from OptionsClass import greeks, option
from CodeTest import CommoditiesFuturesTest, PricingModelsTest, DynamicHedgingTest, FindingSpreadsTest


def main():
    print(' -- Start -- ')
    return


main()
