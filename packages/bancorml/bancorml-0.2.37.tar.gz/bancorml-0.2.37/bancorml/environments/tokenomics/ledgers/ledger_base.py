"""Base class for all ledgers."""
from abc import ABC, abstractmethod
from bancorml.utils import is_solidity_converted, convert_to_fixedpoint
from decimal import Decimal

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

    def validate(self, bnt_funding_limit):
        for tkn in self.ledger:
            if self.name in ['Vault Ledger', 'Staking Ledger', 'Vortex Ledger', 'External Protection Wallet Ledger']:
                if tkn not in self.ledger:
                    self.ledger[tkn] = [0]
                if self.ledger[tkn][-1] != 0:
                    if not is_solidity_converted(self.ledger[tkn][-1]):
                        self.ledger[tkn][-1] = convert_to_fixedpoint(self.ledger[tkn][-1])

            # try:
            #     if self.name == 'Pool Token Supply Ledger':
            #         if f'bn{tkn}_ERC20_contract' not in self.ledger:
            #             self.ledger[f'bn{tkn}_ERC20_contract'] = {'supply':[0], 'block_num':[0]}
            #         if not is_solidity_converted(self.ledger[f'bn{tkn}_ERC20_contract']['supply'][-1]):
            #             self.ledger[f'bn{tkn}_ERC20_contract']['supply'][-1] = convert_to_fixedpoint(self.ledger[f'bn{tkn}_ERC20_contract']['supply'][-1])
            # except:
            #     pass

            if self.name == 'Available Liquidity Ledger':
                if tkn not in self.ledger:
                    self.ledger[tkn] = {tkn:[0], 'BNT':[0], 'block_num':[0], 'funding_remaining':[bnt_funding_limit]}
                if not is_solidity_converted(self.ledger[tkn][tkn][-1]):
                    self.ledger[tkn][tkn][-1] = convert_to_fixedpoint(self.ledger[tkn][tkn][-1])
                if not is_solidity_converted(self.ledger[tkn]['BNT'][-1]):
                    self.ledger[tkn]['BNT'][-1] = convert_to_fixedpoint(self.ledger[tkn]['BNT'][-1])
