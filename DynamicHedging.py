from PyOptionClasses.OptionsClass import greeks, option


# Desc: Find the number of stock needed to buy (or sell) to become delta neutral
# Input: Option position and number of contracts
# Output: Number of underlying needed to hedge option (+ for long, - for short)
def delta_neutrality_stock(option_position, num_contracts):
    option_delta = option_position.greeks.delta
    contract_delta = option_delta * num_contracts
    stock_equivalent = -1 * contract_delta
    return stock_equivalent
