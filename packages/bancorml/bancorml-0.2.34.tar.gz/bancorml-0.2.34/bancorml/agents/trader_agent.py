from .agent_base import AgentBase
# from .random_walk import RandomWalker
import random
import pandas as pd
from fractions import Fraction
from decimal import *

def Solidity(val):
    return int(Decimal(val) * 10 ** 18)

class TraderAgent(AgentBase):
    """Trader subclass of RandomWalker, which is subclass to Mesa Agent
    """
    name = 'Trader Agent'

    def __init__(self,
                 env,
                 model=None,
                 pos=None,
                 moore=None,
                 unique_id=name
        ):

        # Bancor3 protocol, set at __init__, all LP's have the same protocol in this model
        self.protocol = env

        self.wallet = {
            'block_num': [0]
        }

        if model is not None:
            # init parent class with required parameters
            super().__init__(unique_id, pos, model, moore=moore)


    def swap(self, tkn1, x, tkn2, fake_wallet=True, block_num=0, update_liquidity=False):
        '''
            Loops over the addresses and discovers a random user with a non-zero balance of a random TKN (TKN).
            (conditional logic removes the blockNo and bnTKN lists from the choice)
            Creates a random number from the TKN balance (x).
            Adds new rows for each address, subtracts x from the appropriate list (i.e. as though the user has transferred it to the vault).
            Calls the AddLiquidity function, and adds the appropriate number of pool tokens to the appropriate list in the addresses dictionary.
            '''
        x = Solidity(x)
        if tkn1 not in self.wallet and fake_wallet:
            self.wallet[tkn1]=[x * 1000 for i in range(len(self.wallet['block_num']))]
            self.wallet[tkn2]=[0 for i in range(len(self.wallet['block_num']))]


        elif tkn1 not in self.wallet:
            raise UserWarning(f"{tkn1} not found in agent wallet.")

        for key in self.wallet:
            if key == 'block_num':
                self.wallet[key].append(block_num)
            else:
                self.wallet[key].append(self.wallet[key][-1])

            if tkn1 == key:
                self.wallet[tkn1][-1] -= x
                self.wallet[tkn2][-1] += self.protocol.trade(tkn1, x, tkn2, block_num, update_liquidity)

            if (key != 'block_num') & (self.wallet[key][-1] < 0):
                if not self.protocol.warning_only:
                    raise UserWarning(f'Error. {key} balance cannot be less than zero. {self.wallet[key][-1]}')
                else:
                    f'Warning. {key} balance should not be less than zero. {self.wallet[key][-1]}'

    def get_wallet(self):
        return pd.DataFrame.from_dict(self.wallet)

    def step(self):
        # move to a cell in my Moore neighborhood
        self.random_move()
