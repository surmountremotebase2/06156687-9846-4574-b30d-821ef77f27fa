from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, Momentum
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers you are interested in
        # SPY for the S&P 500 ETF and GLD for Gold ETF
        self.tickers = ["SPY", "GLD"]

    @property
    def interval(self):
        # Set how often the strategy should be running, e.g., Daily
        return "1day"

    @property
    def assets(self):
        # List of assets the strategy will handle
        return self.tickers

    @property
    def data(self):
        # This strategy does not need additional data aside from price
        return []

    def run(self, data):
        # Initialize the allocation for both SPY and GLD to 0
        allocation = {"SPY": 0, "GLD": 0}
        
        # Calculate the 20-day Momentum for SPY to assess its trend
        spy_momentum = Momentum("SPY", data["ohlcv"], 20)
        
        # Ensure there is enough data to calculate the Momentum
        if spy_momentum is not None and len(spy_momentum) > 0:
            # If the most recent Momentum is positive, it implies upward trend
            if spy_momentum[-1] > 0:
                # In the case of upward momentum in SPY, short GLD
                # Here, we are expressing a bearish outlook on gold, thus a negative allocation
                # Change the allocation based on your shorting strategy or broker's requirements
                allocation["GLD"] = -0.5  # Example short position as 50% of the portfolio value
            else:
                # If SPY shows downward momentum, take a long position on GLD
                # Assuming gold may move inversely to the market
                allocation["GLD"] = 1.0  # 100% allocation towards GLD
        
        # Log the Momentum for tracking
        log(f"SPY Momentum: {spy_momentum[-1] if spy_momentum else 'N/A'}")
        
        # Return the target allocations
        return TargetAllocation(allocation)