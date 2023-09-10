from yahoo_fin import options as op

ticker = "AAPL"

expirationDates = op.get_expiration_dates(ticker)

print(expirationDates)