from bancorml.environments.env_base import EnvBase
from bancorml.agents import LiquidityProviderAgent
from fractions import Fraction
from bancorml.utils import convert_to_fixedpoint, is_solidity_converted


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
            spot_prices (dict): Dictionary of tkn:price (str:float) key-values per tkn.
            whitelisted_tokens (list): List of token tickernames indicating whitelist status approval.
            bootstrapped_tokens (list): List of DAOmsig initiated pools/tokens.
            vortex_rates (dict): Dictionary of tkn:rate (str:float) key-values per TKN.
        """

    name = "Bancor3 Environment"
    block_num = 0
    ema = {}

    def __init__(
            self,
            block_num=0,
            alpha=0.2,
            is_solidity=False,
            min_liquidity_threshold=10000,
            exit_fee=.0025,
            cooldown_period=7,
            bnt_funding_limit=100000,
            external_rate_feed={
                "TKN": {'block_num': [0],
                        'rate': [7.50]},
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
                "TKN": 0.01,
                "BNT": 0.01,
                "LINK": 0.01,
                "ETH": 0.01,
                "wBTC": 0.01,
                "DAI": 0.01,
            },
            whitelisted_tokens=['wBTC', 'BNT', 'LINK', 'ETH', 'DAI', 'TKN'],
            bootstrapped_tokens=[],
            exchange_rates={},
            spot_rates={
                "TKN": {'block_num': [0],
                        'rate': [7.50]},
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
            vortex_rates={
                "TKN": 0.2,
                "BNT": 0.2,
                "LINK": 0.2,
                "ETH": 0.2,
                "wBTC": 0.2,
                "DAI": 0.2,
            },
            warning_only=False,
            dao_msig_initialized_pools=[],
            verbose=True,
            **kwargs
    ):

        super().__init__()

        # create a dictionary to assert key equivalence below
        whitelisted_tokens_dic = {}
        for key in whitelisted_tokens:
            whitelisted_tokens_dic[key] = []

        # assert key equivalence with all required dictionaries
        assert whitelisted_tokens_dic.keys() == vortex_rates.keys() == spot_rates.keys() == pool_fees.keys() == external_rate_feed.keys(), 'ERROR: Tokens listed in whitelisted_tokens must also be found in vortex_rates, spot_rates, pool_fees, external_rate_feed \n'                                                                                                                        'You should define each of these during Bancor3() instantiation.'

        # if is_solidity=True, convert values to be solidity (Fixed Point) compatible
        if is_solidity:

            if not isinstance(alpha, Fraction):
                original_alpha = alpha
                alpha = Fraction(alpha).limit_denominator()
                print(f'WARNING: alpha={original_alpha} has been converted to {alpha} \n'
                      f'Manually specify a Fraction type if you do not want automatic conversion.')

            if not isinstance(exit_fee, Fraction):
                original_alpha = exit_fee
                exit_fee = Fraction(exit_fee).limit_denominator()
                print(f'WARNING: exit_fee={original_alpha} has been converted to {exit_fee} \n'
                      f'Manually specify a Fraction type if you do not want automatic conversion.')

            if not is_solidity_converted(min_liquidity_threshold, 'Bancor3 Instantiation'):
                original_min_liquidity_threshold = min_liquidity_threshold
                min_liquidity_threshold = convert_to_fixedpoint(min_liquidity_threshold)
                print(
                    f'WARNING: min_liquidity_threshold={original_min_liquidity_threshold} has been converted to {min_liquidity_threshold} \n'
                    f'Manually specify a valid solidity compatible value (e.g., value * 10 ** 18 ) if you do not want automatic conversion.')

            if not is_solidity_converted(bnt_funding_limit, 'Bancor3 Instantiation'):
                original_bnt_funding_limit = bnt_funding_limit
                bnt_funding_limit = convert_to_fixedpoint(bnt_funding_limit)
                print(
                    f'WARNING: bnt_funding_limit={original_bnt_funding_limit} has been converted to {bnt_funding_limit} \n'
                    f'Manually specify a valid solidity compatible value (e.g., value * 10 ** 18 ) if you do not want automatic conversion.')

            for tkn in whitelisted_tokens:

                if not isinstance(pool_fees[tkn], Fraction):
                    original_pool_fee = pool_fees[tkn]
                    pool_fees[tkn] = Fraction(pool_fees[tkn]).limit_denominator()
                    print(f'WARNING: pool_fees[{tkn}]={original_pool_fee} has been converted to {pool_fees[tkn]} \n'
                          f'Manually specify a Fraction type if you do not want automatic conversion.')

                if not isinstance(vortex_rates[tkn], Fraction):
                    original_vortex_rate = vortex_rates[tkn]
                    vortex_rates[tkn] = Fraction(vortex_rates[tkn]).limit_denominator()
                    print(
                        f'WARNING: vortex_rates[{tkn}]={original_vortex_rate} has been converted to {vortex_rates[tkn]} \n'
                        f'Manually specify a Fraction type if you do not want automatic conversion.')

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

        for tkn in self.available_liquidity.ledger:
            self.available_liquidity.ledger[tkn]['funding_limit'][-1] = bnt_funding_limit

        self.protocol_agent = LiquidityProviderAgent(env=self, unique_id="Bancor Protocol")

    def withdraw(self, tkn, x, block_num, p=0, q=0, r=0, s=0, t=0, u=0):
        """Bancor3 Unstake protocol logic

        Args:
            x (int or float): The precise TKN value of the bnTKN tokens being withdrawn.
            uid (str or int): The agent user id (default=0)
            tkn (str): The abbreviated token name (default=BNT, valid options are as listed on CoinGecko)

        Returns:
            tkn_out (int or float or decimal): The x of TKN to return to the user
            bnt_out (int or float or decimal): The x of BNT to return to the user
        """
        # tkn_last_block_ema = self.ema[tkn]['block_num'][-1]
        # if block_num != tkn_last_block_ema:
        #     self.update_ema(tkn)
        #     self.block_num = block_num

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
                external_wallet_case = self.tokenomics.check_external_wallet_adjustment(a, b, w, t,
                                                                                        self.tokenomics.satisfies_hlim,
                                                                                        self.tokenomics.satisfies_hmax)

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

    def deposit(self, tkn, x, block_num):
        """Main protocol logic to perform staking functionality

        Args:
            tkn (str): The abbreviated token name (default=BNT, valid options are as listed on CoinGecko)
            x (int or float): The precise TKN value of the bnTKN tokens being withdrawn.

        Returns:
            y (int or float or decimal): the number of pool tokens issued to the user.
        """
        x = self.validate_type(x)
        # tkn_last_block_ema = self.ema[tkn]['block_num'][-1]
        # print(tkn_last_block_ema, block_num)
        # if block_num != tkn_last_block_ema:
        #     self.update_ema(tkn)
        #     self.block_num = block_num

        assert tkn in self.whitelisted_tokens, f'The token is not supported in whitelisted_tokens. {self.whitelisted_tokens}'
        if tkn == 'BNT':
            bnbnt_supply = self.pool_token_supply.ledger['bnBNT_ERC20_contract']['supply'][-1]
            staked_bnt = self.staking.ledger['BNT'][-1]
            pool_tokens_issued_to_user = self.tokenomics.get_pool_tokens_issued_to_user(x, bnbnt_supply, staked_bnt)
            self.protocol_agent.wallet["bnBNT"]["bnBNT"].append(self.protocol_agent.wallet['bnBNT']['bnBNT'][-1] - pool_tokens_issued_to_user)
            self.protocol_agent.wallet["bnBNT"]['block_num'].append(self.block_num)
        else:
            pool_tokens_issued_to_user = self.mint_bntkn(tkn, x)
            self.add_to_vault(tkn, x)
            self.add_to_staking_ledger(tkn, x)
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

        tkn1_last_block_ema = self.ema[tkn1]['block_num'][-1]
        if block_num != tkn1_last_block_ema:
            self.update_ema(tkn1)
            self.block_num = block_num

        tkn2_last_block_ema = self.ema[tkn2]['block_num'][-1]
        if block_num != tkn2_last_block_ema:
            self.update_ema(tkn2)
            self.block_num = block_num

        if (tkn1 == 'BNT') or (tkn2 == 'BNT'):

            if tkn1 == 'BNT':
                bnt_in = x
                tkn_in = None
                tkn = tkn2

            elif tkn2 == 'BNT':
                bnt_in = None
                tkn_in = x
                tkn = tkn1

            a = self.available_liquidity.ledger[tkn]['BNT'][-1]
            a = self.validate_type(a)
            b = self.available_liquidity.ledger[tkn][tkn][-1]
            b = self.validate_type(b)
            d = self.pool_fees[tkn]
            d = self.validate_type(d)
            e = self.vortex_rates[tkn]
            e = self.validate_type(e)

            if tkn1 == 'BNT':
                if self.is_solidity:
                    bnt_trading_liquidity, tkn_trading_liquidity, tkn_to_trader, bnt_to_vortex, tkn_to_staking_ledger, crude_tkn_out = self.tokenomics.handle_trade_bnt_to_tkn_extra_steps(a, b, x, e, d, bnt_in, tkn_in, tkn)
                else:
                    raise UserWarning('FloatingPoint not yet working, try fixedpoint')

                if self.is_within_ema_tolerance(tkn) or update_liquidity:
                    self.update_available_liquidity_ledger(tkn2,
                                                           tkn_to_staking_ledger,
                                                           tkn,
                                                           bnt_trading_liquidity,
                                                           tkn_trading_liquidity)

                self.add_to_vault('BNT', x)
                self.remove_from_vault(tkn2, tkn_to_trader)
                self.add_to_staking_ledger(tkn2, tkn_to_staking_ledger)
                self.add_to_vortex_ledger(bnt_to_vortex)
                if self.verbose: print(f'bnt_trading_liquidity={bnt_trading_liquidity}, \n'
                                       f'tkn_trading_liquidity={tkn_trading_liquidity}, \n'
                                       f'tkn_to_trader={tkn_to_trader}, \n'
                                       f'tkn_to_staking_ledger={tkn_to_staking_ledger}, \n'
                                       f'bnt_to_vortex={bnt_to_vortex} \n\n')
                tkn_out = tkn_to_trader

            elif tkn2 == 'BNT':
                if self.is_solidity:
                    bnt_trading_liquidity, tkn_trading_liquidity, bnt_to_trader, bnt_to_vortex, bnt_to_staking_ledger, crude_bnt_out = self.tokenomics.handle_trade_tkn_to_bnt_extra_steps(a, b, x, e, d, bnt_in, tkn_in, tkn)
                else:
                    raise UserWarning('FloatingPoint not yet working, try fixedpoint')

                if self.is_within_ema_tolerance(tkn) or update_liquidity:
                    self.update_available_liquidity_ledger('BNT',
                                                           bnt_to_staking_ledger,
                                                           tkn,
                                                           bnt_trading_liquidity,
                                                           tkn_trading_liquidity)

                self.remove_from_vault('BNT', bnt_to_trader)
                self.add_to_vault(tkn, x)
                self.add_to_staking_ledger('BNT', bnt_to_staking_ledger)
                self.add_to_vortex_ledger(bnt_to_vortex)
                if self.verbose: print(f'bnt_trading_liquidity={bnt_trading_liquidity}, \n'
                                       f'tkn_trading_liquidity={tkn_trading_liquidity}, \n'
                                       f'crude_bnt_out={crude_bnt_out}, \n'
                                       f'bnt_to_staking_ledger={bnt_to_staking_ledger}, \n'
                                       f'bnt_to_vortex={bnt_to_vortex} \n\n')

                # this variable name is returned to user
                tkn_out = bnt_to_trader

        else:
            bnt_out = self.trade(tkn1, x, 'BNT', block_num)
            tkn_out = self.trade('BNT', bnt_out, tkn2, block_num)

        self.check_pool_shutdown(warning_only=self.warning_only)
        for token in [tkn1, tkn2]:
            self.update_spot_rates(token)

        return tkn_out
