"""Base class for all ledgers."""
from abc import ABC, abstractmethod
from bancorml.utils import is_solidity_converted, convert_to_fixedpoint
from decimal import Decimal
from math import floor

class LedgerBase(ABC):
    """Base class for all ledgers."""

    def _validate_ledger(self, ledger, new_state):
        if not isinstance(new_state, ledger):
            raise ValueError(
                f"Invalid type {new_state}. New state must be an instance of {ledger}"
            )

    @property
    def name(cls):
        """Returns string name of this component."""

    @property
    def ledger(self):
        """
        Returns:
            (dict): Dictionary representing the ledger balance
        """
        return self._ledger

    @ledger.setter
    def ledger(self, new_state):
        """
        Args:
            new_state (dict): Dictionary representing the new state of the ledger balance

        Returns:
            (dict): Dictionary representing the updated ledger balance
        """
        self._validate_balance(type(self.ledger), new_state)
        self._ledger = new_state

    @property
    def is_solidity_converted(self):
        """
        Returns:
            (bool): Boolean true if balances have already been converted to solidity.
        """
        return self._is_solidity_converted

    @is_solidity_converted.setter
    def is_solidity_converted(self, new_state):
        """
        Args:
            new_state (dict): Dictionary representing the new state of the ledger balance

        Returns:
            (dict): Dictionary representing the updated ledger balance
        """
        self._validate_balance(type(self.ledger), new_state)
        self._ledger = new_state

    def validate(self, bnt_funding_limit, is_solidity):
        for tkn in self.ledger:
            if self.name in ['Vault Ledger', 'Staking Ledger', 'Vortex Ledger', 'External Protection Wallet Ledger']:
                if tkn not in self.ledger:
                    self.ledger[tkn] = [0]
                if self.ledger[tkn][-1] != 0:
                    if is_solidity:
                        if not is_solidity_converted(self.ledger[tkn][-1]):
                            self.ledger[tkn][-1] = convert_to_fixedpoint(self.ledger[tkn][-1])

                        try:
                            self.ledger[tkn][-1] = floor(self.ledger[tkn][-1])
                        except:
                            pass

            if self.name == 'Available Liquidity Ledger':
                if tkn not in self.ledger:
                    self.ledger[tkn] = {tkn:[0], 'BNT':[0], 'block_num':[0], 'funding_remaining':[bnt_funding_limit]}
                if is_solidity:
                    if not is_solidity_converted(self.ledger[tkn][tkn][-1]):
                        self.ledger[tkn][tkn][-1] = convert_to_fixedpoint(self.ledger[tkn][tkn][-1])
                    if not is_solidity_converted(self.ledger[tkn]['BNT'][-1]):
                        self.ledger[tkn]['BNT'][-1] = convert_to_fixedpoint(self.ledger[tkn]['BNT'][-1])

                    # floor
                    try: self.ledger[tkn][tkn][-1] = floor(self.ledger[tkn][tkn][-1])
                    except: pass

                    try: self.ledger[tkn]['BNT'][-1] = floor(self.ledger[tkn]['BNT'][-1])
                    except: pass
