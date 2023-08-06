"""Base Agent Environment Class."""
import logging
from abc import ABC, abstractmethod
from decimal import Decimal
import numpy as np
import pandas as pd
# from bancorml.environments.observation_space import observation_space
# from evalml.utils.logger import get_logger, log_title, log_subtitle
from tabulate import tabulate

from bancorml.environments.tokenomics.ledgers import VaultLedger, PoolTokenSupplyLedger, ExternalProtectionWalletLedger, \
    StakingLedger, AvailableLiquidityLedger, VortexLedger
from bancorml.utils import FixedPointUnstakeTKN, FloatingPointUnstakeTKN, FixedPointGeneral, FloatingPointGeneral
from bancorml.environments.tokenomics.floating_point_tokenomics import FloatingPointTokenomics
from bancorml.environments.tokenomics.fixed_point_tokenomics import FixedPointTokenomics
from fxpmath import Fxp
from fractions import Fraction
from bancorml.utils import convert_to_fixedpoint, is_solidity_converted
from math import floor

# logger = logging.getLogger(__name__)
from bancorml.utils.schemas import FixedPoint


class EnvBase(ABC):
    """Environment base for multi-agent-oriented system.
    """
    metadata = {'render.modes': []}

    def __init__(
        self,
    ):

        # create a vault
        self.vault = VaultLedger()

        # create a staking ledger
        self.staking = StakingLedger()

        # create a single liquidity pool for the model
        self.pool_token_supply = PoolTokenSupplyLedger()

        # create a external protection wallet for the model
        self.external_protection_wallet = ExternalProtectionWalletLedger()

        # create a ledger to track available liquidity
        self.available_liquidity = AvailableLiquidityLedger()

        # create a ledger for the vortex
        self.vortex = VortexLedger()

        # create a list of all ledgers for easy validation in validate_ledgers() method
        self.ledgers = [self.vault, self.staking, self.pool_token_supply, self.external_protection_wallet, self.available_liquidity, self.vortex]
        
    @property
    def min_liquidity_threshold(self) -> int or float or Decimal:
        """Minimum pool liquidity threshold before the DAOmsig can initiate."""
        return self._min_liquidity_threshold

    @min_liquidity_threshold.setter
    def min_liquidity_threshold(self, updated_min_liquidity_threshold: int or float or Decimal):
        self._min_liquidity_threshold = updated_min_liquidity_threshold

    @property
    def warning_only(self) -> bool:
        """If True then will cause exception and break whenever a negative balance is found."""
        return self._warning_only

    @warning_only.setter
    def warning_only(self, updated_warning_only: bool):
        self._warning_only = updated_warning_only

    @property
    def bnt_funding_limit(self) -> int or float or Decimal:
        """The BancorDAO determines the available liquidity for trading, through adjustment
        of the “BNT funding limit” parameter.
        """
        return self._bnt_funding_limit

    @bnt_funding_limit.setter
    def bnt_funding_limit(self, updated_bnt_funding_limit: int or float or Decimal):
        self._bnt_funding_limit = updated_bnt_funding_limit

    @property
    def alpha(self) -> float or Fraction:
        """EMA calculation alpha setting"""
        return self._alpha

    @alpha.setter
    def alpha(self, updated_alpha: float or Fraction):
        self._alpha = updated_alpha

    @property
    def verbose(self) -> bool:
        """Whether to print system state during processing"""
        return self._verbose

    @verbose.setter
    def verbose(self, updated_verbose: bool):
        self._verbose = updated_verbose

    @property
    def whitelisted_tokens(self) -> list:
        """List of approved tokens allowed on Bancor v3"""
        return self._whitelisted_tokens

    @whitelisted_tokens.setter
    def whitelisted_tokens(self, updated_whitelist: list):
        self._whitelisted_tokens = updated_whitelist

    @property
    def dao_msig_initialized_pools(self) -> list:
        """List of DAOmsig initialized pools on Bancor v3"""
        return self._dao_msig_initialized_pools

    @dao_msig_initialized_pools.setter
    def dao_msig_initialized_pools(self, updated_dao_msig_initialized_pools: list):
        self._dao_msig_initialized_pools = updated_dao_msig_initialized_pools

    @property
    def external_rate_feed(self) -> dict:
        """List of approved tokens allowed on Bancor v3"""
        return self._external_rate_feed

    @external_rate_feed.setter
    def external_rate_feed(self, updated_external_rate_feed: dict):
        self._external_rate_feed = updated_external_rate_feed

    @property
    def bootstrapped_tokens(self) -> list:
        """List of whitelisted tkn pools on Bancor v3 which meet the minimum pool liquidity threshold"""
        return self._bootstrapped_tokens

    @bootstrapped_tokens.setter
    def bootstrapped_tokens(self, updated_bootstrapped_tokens: list):
        self._bootstrapped_tokens = updated_bootstrapped_tokens

    @property
    def vortex_rates(self) -> dict:
        """The Bancor Vortex accrues value from its share of the revenues is used to buy and burn vBNT to provide IL protection."""
        return self._vortex_rates

    @vortex_rates.setter
    def vortex_rates(self, updated_vortex_rates: dict):
        self._vortex_rates = updated_vortex_rates

    @property
    def pool_fees(self) -> dict:
        """Protocol revenue (i.e. the pool fees, or the commissions paid by traders) is distributed to users by increasing the balance of the staking ledger, equal to the value captured."""
        return self._pool_fees

    @pool_fees.setter
    def pool_fees(self, updated_pool_fees: dict):
        self._pool_fees = updated_pool_fees

    @property
    def exit_fee(self) -> Decimal or Fraction:
        """
        As a final circumspection against bad behavior,
        exit fees are introduced into the Bancor ecosystem for the first time.
        The exit fee is designed to temper the profit motive of the imagined exploit vector.
        """
        return self._exit_fee

    @exit_fee.setter
    def exit_fee(self, updated_exit_fee: Decimal or Fraction):
        self._exit_fee = updated_exit_fee

    @property
    def exchange_rates(self) -> dict:
        """BNT to tkn exchange rate, effectively swapping out an equal quantity of BNT value for tkn value, until there is no tkn remaining."""
        return self._exchange_rates

    @exchange_rates.setter
    def exchange_rates(self, updated_exchange_rates: dict):
        self._exchange_rates = updated_exchange_rates

    @property
    def ema(self) -> dict:
        """Exponential Moving Average (EMA) used to test spot price tolerance."""
        return self._ema

    @ema.setter
    def ema(self, updated_ema: dict):
        self._ema = updated_ema

    @property
    def spot_rates(self) -> dict:
        """Current system state spot rates. Setting these will cause an auto-update"""
        return self._spot_rates

    @spot_rates.setter
    def spot_rates(self, updated_spot_rates: dict):
        self._spot_rates = updated_spot_rates

    @property
    def custom_name(self):
        """Custom name of the env."""
        return self._custom_name

    @property
    def name(self):
        """Name of the env."""
        return self.custom_name or self.summary

    def set_param(self, is_solidity=None,
                        block_num=None,
                        min_liquidity_threshold=None,
                        bnt_funding_limit=None,
                        alpha=None,
                        pool_fees=None,
                        cooldown_period=None,
                        exit_fee=None,
                        spot_rates=None,
                        whitelisted_tokens=None,
                        bootstrapped_tokens=None,
                        exchange_rates=None,
                        external_rate_feed=None,
                        vortex_rates=None,
                        dao_msig_initialized_pools=None,
                        warning_only=None,
                        verbose=None
                  ):
        """Allows user to set the specified system parameters.

        Args:
            is_solidity (bool): Toggles between floating-point-signed and fixed-point-unsigned
            min_liquidity_threshold (float): The BancorDAO prescribes a liquidity threshold, denominated in BNT, that represents the minimum available liquidity that must be present before the protocol bootstraps the pool with BNT.
            bnt_funding_remaining (int): The BancorDAO determines the available liquidity for trading, through adjustment of the “BNT funding limit” parameter.
            alpha (float): Alpha value in the EMA equation.
            pool_fees (dict): Dictionary of tkn:fee (str:float) key-values per pool.
            cooldown_period (int): The cooldown period in days.
            exit_fee (float): The global exit fee.
            spot_rates (dict): Dictionary of tkn:price (str:float) key-values per tkn.
            whitelisted_tokens (list): List of token tickernames indicating whitelist status approval.
            bootstrapped_tokens (list): List of DAOmsig initiated pools/tokens.
            vortex_rates (dict): Dictionary of tkn:rate (str:float) key-values per tkn.

        Returns:
            self
        """
        if block_num is not None:
            self.block_num = block_num
        if is_solidity is not None:
            self.is_solidity = is_solidity
            self.tokenomics = FixedPointTokenomics() if is_solidity else FloatingPointTokenomics()
        if verbose is not None:
            self.verbose = verbose
        if exchange_rates is not None:
            self.exchange_rates = exchange_rates
        if min_liquidity_threshold is not None:
            self.min_liquidity_threshold = min_liquidity_threshold
        if bnt_funding_limit is not None:
            self.bnt_funding_limit = bnt_funding_limit
        if alpha is not None:
            self.alpha = alpha
        if warning_only is not None:
            self.warning_only = warning_only
        if cooldown_period is not None:
            self.cooldown_period = cooldown_period
        if pool_fees is not None:
            self.pool_fees = pool_fees
        if exit_fee is not None:
            self.exit_fee = exit_fee
        if whitelisted_tokens is not None:
            self.set_whitelisted_tokens(whitelisted_tokens)
        if vortex_rates is not None:
            self.vortex_rates = vortex_rates
        if external_rate_feed is not None:
            self.external_rate_feed = external_rate_feed
        if bootstrapped_tokens is not None:
            self.bootstrapped_tokens = bootstrapped_tokens
        if dao_msig_initialized_pools is not None:
            self.dao_msig_initialized_pools = dao_msig_initialized_pools
        if spot_rates is not None:
            self.spot_rates = spot_rates
        self.update_exchange_rates()
        self.init_ema()
        
    def validate_ledgers(self):
        for ledger in self.ledgers:
            try: ledger.validate(self.bnt_funding_limit)
            except: raise UserWarning(f'ERROR: Could not validate {ledger.name}')

    def init_tokens(self, add_tkns=[]):
        whitelisted_tokens = self.whitelisted_tokens
        external_rate_feed = self.external_rate_feed
        pool_fees = self.pool_fees
        vortex_rates = self.vortex_rates
        spot_rates = self.spot_rates
        ema = self.ema
        for tkn in add_tkns:
            if tkn not in whitelisted_tokens:
                whitelisted_tokens.append(tkn)
        for tkn in whitelisted_tokens:
            if tkn not in external_rate_feed:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to external_rate_feed at 1 USD \n'
                          f'You can update this with the .update_external_price(tkn, external_price) method. \n')
                external_rate_feed[tkn] =  {'block_num': [self.block_num], 'rate': [1.00]}
            if tkn not in pool_fees:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to pool_fees at {Fraction(1, 100) if self.is_solidity else 0.01} \n'
                          f'You can update this with the .update_pool_fee(tkn, pool_fee) method. \n')
                pool_fees[tkn] = Fraction(1, 100) if self.is_solidity else 0.01
            if tkn not in vortex_rates:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to vortex_rates at {Fraction(2, 10) if self.is_solidity else 0.2} \n'
                          f'You can update this with the .update_vortex_rate(tkn, vortex_rate) method. \n')
                vortex_rates[tkn] = Fraction(2, 10) if self.is_solidity else 0.2
            if tkn not in spot_rates:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to spot_rates at $1 USD \n'
                          f'You can update this with the .update_spot_price(tkn, rate) method. \n')
                spot_rates[tkn] = {'block_num': [self.block_num],'rate': [1]}
            if tkn not in self.vault.ledger:
                self.vault.ledger[tkn] = [0]
            if f"bn{tkn}_ERC20_contract" not in self.pool_token_supply.ledger:
                self.pool_token_supply.ledger[f"bn{tkn}_ERC20_contract"] = {'block_num': [0], 'supply': [0]}
            if tkn not in self.staking.ledger:
                self.staking.ledger[tkn] = [0]
            if tkn not in self.external_protection_wallet.ledger:
                self.external_protection_wallet.ledger[tkn] = [0]
            if tkn not in self.available_liquidity.ledger:
                self.available_liquidity.ledger[tkn] = {'block_num': [self.block_num],'funding_remaining': [
                    self.bnt_funding_limit],'BNT': [0],tkn: [0]}
            self.update_exchange_rates()
            if tkn not in ema:
                if self.verbose:
                    print(
                        f'WARNING: {tkn} was added to ema at the current exchange rate of {self.exchange_rates[tkn]} \n'
                        f'You can update this with the .update_ema(tkn, ema_value) method. \n')
                ema[tkn] = {'block_num': [self.block_num],
                            'ema': [self.exchange_rates[tkn]]}
        self.ema = ema
        self.whitelisted_tokens = whitelisted_tokens
        self.spot_rates = spot_rates
        self.external_rate_feed = external_rate_feed
        self.vortex_rates = vortex_rates
        self.pool_fees = pool_fees

    def init_ema(self):
        ema = self.ema
        for tkn in self.spot_rates:
            if tkn in ema and tkn != 'BNT':
                ema[tkn]['block_num'] = [self.block_num]
                ema[tkn]['ema'] = [self.exchange_rates[tkn]]
        self.ema = ema

    def get_available_liquidity(self, tkn):
        """Gets the available trading liquidity ledger.

        Args:
            tkn (str): Tickername of the token of interest.
        Returns:
            (pd.DataFrame): DataFrame of available_liquidity.ledger logging.
        """
        return pd.DataFrame.from_dict(self.available_liquidity.ledger[tkn])

    def get_vortex(self):
        """Gets the vortex ledger.

        Returns:
            (pd.DataFrame): DataFrame of vortex logging.
        """
        return pd.DataFrame.from_dict(self.vortex.ledger)

    def get_vault(self):
        """Gets the vault ledger.

        Returns:
            (pd.DataFrame): DataFrame of vault ledger logging.
        """
        return pd.DataFrame.from_dict(self.vault.ledger)

    def get_staking(self):
        """Gets the staking ledger.

        Returns:
            (pd.DataFrame): DataFrame of staking ledger logging.
        """
        return pd.DataFrame.from_dict(self.staking.ledger)

    def get_pool_token_supply(self, tkn):
        """Gets the pool token supply ledger.

        Args:
            tkn (str): Tickername of the token of interest.
        Returns:
            (pd.DataFrame): DataFrame of pool token supply ledger logging.
        """
        return pd.DataFrame.from_dict(self.pool_token_supply.ledger[f'bn{tkn}_ERC20_contract'])

    def update_spot_rates(self, tkn):
        """Updates the internal spot price as determined by the trading liquidity balances of the pool

        Args:
            tkn (str): The value of BNT to add to the vortex
        Returns:
            self
        """
        bnt_over_tkn_rate = self.get_bnt_over_tkn_internal_rate(tkn)
        spot_rates = self.spot_rates
        spot_rates[tkn]['block_num'].append(self.block_num)
        spot_rates[tkn]['rate'].append(bnt_over_tkn_rate)
        self.spot_rates = spot_rates

    def set_whitelisted_tokens(self, whitelisted_tokens, bootstrap_tokens=True):
        """Check if the spot rate is outside of the EMA tolerance. No changes are made to the pool depth if outside limits.

        Args:
            whitelisted_tokens (list): The tickername of the token.
            bootstrap_tokens (bool): If true, automatically initializes all whitelisted tokens and adds them to the bootstrapped_tokens list.
        Returns:
            bntkn_value (int or float or decimal): value of a single bntkn pool token.
        """
        self.whitelisted_tokens = whitelisted_tokens
        if bootstrap_tokens:
            self.init_pool(self.whitelisted_tokens)

    def init_pool(self, tkns):
        """Initializes a new pool in the respective ledgers but does not perform the DAOmsig initialization which allows trading.

        Args:
            tkns (list): List of tickernames of the tokens to be initialized.
        Returns:
            self
        """
        for tkn in tkns:
            self.vault.ledger[tkn] = [0]
            self.pool_token_supply.ledger[f"bn{tkn}_ERC20_contract"] = {'block_num': [0], 'supply': [0]}
            self.staking.ledger[tkn] = [0]
            self.external_protection_wallet.ledger[tkn] = [0]

    def validate_type(self, val, src=None):
        """Validates input data types using pydantic type setting. See utils/schema.py for details

        Args:
            val (int or float or decimal): The numerical value to be type checked

        Returns:
            val (int or float or decimal): the validated type-checked value
        """
        if self.is_solidity:
            if not isinstance(val, Fraction):
                if not is_solidity_converted(val, f'validate_type {src}'):
                    val = convert_to_fixedpoint(val)
        else:
            if not isinstance(val, Fraction):
                val = Decimal(val)
            else:
                val = Decimal(float(val))
        return val

    def mint_bntkn(self, tkn, x=None, bnt=None):
        """Adds tkn to the available liquidity ledger.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add. (default=None)
            bnt (int or float or decimal): The value of bnt liquidity to add. (default=None)

        Returns:
            y (int): The number of pool tokens issued to the user.
        """

        pool_token_value = self.validate_type(self.get_pool_token_value(tkn))
        x = self.validate_type(x)
        y = self.tokenomics.handle_multiplication(x, pool_token_value)

        for contract in self.pool_token_supply.ledger:
            self.pool_token_supply.ledger[contract]['block_num'].append(self.block_num)

            if contract == f'bn{tkn}_ERC20_contract':
                new_val = self.tokenomics.handle_addition(self.pool_token_supply.ledger[contract]['supply'][-1], y)
                self.pool_token_supply.ledger[contract]['supply'].append(new_val)

            else:
                self.pool_token_supply.ledger[contract]['supply'].append(self.pool_token_supply.ledger[contract]['supply'][-1])
        return (y)

    def check_pool_shutdown(self, warning_only=True):
        """Checks if any whitelisted tokens meet the pool-shutdown criterea, and resets the DOAmsig state if yes.

        Returns:
            self
        """
        for tkn in self.whitelisted_tokens:

            available_liquidity_bnt = self.available_liquidity.ledger[tkn]['BNT'][-1]
            if available_liquidity_bnt < self.min_liquidity_threshold and (tkn in self.dao_msig_initialized_pools):
                if self.verbose:
                    print(
                        f"WARNING POOL SHUTDOWN!!! \n",
                        f"warning_only={warning_only} \n",
                        f"pool={tkn} \n",
                        f"tkn Liquidity <= Minimum Pool Liquidity, if not warning_only then will reset pool to pre-DAOmsig state"
                    )

    def check_bootstrapped_tokens(self):
        """Checks if new tokens have been whitelisted and whether or not those token meet the min_liquidity_threshold,
        ensures token are added to the bootstrapped_tokens list if any whitelisted tokens meet this criterea

        Returns:
            self
        """

        bootstrapped_tokens = self.bootstrapped_tokens
        for tkn in self.whitelisted_tokens:
            if tkn != 'BNT':
                tkn_vault = self.validate_type(self.vault.ledger[tkn][-1])
                exchange_rate = self.validate_type(self.exchange_rates[tkn])
                tkn_val = self.tokenomics.handle_multiplication(tkn_vault, exchange_rate)
                if (tkn_val >= self.min_liquidity_threshold) & (tkn not in bootstrapped_tokens) & (tkn in self.dao_msig_initialized_pools):
                    bootstrapped_tokens.append(tkn)
        self.bootstrapped_tokens = bootstrapped_tokens

    def check_case(self,
                   is_surplus,
                   is_deficit,
                   satisfies_hlim,
                   satisfies_hmax,
                   reduce_trading_liquidity,
                   a, b, c, e, w):
        """Defines which BIP15 logical case applies to the current action.

        Args:
            is_surplus (bool): Whether the system is in a surplus state.
            is_deficit (bool): Whether the system is in a deficit state.
            satisfies_hlim (bool): Whether the system passes the hlim test.
            satisfies_hmax (bool): Whether the system passes the hmax test.
            reduce_trading_liquidity (bool): Whether the system needs to reduce the available trading liquidity.
            a (int or float or decimal): the BNT balance of the trading liquidity, as judged from the spot rate.
            b (int or float or decimal): the tkn balance of the trading liquidity, as judged from the spot rate.
            c (int or float or decimal): the difference between the tkn balance of the vault, and the tkn trading liquidity.
            e (int or float or decimal): the tkn balance of the staking ledger.
            w (int or float or decimal): the tkn balance of the external protection wallet.

        Returns:
            case (str): the human readable logical-case name
        """
        if is_surplus & (a == 0 and b == 0):
            case = 'bootstrap surplus (special case)'

        elif is_deficit & (a == 0 and b == 0):
            case = 'bootstrap deficit (special case)'

        elif is_surplus & (satisfies_hlim and satisfies_hmax) & ((b + c) > e):
            case = 'arbitrage surplus'

        elif is_surplus & (not satisfies_hlim or not satisfies_hmax) & (not reduce_trading_liquidity):
            case = 'default surplus'

        elif is_surplus & (not satisfies_hlim or not satisfies_hmax) & reduce_trading_liquidity:
            case = 'bootstrap surplus'

        elif is_deficit & (satisfies_hlim and satisfies_hmax):
            case = 'arbitrage deficit'

        elif is_deficit & (not satisfies_hlim or not satisfies_hmax) & (
                not reduce_trading_liquidity):
            case = 'default deficit'

        elif is_deficit & (not satisfies_hlim or not satisfies_hmax) & reduce_trading_liquidity:
            case = 'bootstrap deficit'

        return case

    def validate_input_types(self, tkn, x):
        """Validates input data types using pydantic type setting. See utils/schema.py for details

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add. (default=None)

        Returns:
            a (int or float or decimal): the BNT balance of the trading liquidity, as judged from the spot rate.
            b (int or float or decimal): the tkn balance of the trading liquidity, as judged from the spot rate.
            c (int or float or decimal): the difference between the tkn balance of the vault, and the tkn trading liquidity.
            e (int or float or decimal): the tkn balance of the staking ledger.
            w (int or float or decimal): the tkn balance of the external protection wallet.
            m (float or decimal): the global system exit fee
            n (float or decimal): the per pool trading fee
            x (int or float or decimal): the tkn or BNT amount involved in the current action
        """
        ema = self.validate_type(self.ema[tkn]['ema'][-1])
        a = self.validate_type(self.available_liquidity.ledger[tkn]['BNT'][-1])
        b = self.tokenomics.handle_division(a, ema)
        e = self.validate_type(self.staking.ledger[tkn][-1])
        staked_bnt = self.validate_type(self.staking.ledger['BNT'][-1])
        bnbnt_supply = self.validate_type(self.pool_token_supply.ledger['bnBNT_ERC20_contract']['supply'][-1])
        w = self.validate_type(self.external_protection_wallet.ledger[tkn][-1])
        c = self.validate_type(self.vault.ledger[tkn][-1] - b)
        n = self.validate_type(self.exit_fee)
        m = self.validate_type(self.pool_fees[tkn])
        return a, b, c, e, m, n, x, w, staked_bnt, bnbnt_supply

    def update_available_liquidity_ledger(self, tkn2, tkn_fee, tkn, bnt_trading_liquidity, tkn_trading_liquidity):
        """Updates available liquidity for swaps

        Args:
            tkn (str): The tickername of the token.
            bnt_trading_liquidity (int or float or decimal): The value of liquidity to add to bnt.
            tkn_trading_liquidity (int or float or decimal): The value of liquidity to add to tkn.

        Returns:
            self
        """
        # update tkn liquidity
        funding_remaining = self.available_liquidity.ledger[tkn]['funding_remaining'][-1]
        self.available_liquidity.ledger[tkn]['BNT'].append(bnt_trading_liquidity)
        self.available_liquidity.ledger[tkn][tkn].append(tkn_trading_liquidity)
        if tkn2 == 'BNT':
            self.available_liquidity.ledger[tkn]['funding_remaining'].append(funding_remaining - tkn_fee)
        else:
            self.available_liquidity.ledger[tkn]['funding_remaining'].append(funding_remaining)
        self.available_liquidity.ledger[tkn]['block_num'].append(self.block_num)

    def update_ledger_balances(self, tkn, p, q, r, s, t, u, a, b, c, e, m, n, x, w, case, event_type='unstake_tkn'):
        """Updates the ledger balances for withdraw actions

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add. (default=None)
            a (int or float or decimal): the BNT balance of the trading liquidity, as judged from the spot rate.
            b (int or float or decimal): the tkn balance of the trading liquidity, as judged from the spot rate.
            c (int or float or decimal): the difference between the tkn balance of the vault, and the tkn trading liquidity.
            e (int or float or decimal): the tkn balance of the staking ledger.
            w (int or float or decimal): the tkn balance of the external protection wallet.

        Returns:
            self
        """
        p = self.validate_type(p)
        r = self.validate_type(r)
        s = self.validate_type(s)
        x = self.validate_type(x)
        q = self.validate_type(q)
        u = self.validate_type(u)
        tkn_bnt_liquidity = self.validate_type(self.available_liquidity.ledger[tkn]['BNT'][-1])
        tkn_tkn_liquidity = self.validate_type(self.available_liquidity.ledger[tkn][tkn][-1])
        bnt_staking = self.validate_type(self.staking.ledger['BNT'][-1])
        tkn_staking = self.validate_type(self.staking.ledger[tkn][-1])
        tkn_vault = self.validate_type(self.vault.ledger[tkn][-1])
        tkn_external_protection = self.validate_type(self.external_protection_wallet.ledger[tkn][-1])

        if event_type == 'unstake_tkn':

            # handle surplus signs
            if (case != 'default surplus') & self.tokenomics.surplus:
                tknbnt = self.tokenomics.handle_subtraction(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_addition(tkn_tkn_liquidity, r)
                self.available_liquidity.ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity.ledger[tkn][tkn][-1] = tkntkn

            elif self.tokenomics.surplus:
                tknbnt = self.tokenomics.handle_subtraction(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_subtraction(tkn_tkn_liquidity, r)
                self.available_liquidity.ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity.ledger[tkn][tkn][-1] = tkntkn

            # handle deficit signs
            elif (self.tokenomics.deficit) & ('ep2' in case):
                tknbnt = self.tokenomics.handle_subtraction(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_subtraction(tkn_tkn_liquidity, r)
                self.available_liquidity.ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity.ledger[tkn][tkn][-1] = tkntkn

            elif self.tokenomics.deficit:
                tknbnt = self.tokenomics.handle_addition(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_subtraction(tkn_tkn_liquidity, r)
                self.available_liquidity.ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity.ledger[tkn][tkn][-1] = tkntkn

            staking_bnt = self.tokenomics.handle_subtraction(bnt_staking, q)
            self.staking.ledger['BNT'][-1] = staking_bnt

            staking_tkn = self.tokenomics.handle_subtraction(tkn_staking, x)
            self.staking.ledger[tkn][-1] = staking_tkn

            vault_tkn = self.tokenomics.handle_subtraction(tkn_vault, s)
            self.vault.ledger[tkn][-1] = vault_tkn

            self.mint_bntkn(tkn, bnt=t)

            external_protection_wallet_tkn = self.tokenomics.handle_subtraction(tkn_external_protection, u)
            self.external_protection_wallet.ledger[tkn][-1] = external_protection_wallet_tkn

        eq_case = self.tokenomics.reduce_trading_liquidity
        if self.tokenomics.surplus: eq = 'x(1-n) <= c'
        else: eq = 'x(1-n)(b+c)/e <= c'
        if self.tokenomics.satisfies_hlim and self.tokenomics.satisfies_hmax:
            eq_entry = ''
        else:
            eq_entry = f'{eq}:{eq_case}'

        self.describe_withdrawal = {
            'inputs': [
                f"a:{a}",
                f"b:{b}",
                f"c:{c}",
                f"e:{e}",
                f"m:{m}",
                f"n:{n}",
                f"x:{x}",
            ],
            'tests': [
                f'hlim:{self.tokenomics.hlim}',
                f'hmax:{self.tokenomics.hmax}',
                f'is_surplus:{self.tokenomics.surplus}',
                f'case={case}',
                f'satisfies_hlim:{self.tokenomics.satisfies_hlim}',
                f'satisfies_hmax:{self.tokenomics.satisfies_hmax}',
                eq_entry,
            ],
            'outputs': [
                f"p:{p}",
                f"q:{q}",
                f"r:{r}",
                f"s:{s}",
                f"t:{t}",
                f"u:{u}",
                '',
            ],
            'trading_liquidity': [
                f"BNT:{self.available_liquidity.ledger[tkn]['BNT'][-1]}",
                f"{tkn}:{self.available_liquidity.ledger[tkn][tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
            ],
            'vault': [
                f"{tkn}:{self.vault.ledger[tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            'staking_ledger': [
                f"{tkn}:{self.staking.ledger[tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            'external_protection_ledger': [
                f"{tkn}:{self.external_protection_wallet.ledger[tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
                '',
            ]
        }
        return self

    def describe(self, withdraw=False, return_tabular=False):
        """Outputs details of the system state, including ledgers & parameters, or the case of withdrawal, inputs, outputs, &etc.
        Args:
            return_dict (bool): If True, return dictionary of information about system state. Defaults to False.
        Returns:
            pd.DataFrame: DataFrame of system state
        """
        if withdraw:
            logger = self.describe_withdrawal
        else:
            logger = {'trading_liquidity':[],
                      'vault': [],
                      'staking_ledger': [],
                      'pool_token_supply': [],
                      'vortex': []
            }
            for tkn in self.available_liquidity.ledger:
                if tkn != 'BNT':
                    logger['trading_liquidity'].append(f"{tkn}:{self.available_liquidity.ledger[tkn][tkn][-1]} - BNT:{self.available_liquidity.ledger[tkn]['BNT'][-1]}")
            for tkn in self.available_liquidity.ledger:
                logger['vault'].append(
                    f"{tkn}:{self.vault.ledger[tkn][-1]}")
            for tkn in self.staking.ledger:
                if tkn != 'block_num':
                    logger['staking_ledger'].append(
                    f"{tkn}:{self.staking.ledger[tkn][-1]}")
            for tkn in self.pool_token_supply.ledger:
                logger['pool_token_supply'].append(
                    f"{tkn.replace('_ERC20_contract','')}:{self.pool_token_supply.ledger[tkn]['supply'][-1]}")
            logger['vortex'].append(f"Balance:{self.vortex.ledger['BNT'][-1]}")
            max_rows = max([len(logger['pool_token_supply']),
                            len(logger['staking_ledger']),
                            len(logger['vault']),
                            len(logger['trading_liquidity'])])
            for key in logger:
                for row in range(max_rows - len(logger[key])):
                    logger[key].append('')
            for ledger in logger:
                logger[ledger].sort()
        df = pd.DataFrame(logger)
        if return_tabular:
            return tabulate(df, headers='keys', tablefmt='psql', floatfmt=".3f")
        else: 
            return df

    def update_exchange_rates(self):
        #TODO oracle exchange rates
        exchange_rates = self.exchange_rates
        bnt_price = self.spot_rates['BNT']['rate'][-1]
        for tkn in self.spot_rates:
            tkn_price = self.spot_rates[tkn]['rate'][-1]
            exchange_rates[tkn] = self.tokenomics.handle_division(tkn_price, bnt_price)
        self.exchange_rates = exchange_rates

    def get_pool_token_value(self, tkn):
        """Get pool token value in bntkn/tkn. If this is the first issuance, the pool token value is forced to 1.

        Args:
            x (int or float or decimal): The value of BNT to add to the vortex
        Returns:
            bntkn_value (int or float or decimal): value of a single bntkn pool token.
        """
        staked_amount = self.staking.ledger[tkn][-1]
        bntkn_supply = self.pool_token_supply.ledger[f'bn{tkn}_ERC20_contract']['supply'][-1]
        if staked_amount > 0 and bntkn_supply > 0:
            bntkn_value = self.tokenomics.handle_division(bntkn_supply, staked_amount)
        else:
            bntkn_value = Fraction(1)
        return bntkn_value

    def get_bnt_over_tkn_internal_rate(self, tkn):
        """Gets the spot rate in units of BNT/tkn as determined by the trading liquidity balances of the pool

        Args:
            tkn (str): The value of BNT to add to the vortex
        Returns:
            bnt_over_tkn_rate (int or float or decimal): spot rate in units of BNT/tkn
        """
        if tkn == 'BNT':
            bnt_over_tkn_rate = self.exchange_rates[tkn]
        else:
            tkn_amt = self.available_liquidity.ledger[tkn][tkn][-1]
            BNT_amt = self.available_liquidity.ledger[tkn]['BNT'][-1]
            if tkn_amt > 0 and BNT_amt > 0:
                bnt_over_tkn_rate = self.tokenomics.handle_division(BNT_amt, tkn_amt)
            else:
                bnt_over_tkn_rate = self.exchange_rates[tkn]
        return bnt_over_tkn_rate
    
    def get_tkn_over_bnt_internal_rate(self, tkn) -> int or float or Decimal or Fraction:
        """Gets the spot rate in units of BNT/tkn as determined by the trading liquidity balances of the pool

        Args:
            tkn (str): The value of BNT to add to the vortex
        Returns:
            bnt_over_tkn_rate (int or float or decimal): spot rate in units of BNT/tkn
        """
        tkn_amt = self.available_liquidity.ledger[tkn][tkn][-1]
        BNT_amt = self.available_liquidity.ledger[tkn]['BNT'][-1]
        if tkn_amt > 0 and BNT_amt > 0:
            tkn_over_bnt_rate = self.tokenomics.handle_division(tkn_amt, BNT_amt)
        else:
            tkn_over_bnt_rate = 1
        return tkn_over_bnt_rate
    
    def get_bnt_over_tkn_external_rate(self, tkn) -> int or float or Decimal or Fraction:
        """Gets the rate in units of tkn/BNT as determined by the external price feed

        Args:
            tkn (str): The token tickername.
        Returns:
            tkn_over_bnt_rate (int or float or decimal): bnt rate in units of tkn/BNT
        """
        bnt_price = self.validate_type(self.external_rate_feed['BNT']['rate'][-1])
        tkn_price = self.validate_type(self.external_rate_feed[tkn]['rate'][-1])
        bnt_over_tkn_rate = self.tokenomics.handle_division(bnt_price, tkn_price)
        return bnt_over_tkn_rate

    def get_bnbnt_rate(self, bnbnt_supply, bnt_staking):
        if bnbnt_supply > 0 and bnt_staking > 0:
            bnbnt_rate = self.tokenomics.handle_division(bnbnt_supply, bnt_staking)
        else:
            bnbnt_rate = 1
        return bnbnt_rate

    def dao_msig_initialize_pools(self, force=False, multiplier=2):
        """Command to initialize the pools in simulation of DAOmsig actions.

        Returns:
            self
        """
        dao_msig_initialized_pools = self.dao_msig_initialized_pools
        for tkn in self.whitelisted_tokens:
            if tkn != 'BNT':

                # Define variables of interest and validate types
                bnt_per_tkn = self.validate_type(self.get_bnt_over_tkn_internal_rate(tkn))
                tkn_tkn_liquidity = self.validate_type(self.available_liquidity.ledger[tkn][tkn][-1])
                tkn_bnt_liquidity = self.validate_type(self.available_liquidity.ledger[tkn]['BNT'][-1])
                tkn_vault = self.validate_type(self.vault.ledger[tkn][-1])
                bnt_vault = self.validate_type(self.vault.ledger['BNT'][-1])
                bnt_staking = self.validate_type(self.staking.ledger['BNT'][-1])
                bnbnt_supply = self.validate_type(self.pool_token_supply.ledger[f"bnBNT_ERC20_contract"]["supply"][-1])
                funding_remaining = self.validate_type(self.available_liquidity.ledger[tkn]['funding_remaining'][-1])

                # Convert the vault balance to BNT / TKN units
                tkn_vault_times_bnt_per_tkn = self.tokenomics.handle_multiplication(tkn_vault, bnt_per_tkn)

                # Hack to allow state-based comparison with Barak's solidity output (JSON) (NOTE: default=1 causes no change in expected values)
                min_liquidity_threshold = self.tokenomics.handle_multiplication(self.min_liquidity_threshold, multiplier)

                if (
                        tkn_tkn_liquidity == 0 \
                        and tkn_bnt_liquidity == 0 \
                        and tkn_vault_times_bnt_per_tkn >= min_liquidity_threshold \
                        and tkn not in self.dao_msig_initialized_pools
                    ) \
                        or force:

                    # append current block_num
                    self.available_liquidity.ledger[tkn]['block_num'].append(self.block_num)

                    # new available liquidity value = min_liquidity_threshold / bnt_per_tkn
                    self.available_liquidity.ledger[tkn][tkn].append(self.tokenomics.handle_division(min_liquidity_threshold, bnt_per_tkn))

                    # available tknBNT liquidity becomes the min_liquidity_threshold
                    self.available_liquidity.ledger[tkn]['BNT'].append(min_liquidity_threshold)

                    # BNT vault ledger balance value = existing + min_liquidity_threshold
                    self.vault.ledger['BNT'].append(self.tokenomics.handle_addition(bnt_vault, min_liquidity_threshold))

                    # BNT staking ledger balance value = existing + min_liquidity_threshold
                    self.staking.ledger['BNT'].append(self.tokenomics.handle_addition(bnt_staking, min_liquidity_threshold))

                    # bnBNT token supply value = existing + min_liquidity_threshold
                    self.pool_token_supply.ledger[f"bnBNT_ERC20_contract"]["supply"].append(self.tokenomics.handle_addition(bnbnt_supply, min_liquidity_threshold))

                    # update the EMA for this token
                    self.update_ema(tkn)

                    # Adjust the available liquidity funding remaining value = funding_remaining - min_liquidity_threshold
                    self.available_liquidity.ledger[tkn]['funding_remaining'].append(self.tokenomics.handle_subtraction(funding_remaining, min_liquidity_threshold))

                    # Append the token to the DAO Initialized pools list (so that we don't re-initialize accidentally in the future)
                    dao_msig_initialized_pools.append(tkn)

                    if "bnBNT" not in self.protocol_agent.wallet:
                        self.protocol_agent.wallet['bnBNT'] = {'block_num':[0], 'bnBNT':[0]}

                    bnbnt_rate = self.get_bnbnt_rate(bnbnt_supply, bnt_staking)
                    self.protocol_agent.wallet["bnBNT"]["bnBNT"].append(min_liquidity_threshold * bnbnt_rate)
                    self.protocol_agent.wallet["bnBNT"]['block_num'].append(self.block_num)

        # Update the dao_msig_initialized_pools
        self.dao_msig_initialized_pools = dao_msig_initialized_pools

        # Check if any of the updated pools meet all of the bootstrapping requirements
        self.check_bootstrapped_tokens()

    def update_ema(self, tkn):
        """Updates the EMA (Exponential Moving Average) based on current spot rates.

        Args:
            tkn (str): The tickername of the token.
        Returns:
            self
        """
        alpha = self.validate_type(self.alpha)
        bnt_over_tkn_rate = self.validate_type(self.get_bnt_over_tkn_internal_rate(tkn))
        current_ema = self.validate_type(self.ema[tkn]['ema'][-1])
        ema = self.ema
        if tkn in self.ema:
            if ema[tkn]['block_num'][-1] < self.block_num:
                ema[tkn]['block_num'].append(self.block_num)
                new_ema = self.tokenomics.handle_ema(alpha, bnt_over_tkn_rate, current_ema)
                ema[tkn]['ema'].append(new_ema)
        else:
            ema[tkn]['block_num'].append(self.block_num)
            ema[tkn]['ema'].append(self.exchange_rates[tkn])
        self.ema = ema

    def is_within_ema_tolerance(self, tkn, lower_limit=Fraction(99, 100), upper_limit=Fraction(101, 100)):
        """Check if the spot rate is outside of the EMA tolerance. No changes are made to the pool depth if outside limits.

        Args:
            tkn (str): The tickername of the token.
        Returns:
            bntkn_value (int or float or decimal): value of a single bntkn pool token.
        """
        bnt_over_tkn_rate = self.get_bnt_over_tkn_internal_rate(tkn)
        bnt_over_tkn_rate = self.validate_type(bnt_over_tkn_rate)
        ema = self.ema[tkn]['ema'][-1]
        ema = self.validate_type(ema)
        lower_limit = self.validate_type(lower_limit)
        upper_limit = self.validate_type(upper_limit)
        lower_bound = self.tokenomics.handle_multiplication(lower_limit, ema)
        upper_bound = self.tokenomics.handle_multiplication(upper_limit, ema)
        result = lower_bound <= bnt_over_tkn_rate <= upper_bound
        if self.verbose:
            print(
                f"spot_rate={bnt_over_tkn_rate} \n",
                f"ema={ema} \n",
                f"EMA Test = {result}, ({lower_limit} * {ema}) <= {bnt_over_tkn_rate} <= ({upper_limit} * {ema}), tkn={tkn}"
            )
        return result

    def remove_from_vault(self, tkn, x):
        """Adds x tkn to the self.vault.ledger dictionary with the same block_num number.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The amount of tkn.
        Returns:
            self
        """
        for key in self.vault.ledger:
            if key == tkn:
                new_val = self.tokenomics.handle_subtraction(self.vault.ledger[key][-1], x)
                self.vault.ledger[key].append(new_val)
            else:
                self.vault.ledger[key].append(self.vault.ledger[key][-1])
            self.vault.ledger['block_num'][-1] = self.block_num

    def add_to_vault(self, tkn, x):
        """Adds x tkn to the self.vault.ledger dictionary with the same block_num number.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The amount of tkn.
        Returns:
            self
        """
        for key in self.vault.ledger:
            if key == tkn:

                new_val = self.tokenomics.handle_addition(self.vault.ledger[key][-1], x)
                self.vault.ledger[key].append(new_val)
            else:
                self.vault.ledger[key].append(self.vault.ledger[key][-1])
            self.vault.ledger['block_num'][-1] = self.block_num

    def add_to_staking_ledger(self, tkn, x):
        """Adds x tkn to the self.staking.ledger dictionary with the same block_num number.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The amount of tkn.
        Returns:
            self
        """
        self.staking.ledger['block_num'].append(self.block_num)
        for key in self.staking.ledger:
            if key == tkn:
                new_val = self.tokenomics.handle_addition(self.staking.ledger[key][-1], x)
                self.staking.ledger[key].append(new_val)
            else:
                self.staking.ledger[key].append(self.staking.ledger[key][-1])

    def add_to_vortex_ledger(self, x):
        """Adds tkn to the vortex ledger.

        Args:
            x (int or float or decimal): The value of BNT to add to the vortex.

        Returns:
            self
        """
        new_val = self.tokenomics.handle_addition(self.vortex.ledger['BNT'][-1], x)
        self.vortex.ledger['BNT'].append(new_val)
        self.vortex.ledger['block_num'].append(self.block_num)

    def add_tkn_to_pool_token_supply_ledger(self, tkn, x):
        self.pool_token_supply.ledger[tkn]['block_num'].append(self.block_num)
        for key in self.pool_token_supply.ledger:
            if key == tkn:
                new_val = self.tokenomics.handle_addition(self.pool_token_supply.ledger[tkn]['supply'][-1], x)
                self.pool_token_supply.ledger[tkn]['supply'].append(new_val)
            else:
                self.pool_token_supply.ledger[key]['supply'].append(self.pool_token_supply.ledger[key]['supply'][-1])

    def add_tkn_to_available_liquidity_ledger(self, tkn, x):
        """Adds tkn to the available liquidity ledger.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or Decimal or decimal): The value of liquidity to add.

        Returns:
            self
        """
        for key in self.available_liquidity.ledger:
            if key == tkn:
                ema = self.validate_type(self.ema[tkn]['ema'][-1])
                a = self.validate_type(self.available_liquidity.ledger[key]['BNT'][-1])
                b = self.tokenomics.handle_division(a, ema)
                c = self.validate_type(self.tokenomics.handle_subtraction(self.vault.ledger[key][-1], b))
                c_ema = self.tokenomics.handle_multiplication(c, ema)

                spot_rate = self.get_bnt_over_tkn_internal_rate(tkn)
                print('spot_rate ', spot_rate)
                print('ema ', ema)

                b_plus_c = self.tokenomics.handle_addition(b, c)
                funding_remaining = self.validate_type(self.available_liquidity.ledger[key]['funding_remaining'][-1])
                a_plus_funding_remaining = self.tokenomics.handle_addition(a, funding_remaining)

                if self.verbose: print(f'a={a}, b={b}, c={c}, ema={ema}, funding_remaining={funding_remaining}')

                if (c >= b) & (a <= funding_remaining):
                    if self.verbose: print('case1')
                    new_tknbnt_liquidity = self.tokenomics.handle_multiplication(a, 2)
                    new_tkn_liquidity = self.tokenomics.handle_multiplication(b, 2)
                    new_funding_remaining = self.tokenomics.handle_subtraction(funding_remaining, a)

                elif (c >= b) & (a > funding_remaining) or (c < b) & (a > funding_remaining) & (c_ema >= funding_remaining):
                    if self.verbose: print('case2')
                    new_tknbnt_liquidity = a_plus_funding_remaining
                    new_tkn_liquidity = self.tokenomics.handle_division(a_plus_funding_remaining, ema)
                    new_funding_remaining = 0

                elif (c < b) & (a <= funding_remaining) or (c < b) & (a > funding_remaining) & (c_ema < funding_remaining):
                    if self.verbose: print('case3')
                    new_tknbnt_liquidity = self.tokenomics.handle_multiplication(b_plus_c, ema)
                    new_tkn_liquidity = b_plus_c
                    new_funding_remaining = self.tokenomics.handle_subtraction(funding_remaining, c_ema)

                self.available_liquidity.ledger[key]['BNT'].append(new_tknbnt_liquidity)
                self.available_liquidity.ledger[key][tkn].append(new_tkn_liquidity)
                self.available_liquidity.ledger[key]['funding_remaining'].append(new_funding_remaining)
                self.available_liquidity.ledger[key]['block_num'].append(self.block_num)

                final_liquidity = self.available_liquidity.ledger[key]['BNT'][-1]
                delta = self.tokenomics.handle_subtraction(final_liquidity, a)
                bnt_staked = self.staking.ledger['BNT'][-1]
                bnbnt_supply = self.pool_token_supply.ledger["bnBNT_ERC20_contract"]["supply"][-1]

                if bnbnt_supply > 0 and bnt_staked > 0:
                    bnt_bntkn_over_bnt_rate = self.tokenomics.handle_division(bnt_staked, bnbnt_supply)
                    update_amt = self.tokenomics.handle_division(delta, bnt_bntkn_over_bnt_rate)
                    self.add_tkn_to_pool_token_supply_ledger("bnBNT_ERC20_contract", update_amt)

                self.add_to_vault('BNT', delta)
                self.add_to_staking_ledger('BNT', delta)

                if "bnBNT" not in self.protocol_agent.wallet:
                    self.protocol_agent.wallet["bnBNT"] = {'block_num': [0], "bnBNT": [0]}

                bnbnt_rate = self.get_bnbnt_rate(bnbnt_supply, bnt_staked)
                new_val = self.tokenomics.handle_addition(self.protocol_agent.wallet["bnBNT"]["bnBNT"][-1], self.tokenomics.handle_multiplication(delta, bnbnt_rate))
                self.protocol_agent.wallet["bnBNT"]["bnBNT"].append(new_val)
                self.protocol_agent.wallet["bnBNT"]['block_num'].append(self.block_num)

            else:
                self.available_liquidity.ledger[key][key].append(self.available_liquidity.ledger[key][key][-1])
                self.available_liquidity.ledger[key]['BNT'].append(self.available_liquidity.ledger[key]['BNT'][-1])
                self.available_liquidity.ledger[key]['block_num'].append(self.block_num)
                self.available_liquidity.ledger[key]['funding_remaining'].append(
                    self.available_liquidity.ledger[key]['funding_remaining'][-1])


    # def add_tkn_to_available_liquidity_ledger(self, tkn, x):
    #     """Adds tkn to the available liquidity ledger.
    #
    #     Args:
    #         tkn (str): The tickername of the token.
    #         x (int or float or Decimal or decimal): The value of liquidity to add.
    #
    #     Returns:
    #         self
    #     """
    #     for key in self.available_liquidity.ledger:
    #         if key == tkn:
    #             ema = self.validate_type(self.ema[tkn]['ema'][-1])
    #             a = self.validate_type(self.available_liquidity.ledger[key]['BNT'][-1])
    #             b = self.validate_type(self.available_liquidity.ledger[key][key][-1])
    #             c = self.validate_type(self.tokenomics.handle_subtraction(self.vault.ledger[key][-1], b))
    #
    #             import math
    #             a_ema = floor(math.sqrt(a * b * ema))
    #             b_ema = floor(math.sqrt(floor(a * b / ema)))
    #             c_ema = floor(math.sqrt(floor(a * c / ema)))
    #
    #             # b = self.tokenomics.handle_division(a, ema)
    #             # c_ema = self.tokenomics.handle_multiplication(c, ema)
    #
    #             b_plus_c = self.tokenomics.handle_addition(b_ema, c_ema)
    #             funding_remaining = self.validate_type(self.available_liquidity.ledger[key]['funding_remaining'][-1])
    #             a_plus_funding_remaining = self.tokenomics.handle_addition(a, funding_remaining)
    #
    #             if self.verbose: print(f'a={a_ema}, b={b_ema}, c={c_ema}, ema={ema}, funding_remaining={funding_remaining}')
    #
    #             if (c_ema >= b_ema) & (a_ema <= funding_remaining):
    #                 if self.verbose: print('case1', b_ema, floor(b_ema))
    #                 new_tknbnt_liquidity = self.tokenomics.handle_multiplication(a_ema, 2)
    #                 new_tkn_liquidity = self.tokenomics.handle_multiplication(b_ema, 2)
    #                 new_funding_remaining = self.tokenomics.handle_subtraction(funding_remaining, a_ema)
    #
    #             elif (c_ema >= b_ema) & (a_ema > funding_remaining) or (c_ema < b_ema) & (a_ema > funding_remaining) & (c_ema >= funding_remaining):
    #                 if self.verbose: print('case2')
    #                 new_tknbnt_liquidity = a_plus_funding_remaining
    #                 new_tkn_liquidity = self.tokenomics.handle_division(a_plus_funding_remaining, ema)
    #                 new_funding_remaining = 0
    #
    #             elif (c_ema < b_ema) & (a_ema <= funding_remaining) or (c_ema < b_ema) & (a_ema > funding_remaining) & (c_ema < funding_remaining):
    #                 if self.verbose: print('case3')
    #                 new_tknbnt_liquidity = self.tokenomics.handle_multiplication(b_plus_c, ema)
    #                 new_tkn_liquidity = b_plus_c
    #                 new_funding_remaining = self.tokenomics.handle_subtraction(funding_remaining, c_ema)
    #
    #             print('new_tknbnt_liquidity ', new_tknbnt_liquidity, type(new_tknbnt_liquidity))
    #             self.available_liquidity.ledger[key]['BNT'].append(new_tknbnt_liquidity)
    #             self.available_liquidity.ledger[key][tkn].append(new_tkn_liquidity)
    #             self.available_liquidity.ledger[key]['funding_remaining'].append(new_funding_remaining)
    #             self.available_liquidity.ledger[key]['block_num'].append(self.block_num)
    #
    #             final_liquidity = self.available_liquidity.ledger[key]['BNT'][-1]
    #             delta = floor(self.tokenomics.handle_subtraction(final_liquidity, a_ema))
    #             bnt_staked = floor(self.staking.ledger['BNT'][-1])
    #             bnbnt_supply = floor(self.pool_token_supply.ledger["bnBNT_ERC20_contract"]["supply"][-1])
    #
    #             if bnbnt_supply > 0 and bnt_staked > 0:
    #                 # print('bnt_staked, bnbnt_supply ', bnt_staked, bnbnt_supply, type(bnt_staked), type(bnbnt_supply))
    #                 bnt_bntkn_over_bnt_rate = floor(self.tokenomics.handle_division(bnt_staked, bnbnt_supply))
    #                 # print('delta, bnt_bntkn_over_bnt_rate', delta, bnt_bntkn_over_bnt_rate, type(delta), type(bnt_bntkn_over_bnt_rate))
    #                 update_amt = self.tokenomics.handle_division(delta, bnt_bntkn_over_bnt_rate)
    #                 self.add_tkn_to_pool_token_supply_ledger("bnBNT_ERC20_contract", update_amt)
    #
    #             self.add_to_vault('BNT', delta)
    #             self.add_to_staking_ledger('BNT', delta)
    #
    #             if "bnBNT" not in self.protocol_agent.wallet:
    #                 self.protocol_agent.wallet["bnBNT"] = {'block_num': [0], "bnBNT": [0]}
    #
    #             bnbnt_rate = self.get_bnbnt_rate(bnbnt_supply, bnt_staked)
    #             new_val = self.tokenomics.handle_addition(self.protocol_agent.wallet["bnBNT"]["bnBNT"][-1], self.tokenomics.handle_multiplication(delta, bnbnt_rate))
    #             self.protocol_agent.wallet["bnBNT"]["bnBNT"].append(new_val)
    #             self.protocol_agent.wallet["bnBNT"]['block_num'].append(self.block_num)
    #
    #         else:
    #             self.available_liquidity.ledger[key][key].append(self.available_liquidity.ledger[key][key][-1])
    #             self.available_liquidity.ledger[key]['BNT'].append(self.available_liquidity.ledger[key]['BNT'][-1])
    #             self.available_liquidity.ledger[key]['block_num'].append(self.block_num)
    #             self.available_liquidity.ledger[key]['funding_remaining'].append(
    #                 self.available_liquidity.ledger[key]['funding_remaining'][-1])