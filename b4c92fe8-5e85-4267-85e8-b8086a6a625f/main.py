from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.technical_indicators import ATR
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["GLD", "SPY"] # GLD represents gold, SPY represents the S&P 500
        self.atr_length = 14 # Standard period for ATR calculation

    @property
    def interval(self):
        return "1day" # Using daily data for analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # No additional data subscription is created as technical indicators data is created from ohlcv directly
        return []

    def run(self, data):
        # Calculate the ATR for SPY to measure volatility
        spy_atr = ATR("SPY", data["ohlcv"], self.atr_length)
        allocation_dict = {"GLD": 0} # Default to no allocation
        
        if not spy_atr:
            log("No ATR data available for SPY. No action taken.")
            return TargetAllocation(allocation_dict)
        
        # Interpret the last ATR value for SPY
        current_spy_atr = spy_atr[-1]

        log(f"Current ATR for SPY: {current_spy_atr}")

        # Strategy logic: If volatility increases, short gold (increase allocation in inverse gold assets or reduce if it's a direct gold asset in this simplistic case)
        # This example strictly sells GLD (to represent going short) as it's simplified without considering actual shorting mechanics or inverse assets
        if current_spy_atr > spy_atr[-2]: # If current ATR is higher than the previous period's ATR, indicating increased volatility
            allocation_dict["GLD"] = -0.5 # Placeholder to represent taking a short position, in real trading, this might involve buying inverse ETFs or using derivatives
            log("Increased volatility detected in SPY. Attempting to short GLD")

        # Return the allocation, where in this simplified example, a negative value indicates a 'short' intent
        return TargetAllocation(allocation_dict)