from option_class import greeks, option


# Desc: Find the number of stock needed to buy (or sell) to become delta neutral
# Input:
# Output:
def delta_neutrality_stock(option_position, num_contracts):
    option_delta = option_position.greeks.delta
    contract_delta = option_delta * num_contracts
    stock_equivalent = -1 * contract_delta
    return stock_equivalent


test_greeks = greeks(0.5, 0.1, -0.06, 0.01, 0.01)
test_option = option(1, 99.50, 5.00, test_greeks)

equiv_stock = delta_neutrality_stock(test_option, 2)
print(f'Equivalent stock: {equiv_stock}')
