from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # SH is the ProShares Short S&P 500 ETF, and SPY represents the S&P 500
        self.asset_to_trade = "SH" 
        self.reference_asset = "SPY"
        self.short_term_sma_length = 1
        self.long_term_sma_length = 10

    @property
    def assets(self):
        # The assets we're interested in (SPY for analysis and SH for trading)
        return [self.reference_asset, self.asset_to_trade]

    @property
    def interval(self):
        # Daily intervals for the moving averages
        return "1day"

    @property
    def data(self):
        # No additional data required beyond default OHLCV data
        return []

    def run(self, data):
        # Calculate short-term and long-term SMAs for SPY
        spy_sma_short = SMA(self.reference_asset, data['ohlcv'], self.short_term_sma_length)
        spy_sma_long = SMA(self.reference_asset, data['ohlcv'], self.long_term_sma_length)

        allocation_pct = 0

        # Ensure we have enough data points for both SMA calculations
        if spy_sma_short is not None and spy_sma_long is not None and len(spy_sma_short) > 0 and len(spy_sma_long) > 0:
            # Detect the SMA crossover indicating a downtrend
            if spy_sma_short[-1] < spy_sma_long[-1]:
                allocation_pct = 1  # Go long on SH
            # In case of uptrend, we choose not to hold the SH ETF
            else:
                allocation_pct = 0  # Neutral or no position in SH

        # Return the target allocation for SH
        return TargetAllocation({self.asset_to_trade: allocation_pct})