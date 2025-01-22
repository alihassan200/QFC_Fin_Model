
class Market:
    transaction_fee = 0.005
    def __init__(self) -> None:
        self.stocks = {"HydroCorp": 123, "BrightFuture": 456}  # stocks what does it mean 

    def updateMarket(self):
        #Will be implemented during grading. 
        #This function will update the stock values to their "real" values each day.
        pass
 
class Portfolio:
    def __init__(self) -> None:
        self.shares = {"HydroCorp": 0, "BrightFuture": 0}
        self.cash = 100000

    def evaluate(self, curMarket: Market) -> float:
        valueA = self.shares["HydroCorp"] * curMarket.stocks["HydroCorp"]
        valueB = self.shares["BrightFuture"] * curMarket.stocks["BrightFuture"]

        return valueA + valueB + self.cash   ##what is the total value to but cant we change the value of the hydrocrop thing in this context. 

    def sell(self, stock_TSLA: str, sharesToSell: float, curMarket: Market) -> None:    # none means void bsaicallyy 
        if sharesToSell <= 0:
            raise ValueError("Number of shares must be positive")

        if sharesToSell > self.shares[stock_TSLA]:
            raise ValueError("Attempted to sell more stock than is available")

        self.shares[stock_TSLA] -= sharesToSell
        self.cash += (1 - Market.transaction_fee) * sharesToSell * curMarket.stocks[stock_TSLA]   # in this is you get the update value of the cash market 

    def buy(self, stock_TSLA: str, sharesToBuy: float, curMarket: Market) -> None:
        if sharesToBuy <= 0:
            raise ValueError("Number of shares must be positive")
        
        cost = (1 + Market.transaction_fee) * sharesToBuy * curMarket.stocks[stock_TSLA]
        if cost > self.cash:
            raise ValueError("Attempted to spend more cash than available")

        self.shares[stock_TSLA] += sharesToBuy   ## you add that in shares 
        self.cash -= cost

class Context:
    def __init__(self) -> None:
        pass

    # for day 12 take 

    # one of the variables can be the cash in this case 
    # but in this what stock price 

    
        
    ## so we have to update here the context and just use the market and portfolio function to call out that 
    For each potential shock mentioned, using data from your model  # see they are using this model from it, for normal days take it from model
    # and then also consider shocks using the data, and shiraz would confirm the model using excel file and then we would use this 
on that  day, discuss how you would hedge against these risks.

Within update_portfollio, you may only update 
your portfolio via the Portfollio.buy and Portfolio.sell methods. Do not manually
change how many units of stock are in your portfolio. Any submission which does this
will not be counted.
    
    # PUT WHATEVER YOU WANT HERE

def update_portfolio(curMarket: Market, curPortfolio: Portfolio, context: Context):
    # YOUR TRADING STRATEGY GOES HERE
    pass
    

###SIMULATION###
market = Market()
portfolio = Portfolio()
context = Context()

for i in range(365):
    update_portfolio(market, portfolio, context)
    market.updateMarket()   ## so will they passs from this day to this day the person wants to trade or joint in the middle of the year and now evulate 
    # or will they take the full 

print(portfolio.evaluate(market))  



## starting value 100,000
# have to divide accordingly



