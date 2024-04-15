from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, OHLCV
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets the strategy focuses on.
        # In this case, we focus on gold as represented by 'GLD' 
        # and the VIX volatility index, represented by 'VIX'.
        self.tickers = ["GLD", "VIX"]

    @property
    def interval(self):
        # The time interval for data collection, '1day' for daily trading.
        return "1day"

    @property
    def assets(self):
        # The assets that this strategy trades.
        return self.tickers

    @property
    def data(self):
        # Data needed for the trading strategy which includes the assets' OHLCV data.
        return [OHLCV(ticker) for ticker in self.tickers]

    def run(self, data):
        # Extract the most recent closing prices for GLD and VIX.
        gld_close = data["ohlcv"]["GLD"]["close"][-1] if "GLD" in data["ohlcv"] and len(data["ohlcv"]["GLD"]["close"]) > 0 else None
        vix_close = data["ohlcv"]["VIX"]["close"][-1] if "VIX" in data["ohlcv"] and len(data["ohlcv"]["VIX"]["close"]) > 0 else None

        # Initialize the target allocation.
        allocation_dict = {"GLD": 0}

        if gld_close is not None and vix_close is not None:
            # Check for the VIX closing price to decide on the trading strategy for GLD.
            # A higher VIX usually indicates market volatility; inversely trading GLD based on VIX.
           
            if vix_close > 20:
                # If VIX is high (> 20), it indicates increased market volatility.
                # The strategy opts to short GLD assuming investors will flee to safety (inverse relation).
                allocation_dict["GLD"] = -0.5  # Short GLD with a 50% position of available capital.
            else:
                # In lower volatility (VIX <= 20), the strategy takes a long position,
                # assuming GLD will decrease as investors take on more risk.
                allocation_dict["GLD"] = 0.5  # Long GLD with a 50% position of available capital.

        # Log the strategy decision.
        log("GLD allocation based on VIX: {}".format(allocation_dict["GLD"]))

        return TargetAllocation(allocation_dict)