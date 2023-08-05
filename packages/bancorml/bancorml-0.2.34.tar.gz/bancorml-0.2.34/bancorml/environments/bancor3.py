from bancorml.environments.env_base import EnvBase
from bancorml.agents import LiquidityProviderAgent
from fractions import Fraction

class Bancor3(EnvBase):
    """Bancor3 Environment.

        Args:
            is_solidity (bool): Toggles between floating-point-signed and fixed-point-unsigned
            min_liquidity_threshold (float): The BancorDAO prescribes a liquidity threshold, denominated in BNT, that represents the minimum available liquidity that must be present before the protocol bootstraps the pool with BNT.
            bnt_funding_limit (int): The BancorDAO determines the available liquidity for trading, through adjustment of the “BNT funding limit” parameter.
            alpha (float): Alpha value in the EMA equation.
            pool_fees (dict): Dictionary of tkn:fee (str:float) key-values per pool.
            cooldown_period (int): The cooldown period in days.
            exit_fee (float): The global exit fee.
            spot_rates (dict): Dictionary of tkn:price (str:float) key-values per tkn.
            whitelisted_tokens (list): List of token tickernames indicating whitelist status approval.
            bootstrapped_tokens (list): List of DAOmsig initiated pools/tokens.
            vortex_rates (dict): Dictionary of tkn:rate (str:float) key-values per TKN.
        """

    name = "Bancor3 Environment"
    block_num = 0
    ema = {
        # 'TKN': {'block_num': [0], 'ema': [0]},
        # 'BNT': {'block_num': [0], 'ema': [0]},
        # 'DAI': {'block_num': [0], 'ema': [0]},
        # 'wBTC': {'block_num': [0], 'ema': [0]},
        # 'ETH': {'block_num': [0], 'ema': [0]},
        # 'LINK': {'block_num': [0], 'ema': [0]}
    }

    def __init__(
            self,
            block_num=0,
            alpha=Fraction(2, 10),
            is_solidity=False,
            min_liquidity_threshold=10000,
            exit_fee=Fraction(2500, 1000000),
            cooldown_period=7,
            bnt_funding_limit=100000,
            external_rate_feed={
                        "TKN": {'block_num': [0],
                                'rate': [Fraction(2.50 / 3.0)]},
                        "BNT": {'block_num': [0],
                                'rate': [2.50]},
                        "LINK": {'block_num': [0],
                                'rate': [15.00]},
                        "ETH": {'block_num': [0],
                                'rate': [2500.00]},
                        "wBTC": {'block_num': [0],
                                'rate': [40000.00]},
                        "DAI": {'block_num': [0],
                                'rate': [1.00]}
            },
            pool_fees={
                "TKN": Fraction(1, 100),
                "BNT": Fraction(1, 100),
                "LINK": Fraction(1, 100),
                "ETH": Fraction(1, 100),
                "wBTC": Fraction(1, 100),
                "DAI": Fraction(1, 100),
            },
            whitelisted_tokens=['wBTC','BNT','LINK','ETH','DAI','TKN'],
            bootstrapped_tokens=[],
            exchange_rates={},
            spot_rates={
                "TKN": {'block_num': [0],
                        'rate': [Fraction(2.50 / 3.0)]},
                "BNT": {'block_num':[0],
                        'rate':[2.50]},
                "LINK": {'block_num':[0],
                        'rate':[15.00]},
                "ETH": {'block_num':[0],
                        'rate':[2500.00]},
                "wBTC": {'block_num':[0],
                        'rate':[40000.00]},
                "DAI": {'block_num': [0],
                         'rate': [1.00]}
            },
            vortex_rates={
                "TKN": Fraction(2, 10),
                "BNT": Fraction(2, 10),
                "LINK": Fraction(2, 10),
                "ETH": Fraction(2, 10),
                "wBTC": Fraction(2, 10),
                "DAI": Fraction(2, 10),
            },
            warning_only=False,
            dao_msig_initialized_pools=[],
            verbose=True,
            **kwargs
    ):

        super().__init__()
        self._ema = Bancor3.ema
        self.set_param(alpha=alpha,
                       warning_only=warning_only,
                       spot_rates=spot_rates,
                       vortex_rates=vortex_rates,
                       block_num=block_num,
                       exchange_rates=exchange_rates,
                       min_liquidity_threshold=min_liquidity_threshold,
                       bnt_funding_limit=bnt_funding_limit,
                       exit_fee=exit_fee,
                       cooldown_period=cooldown_period,
                       pool_fees=pool_fees,
                       bootstrapped_tokens=bootstrapped_tokens,
                       whitelisted_tokens=whitelisted_tokens,
                       external_rate_feed=external_rate_feed,
                       is_solidity=is_solidity,
                       dao_msig_initialized_pools=dao_msig_initialized_pools,
                       verbose=verbose)

        for tkn in self.available_liquidity_ledger:
            self.available_liquidity_ledger[tkn]['funding_limit'][-1] = bnt_funding_limit

        self.protocol_agent = LiquidityProviderAgent(env=self, unique_id="Bancor Protocol")


    def unstake(self, tkn, x, p=0, q=0, r=0, s=0, t=0, u=0):
        """Bancor3 Unstake protocol logic

        Args:
            x (int or float): The precise TKN value of the bnTKN tokens being withdrawn.
            uid (str or int): The agent user id (default=0)
            tkn (str): The abbreviated token name (default=BNT, valid options are as listed on CoinGecko)

        Returns:
            tkn_out (int or float or decimal): The x of TKN to return to the user
            bnt_out (int or float or decimal): The x of BNT to return to the user
        """
        a, b, c, e, m, n, x, w, staked_bnt, bnbnt_supply = self.validate_input_types(tkn, x)

        if tkn == 'BNT':
            exchange_rate = self.tokenomics.handle_division(staked_bnt, bnbnt_supply)
            tkn_out, bnt_out = self.tokenomics.handle_unstake_bnt(x, exchange_rate, self.exit_fee)

        else:

            # check balanced
            self.tokenomics.check_balanced(b, c, e)

            if self.tokenomics.is_balanced:
                case = 'balanced bootstrap surplus'

            else:

                # check surplus
                self.tokenomics.check_surplus(b, c, e, n)

                # check hlim
                self.tokenomics.check_hlim(b, c, e, x)

                # check hmax
                self.tokenomics.check_hmax(b, c, e, m, n, x, self.tokenomics.surplus)

                # check if trading liquidity needs reduced
                self.tokenomics.check_reduce_trading_liquidity(x, b, c, e, n,
                                                               self.tokenomics.surplus,
                                                               self.tokenomics.satisfies_hmax,
                                                               self.tokenomics.satisfies_hlim)

                # check case (e.g. "default surplus", "arbitrage deficit", etc...)
                case = self.check_case(self.tokenomics.surplus,
                                       self.tokenomics.deficit,
                                       self.tokenomics.satisfies_hlim,
                                       self.tokenomics.satisfies_hmax,
                                       self.tokenomics.reduce_trading_liquidity,
                                       a, b, c, e, w)

            if case in ['bootstrap surplus', 'bootstrap surplus (special case)', 'balanced bootstrap surplus']:
                s = self.tokenomics.handle_bootstrap_surplus(x, n)

            elif case == 'bootstrap deficit (special case)':
                s = self.tokenomics.handle_bootstrap_deficit_special_case(c, e, n, x)

            elif case == 'arbitrage surplus':
                p, r, s = self.tokenomics.handle_arbitrage_surplus(x, n, a, b, c, e, m)

            elif case == 'default surplus':
                p, q, r, s = self.tokenomics.handle_default_surplus(x, n, c, a, b)

            elif case == 'arbitrage deficit':
                p, r, s = self.tokenomics.handle_arbitrage_deficit(x, n, a, m, e, b, c)

            elif case == 'bootstrap deficit':
                s, t = self.tokenomics.handle_bootstrap_deficit(x, n, b, c, e, a)

            elif case == 'default deficit':
                p, q, r, s, t = self.tokenomics.handle_default_deficit(a, b, c, e, n, x)

            if tkn in self.external_protection_wallet_ledger:
                external_wallet_case = self.tokenomics.check_external_wallet_adjustment(a, b, w, t, self.tokenomics.satisfies_hlim, self.tokenomics.satisfies_hmax)

                if external_wallet_case == 'external wallet adjustment (1)':
                    t, u = self.tokenomics.handle_external_wallet_adjustment_1(t, b, a)
                    case = case + ' external wallet adjustment (1)'

                elif external_wallet_case == 'external wallet adjustment (2)':
                    t, u = self.tokenomics.handle_external_wallet_adjustment_2(w, t, b, a)
                    case = case + ' external wallet adjustment (2)'

            # update ledger balances based on the current state
            self.update_ledger_balances(tkn, p, q, r, s, t, u, a, b, c, e, m, n, x, w, case)
            tkn_out = s + u
            bnt_out = t

        self.check_pool_shutdown(warning_only=self.warning_only)
        return tkn_out, bnt_out

    def stake(self, tkn, x, block_num):
        """Main protocol logic to perform staking functionality

        Args:
            tkn (str): The abbreviated token name (default=BNT, valid options are as listed on CoinGecko)
            x (int or float): The precise TKN value of the bnTKN tokens being withdrawn.

        Returns:
            y (int or float or decimal): the number of pool tokens issued to the user.
        """
        x = self.validate_type(x)

        if block_num != self.block_num:
            self.update_ema(tkn)
            self.block_num = block_num

        assert tkn in self.whitelisted_tokens, f'The token is not supported in whitelisted_tokens. {self.whitelisted_tokens}'
        if tkn == 'BNT':
            bnbnt_supply = self.pool_token_supply_ledger['bnBNT_ERC20_contract']['supply'][-1]
            staked_bnt = self.staking_ledger['BNT'][-1]
            pool_tokens_issued_to_user = self.tokenomics.get_pool_tokens_issued_to_user(x, bnbnt_supply, staked_bnt)
            update_amt = bnbnt_supply - pool_tokens_issued_to_user
            self.pool_token_supply_ledger["bnBNT_ERC20_contract"]['block_num'].append(self.block_num)
            self.pool_token_supply_ledger["bnBNT_ERC20_contract"]['supply'].append(update_amt)

        else:
            pool_tokens_issued_to_user = self.mint_bntkn(tkn, x)
            self.add_tkn_to_vault(tkn, x)
            self.add_tkn_to_staking_ledger(tkn, x)

            if self.is_within_ema_tolerance(tkn) and (tkn in self.dao_msig_initialized_pools):
                self.add_tkn_to_available_liquidity_ledger(tkn, x)

            self.check_bootstrapped_tokens()

        self.check_pool_shutdown(warning_only=self.warning_only)
        return pool_tokens_issued_to_user

    def trade(self, tkn1, x, tkn2, block_num, update_liquidity=False):
        """Main protocol logic to perform trading functionality.

        Args:
            tkn1 (str): The abbreviated token name being traded-in
            x (int or float): The precise TKN value of tkn1 being traded.
            tkn2 (str): The abbreviated token name being traded-for (i.e., sent back to the user)

        Returns:
            tkn_out (int or float or decimal): the number of pool tokens issued to the user.
        """
        x = self.validate_type(x)

        if block_num != self.block_num:
            self.update_ema(tkn1)
            self.update_ema(tkn2)
            self.block_num = block_num

        if (tkn1=='BNT') or (tkn2=='BNT'):

            if tkn1=='BNT':
                tkn_a = tkn2
                operation = self.tokenomics.handle_trade_bnt_to_tkn

            elif tkn2=='BNT':
                tkn_a = tkn1
                operation = self.tokenomics.handle_trade_tkn_to_bnt

            a = self.available_liquidity_ledger[tkn_a]['BNT'][-1]
            a = self.validate_type(a)
            b = self.available_liquidity_ledger[tkn_a][tkn_a][-1]
            b = self.validate_type(b)
            d = self.pool_fees[tkn_a]
            d = self.validate_type(d)
            e = self.vortex_rates[tkn_a]
            e = self.validate_type(e)

            print(f'a={a}, \n'
                  f'b={b}, \n'
                  f'd={d}, \n'
                  f'e={e}, \n'
                  f'x={x}, \n')
            bnt_trading_liquidity, tkn_trading_liquidity, tkn_out, tkn_fee, vortex_fee = operation(
                a, d, b, x, e)

            if self.is_within_ema_tolerance(tkn_a) or update_liquidity:
                self.update_available_liquidity_ledger(tkn_a, bnt_trading_liquidity, tkn_trading_liquidity)

            self.add_tkn_to_vault(tkn1, x)
            self.remove_tkn_from_vault(tkn2, tkn_out)
            self.add_tkn_to_staking_ledger(tkn2, tkn_fee)
            self.add_tkn_to_vortex_ledger(tkn2, vortex_fee)


            print(f'bnt_trading_liquidity={bnt_trading_liquidity}, \n'
                  f'tkn_trading_liquidity={tkn_trading_liquidity}, \n'
                  f'tkn_out={tkn_out}, \n'
                  f'tkn_fee={tkn_fee}, \n'
                  f'vortex_fee={vortex_fee} \n\n')

        else:

            a1 = self.available_liquidity_ledger[tkn1]['BNT'][-1]
            a1 = self.validate_type(a1)
            b1 = self.available_liquidity_ledger[tkn1][tkn1][-1]
            b1 = self.validate_type(b1)
            d1 = self.pool_fees[tkn1]
            d1 = self.validate_type(d1)

            a2 = self.available_liquidity_ledger[tkn2]['BNT'][-1]
            a2 = self.validate_type(a2)
            b2 = self.available_liquidity_ledger[tkn2][tkn2][-1]
            b2 = self.validate_type(b2)
            d2 = self.pool_fees[tkn2]
            d2 = self.validate_type(d2)

            e = self.vortex_rates[tkn1]
            e = self.validate_type(e)

            bnt_source_trading_liquidity, tkn_source_trading_liquidity, bnt_destination_trading_liquidity, tkn_destination_trading_liquidity, tkn_out, bnt_fee, tkn_fee, vortex_fee = self.tokenomics.handle_trade_tkn_to_tkn(
                a1, d1, b1, a2, d2, b2, x, e)

            if self.is_within_ema_tolerance(tkn1):
                self.update_available_liquidity_ledger(tkn1, bnt_source_trading_liquidity, tkn_source_trading_liquidity)

            if self.is_within_ema_tolerance(tkn2):
                self.update_available_liquidity_ledger(tkn2, bnt_destination_trading_liquidity, tkn_destination_trading_liquidity)

            self.add_tkn_to_vault(tkn1, x)
            self.add_tkn_to_vault(tkn2, -tkn_out)
            self.add_tkn_to_staking_ledger(tkn2, tkn_fee)
            self.add_tkn_to_staking_ledger('BNT', bnt_fee)
            self.add_tkn_to_vortex_ledger(vortex_fee)

            print(f'bnt_source_trading_liquidity={bnt_source_trading_liquidity}, \n',
                  f'tkn_source_trading_liquidity={tkn_source_trading_liquidity}, \n',
                  f'bnt_destination_trading_liquidity={bnt_destination_trading_liquidity}, \n',
                  f'tkn_destination_trading_liquidity={tkn_destination_trading_liquidity}, \n',
                  f'tkn_out={tkn_out}, \n',
                  f'bnt_fee={bnt_fee}, \n',
                  f'tkn_fee={tkn_fee}, \n',
                  f'vortex_fee={vortex_fee} \n')

        self.check_pool_shutdown(warning_only=self.warning_only)
        for token in [tkn1, tkn2]:
            self.update_spot_rates(token)
        return tkn_out

