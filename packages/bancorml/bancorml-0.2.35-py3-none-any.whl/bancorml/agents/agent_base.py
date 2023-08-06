from abc import ABC, abstractmethod
from bancorml.utils import convert_to_fixedpoint, is_solidity_converted

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
        self.wallet = wallet
        return self

