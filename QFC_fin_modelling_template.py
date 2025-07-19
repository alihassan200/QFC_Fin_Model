class Market:
    transaction_fee = 0.005

    def __init__(self) -> None:
        self.stocks = {"HydroCorp": 123, "BrightFuture": 456}

    def updateMarket(self):
        # Will be implemented during grading. This function will update the
        # stock values to their "real" values each day.
        pass


class Portfolio:
    def __init__(self) -> None:
        self.shares = {"HydroCorp": 0, "BrightFuture": 0}
        self.cash = 100000

    def evaluate(self, curMarket: Market) -> float:
        valueA = self.shares["HydroCorp"] * curMarket.stocks["HydroCorp"]
        valueB = self.shares["BrightFuture"] * curMarket.stocks["BrightFuture"]

        return valueA + valueB + self.cash

    def sell(self, stock_TSLA: str, sharesToSell: float,
             curMarket: Market) -> None:
        if sharesToSell <= 0:
            raise ValueError("Number of shares must be positive")

        if sharesToSell > self.shares[stock_TSLA]:
            raise ValueError("Attempted to sell more stock than is available")

        self.shares[stock_TSLA] -= sharesToSell
        self.cash += (1 - Market.transaction_fee) * sharesToSell * \
                     curMarket.stocks[stock_TSLA]

    def buy(self, stock_TSLA: str, sharesToBuy: float,
            curMarket: Market) -> None:
        if sharesToBuy <= 0:
            raise ValueError("Number of shares must be positive")

        cost = (1 + Market.transaction_fee) * sharesToBuy * curMarket.stocks[
            stock_TSLA]
        if cost > self.cash:
            raise ValueError("Attempted to spend more cash than available")

        self.shares[stock_TSLA] += sharesToBuy
        self.cash -= cost


class Context:
    def __init__(self) -> None:
        self.day_count = 0
        self.averages = {
            "HydroCorp": {"daily": 0.0, "three_day": 0.0, "ten_day": 0.0},
            "BrightFuture": {"daily": 0.0, "three_day": 0.0, "ten_day": 0.0}
        }
        self.price_history = {
            "HydroCorp": [],
            "BrightFuture": []
        }
        self.shocks = {
            50: "Environmental Bill",
            100: "Hurricane",
            150: "Oil Tech",
            250: "OPEC Cuts"
        }
        self.non_dca_shares = {"HydroCorp" : 0, "BrightFuture": 0}

    def update_non_dca_shares (self, company: str, shares: int) -> None:
        self.non_dca_shares[company] += shares

    def next_day(self):
        """Increments the day count."""
        self.day_count += 1

    def update_prices(self, new_prices):
        """
        Updates the price history and recalculates moving averages for both companies.
        :param new_prices: A dictionary containing new prices for both stocks.
                           Example: {"HydroCorp": 120, "BrightFuture": 98}
        """
        for stock, price in new_prices.items():
            self.price_history[stock].append(price)

            # Keep only the last 10 days of prices to limit memory usage
            if len(self.price_history[stock]) > 10:
                self.price_history[stock].pop(0)

        self.calculate_averages()

    def calculate_averages(self):
        """Calculates daily, 3-day, and 10-day moving averages for both stocks."""
        for stock, prices in self.price_history.items():
            if len(prices) >= 1:
                self.averages[stock]["daily"] = sum(prices[-2:]) / 2 # Most recent price

            if len(prices) >= 3:
                self.averages[stock]["three_day"] = sum(prices[-3:]) / 3

            if len(prices) >= 10:
                self.averages[stock]["ten_day"] = sum(prices) / len(prices)


def update_portfolio(curMarket: Market, curPortfolio: Portfolio,
                     context: Context):
    day = context.day_count
    daily_stock_price = curMarket.stocks
    context.update_prices(daily_stock_price)

    # Dollar Cost Averaging
    if (day == 0 or day % 30 == 0) and day < 360:  # Monthly DCA (every 30 days)
        bf_investment = 1500
        hc_investment = 1000

        # Buy $1500 worth of BF stocks
        if curPortfolio.cash >= bf_investment:
            bf_shares = int(bf_investment // (curMarket.stocks["BrightFuture"] * 1.005))
            if bf_shares > 0:
                curPortfolio.buy("BrightFuture", bf_shares, curMarket)

        # Buy $1000 worth of HC stocks
        if curPortfolio.cash >= hc_investment:
            hc_shares = int(hc_investment // (curMarket.stocks["HydroCorp"] * 1.005))
            if hc_shares > 0:
                curPortfolio.buy("HydroCorp", hc_shares, curMarket)

    # Specific day-based actions
    if day == 4:
        hc_investment = 50000  # Buy $50,000 worth of HydroCorp stocks
        if curPortfolio.cash >= hc_investment:
            hc_shares = int(hc_investment // (curMarket.stocks["HydroCorp"] * 1.005))
            if hc_shares > 0:
                curPortfolio.buy("HydroCorp", hc_shares, curMarket)
                context.update_non_dca_shares("HydroCorp", hc_shares)

    if day == 52:
        bf_investment = 20000  # Buy $20,000 worth of BrightFuture stocks
        if curPortfolio.cash >= bf_investment:
            bf_shares = int(bf_investment // (curMarket.stocks["BrightFuture"] * 1.005))
            if bf_shares > 0:
                curPortfolio.buy("BrightFuture", bf_shares, curMarket)
                context.update_non_dca_shares("BrightFuture", bf_shares)


    if day == 85:
        # Sell $25,000 worth of HC stocks
        hc_to_sell = int(25000 // curMarket.stocks["HydroCorp"])
        if hc_to_sell > 0 and context.non_dca_shares["HydroCorp"] >= hc_to_sell:
            curPortfolio.sell("HydroCorp", hc_to_sell, curMarket)
            context.update_non_dca_shares("HydroCorp", -hc_to_sell)

    if day == 95:
        bf_investment = 10000  # Buy $10,000 worth of BrightFuture stocks
        if curPortfolio.cash >= bf_investment:
            bf_shares = int(bf_investment // (curMarket.stocks["BrightFuture"] * 1.005))
            if bf_shares > 0:
                curPortfolio.buy("BrightFuture", bf_shares, curMarket)
                context.update_non_dca_shares("BrightFuture", bf_shares)

    if day == 103:
        # Sell all BF stocks and buy $35,000 worth of HC stocks
        bf_shares_to_sell = int(context.non_dca_shares["BrightFuture"])
        if bf_shares_to_sell > 0:
            curPortfolio.sell("BrightFuture", bf_shares_to_sell, curMarket)
            context.update_non_dca_shares("BrightFuture", -bf_shares_to_sell)

        hc_investment = 35000
        if curPortfolio.cash >= hc_investment:
            hc_shares = int(hc_investment // (curMarket.stocks["HydroCorp"] * 1.005))
            if hc_shares > 0:
                curPortfolio.buy("HydroCorp", hc_shares, curMarket)
                context.update_non_dca_shares("HydroCorp", hc_shares)
    # day + 1
    context.next_day()

###SIMULATION###
market = Market()
portfolio = Portfolio()
context = Context()

for i in range(365):
    update_portfolio(market, portfolio, context)
    market.updateMarket()

print(portfolio.evaluate(market))
