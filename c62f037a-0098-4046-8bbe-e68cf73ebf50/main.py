from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Tickers for SPY and a Gold ETF (e.g., GLD)
        self.tickers = ["SPY", "GLD"]
    
    @property
    def interval(self):
        # Daily interval for making trading decisions
        return "1day"
    
    @property
    def assets(self):
        # Assets involved in the strategy
        return self.tickers
    
    @property
    def data(self):
        # Data required for the strategy; 
        # here, it implicitly refers to price data (e.g., open, high, low, close, volume)
        return []
    
    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {"GLD": 0}
        
        # Check if there is enough data
        if "ohlcv" in data and len(data["ohlcv"]) >= 2:
            # Get previous day's close prices for SPY
            prev_close_spy = data["ohlcv"][-2]["SPY"]["close"]
            # Get current day's open price for SPY
            current_open_spy = data["ohlcv"][-1]["SPY"]["open"]

            # Determine the direction of SPY's performance by comparing open to previous close
            if current_open_spy > prev_close_spy:
                # If SPY opened higher than its previous close, anticipate a bearish day for gold
                # Set allocation to 0, indicating no position in GLD for the day
                allocation_dict["GLD"] = 0
            else:
                # If SPY opened lower than its previous close, anticipate a bullish day for gold
                # Set allocation to 1, meaning fully allocate to GLD for the day
                allocation_dict["GLD"] = 1
        
        # Return the target allocation for GLD based on SPY's movement
        return TargetAllocation(allocation_dict)