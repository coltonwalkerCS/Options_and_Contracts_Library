import pandas as pd
from PricingModels import black_scholes_model_option_price
from OptionsClass import option_data


call_options_exp_may_15_data = {
    'Exercise Price': [44, 46, 48, 50, 52, 54],
    'Price': [4.59, 2.99, 1.75, 0.93, 0.47, 0.23],
    # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
    'Delta': [0.92, 0.78, 0.56, 0.33, 0.16, 0.06],
    'Gamma': [0.045, 0.088, 0.116, 0.107, 0.072, 0.037],
    'Theta': [-0.0046, -0.0091, -0.0121, -0.0111, -0.0075, -0.0038],
    'Vega': [0.029, 0.057, 0.075, 0.069, 0.047, 0.024],
    'Implied Volatility': [19.83, 20.25, 20.48, 20.88, 21.63, 22.46]
}
put_options_exp_may_15_data = {
    'Exercise Price': [44, 46, 48, 50, 52, 54],
    'Price': [0.2, 0.58, 1.35, 2.53, 4.06, 5.84],
    # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
    'Delta': [-0.08, -0.22, -0.44, -0.67, -0.84, -0.94],
    'Gamma': [0.045, 0.088, 0.116, 0.107, 0.072, 0.037],
    'Theta': [-0.0046, -0.0091, -0.0121, -0.0111, -0.0075, -0.0038],
    'Vega': [0.029, 0.057, 0.075, 0.069, 0.047, 0.024],
    'Implied Volatility': [20.12, 20.09, 20.48, 20.88, 21.45, 22.73]
}

call_options_exp_july_15_data = {
    'Exercise Price': [44, 46, 48, 50, 52, 54],
    'Price': [4.96, 3.52, 2.38, 1.55, 0.97, 0.60],
    # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
    'Delta': [0.84, 0.71, 0.55, 0.39, 0.25, 0.15],
    'Gamma': [0.050, 0.071, 0.082, 0.080, 0.066, 0.048],
    'Theta': [-0.0052, -0.0074, -0.0085, -0.0083, -0.0069, -0.0050],
    'Vega': [0.064, 0.091, 0.106, 0.103, 0.085, 0.062],
    'Implied Volatility': [20.12, 20.21, 20.42, 20.80, 21.14, 21.64]
}

put_options_exp_july_15_data = {
    'Exercise Price': [44, 46, 48, 50, 52, 54],
    'Price': [0.56, 0.92, 1.98, 3.14, 4.58, 6.21],
    # 'Theoretical value': [10.5, 20.3, 15.7, 8.9, 12.1],
    'Delta': [-0.16, -0.29, -0.45, -0.61, -0.75, -0.85],
    'Gamma': [0.050, 0.071, 0.082, 0.080, 0.066, 0.048],
    'Theta': [-0.0052, -0.0074, -0.0085, -0.0083, -0.0069, -0.0050],
    'Vega': [0.064, 0.091, 0.106, 0.103, 0.085, 0.062],
    'Implied Volatility': [20.12, 20.31, 20.42, 20.71, 21.25, 21.78]
}

# Put options data into df
call_may_df = pd.DataFrame(call_options_exp_may_15_data)
put_may_df = pd.DataFrame(put_options_exp_may_15_data)

call_july_df = pd.DataFrame(call_options_exp_july_15_data)
put_july_df = pd.DataFrame(put_options_exp_july_15_data)

call_may_options = option_data(call_may_df, 'May 15', 'call', 48.40,0.1534, 0.0, 18)
call_may_options.print_options()
