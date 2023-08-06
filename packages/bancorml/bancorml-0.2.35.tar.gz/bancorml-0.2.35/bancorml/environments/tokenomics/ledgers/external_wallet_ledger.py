"""Component that emulates a External Protection Wallet Ledger Ledger."""
from .ledger_base import LedgerBase

class ExternalProtectionWalletLedger(LedgerBase):
    """Component that emulates a External Protection Wallet Ledger Ledger."""
    name = 'External Protection Wallet Ledger'
    def __init__(self):
        super().__init__()
        self._ledger = {'block_num': [0]}

