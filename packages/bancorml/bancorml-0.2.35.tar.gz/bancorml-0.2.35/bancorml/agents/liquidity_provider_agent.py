from .agent_base import AgentBase
# from .random_walk import RandomWalker
import random
import pandas as pd
from bancorml.utils import convert_to_fixedpoint, is_solidity_converted

class LiquidityProviderAgent(AgentBase):
    """ subclass of RandomWalker, which is subclass to Mesa Agent
    """
    name = 'Liquidity Provider Agent'

    def __init__(self,
                 env,
                 model=None,
                 pos=None,
                 moore=None,
                 unique_id=name,
        ):

        # Bancor3 protocol, set at __init__, all LP's have the same protocol in this model
        self.protocol = env
        self.wallet = {
            'block_num': [0]
        }

        if model is not None:
            # init parent class with required parameters
            super().__init__(unique_id, pos, model, moore=moore)


    def deposit(self, tkn, x, block_num=0, fake_wallet=True):

        self.validate(self.protocol.is_solidity)

        if self.protocol.is_solidity:
            x = convert_to_fixedpoint(x)

        if fake_wallet:
            self.handle_fake_wallet(tkn, x, m=1000)
        else:
            if f"bn{tkn}" not in self.wallet:
                self.wallet[f'bn{tkn}'] = [0]

        new_x = self.protocol.deposit(tkn, x, block_num)

        print('new_x', new_x, self.wallet[f"bn{tkn}"][-1])

        for key in self.wallet:

            if (tkn == key) & (tkn == 'BNT'):
                self.wallet[tkn].append(self.wallet[tkn][-1] - x)
                self.wallet[f"v{tkn}"].append(self.wallet[f"v{tkn}"][-1] + new_x)
                self.wallet[f"bn{tkn}"].append(self.wallet[f"bn{tkn}"][-1] + new_x)

            elif (tkn == key) & (tkn != 'BNT'):
                self.wallet[tkn].append(self.wallet[tkn][-1] - x)

                print('new_xxx', new_x, self.wallet[f"bn{tkn}"][-1])
                self.wallet[f"bn{tkn}"].append(self.wallet[f"bn{tkn}"][-1] + new_x)
                print('new_2xxx wallet', self.wallet[f"bn{tkn}"][-1])

            elif key == 'block_num':
                self.wallet[key].append(self.wallet[key][-1])

            if (key != 'block_num') & (self.wallet[key][-1] < 0):
                if not self.protocol.warning_only:
                    raise UserWarning(f'Error. {key} balance cannot be less than zero. {self.wallet[key][-1]}')


    def withdraw(self, tkn, x, block_num=0, fake_wallet=True):
        '''
        Loops over the addresses and discovers a random user with a non-zero balance of a random TKN (TKN).
        (conditional logic removes the blockNo and bnTKN lists from the choice)
        Creates a random number from the TKN balance (x).
        Adds new rows for each address, subtracts x from the appropriate list (i.e. as though the user has transferred it to the vault).
        Calls the AddLiquidity function, and adds the appropriate number of pool tokens to the appropriate list in the addresses dictionary.
        '''

        self.validate(self.protocol.is_solidity)

        if self.protocol.is_solidity:
            x = convert_to_fixedpoint(x)

        if fake_wallet:
            self.handle_fake_wallet(tkn, x, m=0)
        else:
            self.wallet[f'bn{tkn}'] = [0]

        if 'BNT' not in self.wallet:
            self.wallet['BNT'] = [0 for i in range(len(self.wallet[tkn]))]

        tkn_out, bnt_out = self.protocol.withdraw(tkn, x)
        for key in self.wallet:
            if (tkn == key) & (tkn == 'BNT'):
                self.wallet["BNT"].append(self.wallet["BNT"][-1] + tkn_out)
                self.wallet["BNT"].append(self.wallet["BNT"][-1] + bnt_out)
            elif tkn == key:
                self.wallet[tkn].append(self.wallet[tkn][-1] + tkn_out)
                self.wallet["BNT"].append(self.wallet["BNT"][-1] + bnt_out)
            else:
                if len(self.wallet[key]) < len(self.wallet[tkn]):
                    self.wallet[key].append(self.wallet[key][-1])

            if (key != 'block_num') & (self.wallet[key][-1] < 0):
                if not self.protocol.warning_only:
                    raise UserWarning(f'Error. {key} balance cannot be less than zero. {self.wallet[key][-1]}')


        if len(self.wallet['block_num']) < len(self.wallet[tkn]):
            self.wallet['block_num'].append(block_num)
        if len(self.wallet['BNT']) < len(self.wallet[tkn]):
            self.wallet['BNT'].append(self.wallet['BNT'][-1])

    def handle_fake_wallet(self, tkn, x, m):
        if f'bn{tkn}' not in self.wallet:
            self.wallet[tkn]=[x * m for i in range(len(self.wallet['block_num']))]
            self.wallet[f'bn{tkn}']=[0 for i in range(len(self.wallet['block_num']))]
            if tkn == 'BNT':
                self.wallet[f'v{tkn}'] = [0 for i in range(len(self.wallet['block_num']))]

        if 'BNT' not in self.wallet:
            self.wallet['BNT'] = [0 for i in range(len(self.wallet['block_num']))]

    def get_wallet(self, tkn=None, history=False):
        if (tkn is None) & (not history):
            return pd.DataFrame.from_dict(self.wallet).iloc[[-1]]
        elif (tkn is None) and history:
            return pd.DataFrame.from_dict(self.wallet)
        else:
            bntkn_val = pd.DataFrame.from_dict(self.wallet).iloc[[-1]][f'bn{tkn}'].values[0]
            tkn_val = pd.DataFrame.from_dict(self.wallet).iloc[[-1]][tkn].values[0]
            return f'{tkn}={tkn_val}', f'bn{tkn}={bntkn_val}'

    def step(self):
        # move to a cell in my Moore neighborhood
        self.random_move()
