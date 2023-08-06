"""Component that emulates a Available Liquidity Ledger."""
from .ledger_base import LedgerBase


class AvailableLiquidityLedger(LedgerBase):
    """Component that emulates a Available Liquidity Ledger."""
    def __init__(self):
        super().__init__()
        self._ledger = {}

