import matplotlib.pyplot as plt
import numpy as np


def call_option_parity(strike_price, current_cost):
    # Define a range of possible stock prices at expiration
    stock_prices = np.linspace(0, 2 * strike_price, 100)

    # Calculate the profit or loss for each stock price
    profit_loss = np.maximum(stock_prices - strike_price - current_cost, -current_cost)

    # Find the break even point
    break_even_index = np.where(profit_loss >= 0)[0][0]
    print(break_even_index)
    break_even_price = stock_prices[break_even_index]

    # Plot the parity graph
    plt.figure(figsize=(8, 6))
    plt.plot(stock_prices, profit_loss)
    plt.axhline(y=0, color='black', linestyle='--')
    plt.axvline(x=strike_price, color='red', linestyle='--', label=f'Strike Price {strike_price}')
    plt.scatter(break_even_price, 0, color='green', label='Break even Point')
    plt.annotate(f'({break_even_price:.2f}, 0)', xy=(break_even_price, 0), xytext=(break_even_price + 10, 10),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate(f'Loss = {current_cost}', xy=(stock_prices[0], -current_cost),
                 xytext=(stock_prices[0] + 10, -current_cost + 10),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.xlabel('Stock Price at Expiration')
    plt.ylabel('Profit/Loss')
    plt.title('Call Option Parity at Expiration')
    plt.legend()
    plt.grid(True)
    plt.show()


def put_option_parity(strike_price, current_cost):
    # Define a range of possible stock prices at expiration
    stock_prices = np.linspace(0, 2 * strike_price, 2 * strike_price+1)

    # Calculate the profit or loss for each stock price
    profit_loss = np.maximum(strike_price - stock_prices - current_cost, -current_cost)
    # print(profit_loss)
    # Find the break even point
    break_even_index = np.where(profit_loss >= 0)[0][-1]
    break_even_price = stock_prices[break_even_index]

    # Plot the parity graph
    plt.figure(figsize=(8, 6))
    plt.plot(stock_prices, profit_loss)
    plt.axhline(y=0, color='black', linestyle='--')
    plt.axvline(x=strike_price, color='red', linestyle='--', label='Strike Price')
    plt.scatter(break_even_price, 0, color='green', label='Break even Point')
    plt.annotate(f'({break_even_price:.2f}, 0)', xy=(break_even_price, 0), xytext=(break_even_price - 75, 10),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate(f'Loss = {current_cost}', xy=(strike_price, -current_cost),
                 xytext=(strike_price + 10, -current_cost + 10),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.xlabel('Stock Price at Expiration')
    plt.ylabel('Profit/Loss')
    plt.title('Put Option Parity at Expiration')
    plt.legend()
    plt.grid(True)
    plt.show()


# generateTestGraph()
# call_option_parity(95, 6.25)
put_option_parity(200, 5)
