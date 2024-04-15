from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Momentum
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define tickers for gold and SPY.
        # Assuming GLD as a proxy for the price of gold in this strategy.
        self.tickers = ["SPY", "GLD"]

    @property
    def interval(self):
        # Use daily data for analysis to make day trading decisions
        return "1day"

    @property
    def assets(self):
        # Interested in trading GLD based on SPY's movement
        return self.tickers

    def run(self, data):
        # Initialize a dictionary to hold our target allocations.
        allocation_dict = {"GLD": 0}

        # Check if we have enough data to calculate momentum
        if len(data["ohlcv"]) > 20: # Assuming a 20-day momentum indicator
            spy_momentum = Momentum("SPY", data["ohlcv"], length=20)[-1]

            # If SPY's momentum is positive, we anticipate a downturn in GLD
            # and thus short GLD (assuming we can short in this framework, represented as a negative allocation)
            if spy_momentum > 0:
                allocation_dict["GLD"] = -0.5  # Short half of the portfolio on GLD
                log("Shorting GLD based on positive SPY momentum")

            # If SPY's momentum is negative, we anticipate GLD to rise
            # and go long on GLD.
            elif spy_momentum < 0:
                allocation_dict["GLD"] = 1  # Go fully long on GLD
                log("Going long on GLD based on negative SPY momentum")

            # If momentum is 0 or we don't have enough data, do not take a position
            else:
                log("SPY momentum neutral or insufficient data. No action taken on GLD.")

        else:
            # Log a message if there is not enough data to make a decision.
            log("Insufficient data for momentum calculation. No action taken.")

        # Return our target allocation decision.
        return TargetAllocation(allocation_dict)