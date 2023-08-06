from abc import ABC, abstractmethod
from bancorml.utils import convert_to_fixedpoint, is_solidity_converted
from math import floor

class AgentBase(ABC):
    """Base class for all agents."""

    @property
    @classmethod
    @abstractmethod
    def name(cls):
        """Returns string name of this component."""

    def validate(self, is_solidity):
        wallet = self.wallet
        if is_solidity:
            for tkn in wallet:
                if not is_solidity_converted(wallet[tkn][-1], 'AgentBase'):
                    wallet[tkn][-1] = convert_to_fixedpoint(wallet[tkn][-1])

                try: wallet[tkn][-1] = floor(wallet[tkn][-1])
                except: pass

        self.wallet = wallet
        return self

