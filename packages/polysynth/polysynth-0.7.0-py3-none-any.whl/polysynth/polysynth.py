import os
import sys
import time
import ast
import json
from datetime import datetime
import logging
from typing import Any, Callable, Optional, Union, Dict
import requests

import pickledb
from web3 import Web3
from web3.eth import Contract
from web3.contract import ContractFunction
from web3.exceptions import ContractLogicError, TimeExhausted
from web3.middleware import geth_poa_middleware
from web3.types import (
    TxParams,
    Wei,
    Nonce,
    HexBytes,
)
from polysynth.enum import ErrorMessage, PnlCalcOption, StatusCode

from polysynth.exception import InvalidFormatError, InvalidParameterError, MissingInputError, PolysynthException, TransactionFailedError, NoPositionsOpen, TransactionTimedOut, InvalidGasEstimateFunction
from .types import AddressLike, FundingRateRes, MarginRes, OpenPositionRes, Response, TraderPosition
from .util import (
    _str_to_addr,
    _addr_to_str,
    _load_contract,
    _load_oracle_contract,
    _side_str_to_int,
    _amm_name_to_addr,
    _amm_name_to_oracle_addr,
    _int_to_bignum,
    _check_leverage,
    _check_slippage,
    _check_collateral,
    _normalize,
    _estimate_gas_fee
)

from .constants import (
    _netid_to_name,
    _contract_addresses_oracle
)

from polysynth.abi import ABI

logger = logging.getLogger(__name__)


class Polysynth:
    """
    Wrapper around Polysynth contract
    """

    def __init__(
        self,
        address: Union[AddressLike, str, None],
        private_key: Optional[str],
        gas_estimate_custom: Optional[Callable] = None,
        provider: str = None,
        web3: Web3 = None,
        version: int = 1,
        default_slippage: float = 0.005,
        stable_token_contract_addr: str = None,
        manager_contract_addr: str = None,
        amm_reader_contract_addr: str = None,
        network_name: str = None
    ):
        """
        :param address: The public address of the account to use.
        :param private_key: The private key of the account to use.
        :param provider: Can be optionally set to a Web3 provider URI. If none set, will fall back to the PROVIDER environment variable, or web3 if set.
        :param web3: Can be optionally set to a custom Web3 instance.
        :param version: Which version of the Polysynth contract to use.
        :param default_slippage: Default slippage for a trade, as a float(0.01 is 1 %).
        """
        try:
            self.gas_estimate_custom = gas_estimate_custom
            self.address: AddressLike = _str_to_addr(
                address or "0x0000000000000000000000000000000000000000"
            )
            self.private_key = (
                private_key
                or "0x0000000000000000000000000000000000000000000000000000000000000000"
            )
            self.version = version
            self.default_slippage = default_slippage

            if web3:
                self.w3 = web3
            else:
                self.provider = provider or os.environ["PROVIDER"]
                self.w3 = Web3(
                    Web3.HTTPProvider(
                        self.provider, request_kwargs={"timeout": 60})
                )

            # self.w3.eth.set_gas_price_strategy(medium_gas_price_strategy)
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # self.w3.transactionManager.UseLegacyAsDefault = True

            netid = 0
            try:
                netid = int(self.w3.net.version)
                if netid in _netid_to_name:
                    self.network = _netid_to_name[netid]
                else:
                    raise InvalidParameterError(
                        StatusCode.BAD_REQUEST.value, StatusCode.UNKNOWN_PROVIDER.value, ErrorMessage.INVALID_PROVIDER_URL.value)
            except:
                raise InvalidParameterError(
                    StatusCode.BAD_REQUEST.value, StatusCode.UNKNOWN_PROVIDER.value, ErrorMessage.INVALID_PROVIDER_URL.value)

            # print(
            #     'netid', 'https://protocol-meta.s3.ap-southeast-1.amazonaws.com/polysynth/'+str(netid)+'/abi.json')
            # r = requests.get(
            #     'https://protocol-meta.s3.ap-southeast-1.amazonaws.com/polysynth/'+str(netid)+'/abi.json')
            # print(r.json())

            self.abi = ABI(netid, network_name)

            self.last_nonce: Nonce = self.w3.eth.get_transaction_count(
                self.address)

            self.max_approval_hex = f"0x{64 * 'f'}"
            self.max_approval_int = int(self.max_approval_hex, 16)
            self.max_approval_check_hex = f"0x{15 * '0'}{49 * 'f'}"
            self.max_approval_check_int = int(self.max_approval_check_hex, 16)

            self.fluctuation_limit = 0.012
            self.tx_timeout = 30
            self.db = pickledb.load('txns.db', False)

            if self.version == 1:
                if stable_token_contract_addr is None:
                    stable_token_info = self.abi.get_contract('StableToken')

                self.stable_token_addr = _str_to_addr(
                    stable_token_info['address'])
                self.stable_token_contract = _load_contract(
                    self.w3,
                    self.network,
                    abi_name="StableToken",
                    address=stable_token_info['address'],
                    abi=json.dumps(stable_token_info['abi'])
                )

                if manager_contract_addr is None:
                    manager_contract_info = self.abi.get_contract("Manager")

                self.manager_contract = _load_contract(
                    self.w3,
                    self.network,
                    abi_name="Manager",
                    address=_str_to_addr(manager_contract_info['address']),
                    abi=json.dumps(manager_contract_info['abi'])
                )

                if amm_reader_contract_addr is None:
                    amm_reader_contract_info = self.abi.get_contract(
                        "AmmReader")

                self.amm_reader_contract = _load_contract(
                    self.w3,
                    self.network,
                    abi_name="AmmReader",
                    address=_str_to_addr(amm_reader_contract_info['address']),
                    abi=json.dumps(amm_reader_contract_info['abi'])
                )

        except PolysynthException as pe:
            print(pe)
            sys.exit()

    def input_price(
        self,
        amm: str,
        side: str,
        quoteAssetAmount: int,
    ) -> Response:
        ''' 
            For a market, get equivalent base token amount against quoted token amount

        Args:
            amm (str): name of the market, eg; ETH
            side (int): direction of the quoted asset
            quoteAssetAmount (Wei): quoted asset amount

        Returns:
            Any: Base asset amount
        '''
        try:
            price = _normalize(self._input_price(
                amm, side, quoteAssetAmount)[0])
            return Response(StatusCode.OK.value, None, None, data={"amount": abs(price)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def output_price(
        self,
        amm: str,
        side: str,
        baseAssetAmount: int,
    ) -> Response:
        ''' 
            For a market, get equivalent quoted token amount against base token amount

        Args:
            amm (str): name of the market, eg; ETH
            side (int): direction of the base asset
            baseAssetAmount (Wei): base asset amount

        Returns:
            Any: Quote asset amount
        '''
        try:
            # amm_contract_addr = _amm_name_to_addr(amm, self.network)
            # amm_contract = _load_contract(
            #     self.w3,
            #     self.network,
            #     abi_name="Amm_" + amm.split("-")[0].upper(),
            #     address=_str_to_addr(amm_contract_addr),
            # )
            _rev_side = 1 if _side_str_to_int(side) == 0 else 0
            # price = amm_contract.functions.getOutputPrice(
            #     _rev_side,
            #     _int_to_bignum(baseAssetAmount)
            # ).call()
            amm_info = self.abi.get_contract(amm)
            price = self.amm_reader_contract.functions.getStableTokenAmount(
                amm_info['address'], _side_str_to_int(side), _int_to_bignum(baseAssetAmount)).call()
            return Response(StatusCode.OK.value, None, None, data={"amount": abs(_normalize(price[0]))}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def open_position(
        self,
        amm: str,
        side: str,
        quoteAssetAmount: int,
        leverage: int,
        slippage: int = 0.005
    ) -> Response:
        ''' 
            Open trader's long/short position against an amm

        Args:
            amm (str): name of the market, eg; ETH
            side (int): direction of the trade; 0-buy, 1-sell
            quoteAssetAmount (Wei): quote asset amount
            leverage (int): leverage on quoted amount
            slippage (int): Slippage tolerance

        Returns:
            Hexbytes: Transaction Hash
        '''
        try:
            self.check_trade_constraints(
                amm, side, quoteAssetAmount, leverage, slippage)

            # set allowance for manager to spend token on behalf of user
            allowance = self.allowance()
            if allowance < self.max_approval_int/2:
                self.approve()

            # _amm_contract_addr = _amm_name_to_addr(amm, self.network)
            _amm_info = self.abi.get_contract(amm)
            _side = _side_str_to_int(side)
            _quote_asset_limit = self._quote_asset_limit(
                amm, quoteAssetAmount, leverage, _side, slippage)
            _size = _normalize(self._input_price(
                amm, side, quoteAssetAmount*leverage)[0])
            _price = (quoteAssetAmount*leverage)/_size

            manager = self.manager_contract.functions
            tx_params = self._get_tx_params()
            func_params = [
                _amm_info['address'],
                _side,
                _int_to_bignum(quoteAssetAmount),
                leverage,
                abs(int(_quote_asset_limit)),
            ]

            func = manager.openPosition(*func_params)

            receipt = None
            try:
                receipt = self._build_and_send_tx(func, tx_params)
            except Exception as e:
                return e
                # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

            tx = None
            try:
                tx = self.w3.eth.wait_for_transaction_receipt(
                    receipt, timeout=self.tx_timeout)
            except TimeExhausted as te:
                self.db.set(receipt.hex(), ("openPosition",
                            func_params, tx_params["nonce"]))
                self.db.dump()
                return TransactionTimedOut(
                    StatusCode.REQUEST_TIMEOUT.value,
                    StatusCode.TRANSACTION_PENDING.value,
                    ErrorMessage.TRANSACTION_PENDING.value,
                    data={"tx_hash": receipt.hex()}).__dict__()

            time.sleep(2)

            position = self._trader_position(amm)
            if position[0] == 0:
                raise NoPositionsOpen(
                    StatusCode.OK.value, StatusCode.ZERO_COLLATERAL.value, ErrorMessage.NO_POSITIONS_OPEN.value)
            # _price = round(position[2]/position[0], 4)
            # _size = _normalize(position[0])

            _side = "BUY" if _size > 0 else "SELL"
            # _leverage = round(position[2]/position[1], 4)

            _collateral_ratio = _normalize(self._collateral_ratio(amm))
            _leverage = round(1/_collateral_ratio, 4)

            result = OpenPositionRes(
                _price, _side, _size, _leverage, _collateral_ratio, tx).__dict__()

            return Response(StatusCode.OK.value, None, None, data=result).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def close_position(
        self,
        amm: str,
        slippage=0.005
    ) -> Response:
        '''
            Close trader's position against an amm

        Args:
            amm (str): name of the market, eg; ETH
            slippage (int): Slippage tolerance

        Returns:
            Hexbytes: Transaction Hash
        '''
        try:
            _check_slippage(slippage)

            # check if no position open
            _position = self._trader_position(amm)
            _size = _normalize(_position[0])
            if _size == 0:
                raise TransactionFailedError(
                    StatusCode.FAILED_TRANSACTION.value, StatusCode.EXECUTION_REVERTED.value, ErrorMessage.NO_POSITIONS_OPEN.value)

            # amm_contract_addr = _amm_name_to_addr(
            #     amm, self.network)  # for eg resolves to Amm_eth

            amm_info = self.abi.get_contract(amm)

            _stable_asset_limit = self._stable_asset_limit(amm, slippage)

            manager = self.manager_contract.functions
            tx_params = self._get_tx_params()
            func_params = [
                amm_info['address'],
                abs(int(_stable_asset_limit)),
            ]

            func = manager.closePosition(*func_params)

            receipt = None
            try:
                receipt = self._build_and_send_tx(func, tx_params)
            except Exception as e:
                return e
                # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

            tx = None
            try:
                tx = self.w3.eth.wait_for_transaction_receipt(
                    receipt, timeout=self.tx_timeout)
            except TimeExhausted as te:
                self.db.set(receipt.hex(), ("closePosition",
                            func_params, tx_params["nonce"]))
                self.db.dump()
                return TransactionTimedOut(
                    StatusCode.REQUEST_TIMEOUT.value,
                    StatusCode.TRANSACTION_PENDING.value,
                    ErrorMessage.TRANSACTION_PENDING.value,
                    data={"tx_hash": receipt.hex()}).__dict__()

            result = {
                "tx_hash": tx["transactionHash"].hex(),
                "gas_fees": tx["gasUsed"],
            }

            return Response(StatusCode.OK.value, None, None, data=result).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def add_margin(
        self,
        amm: str,
        collateral: int
    ) -> Response:
        '''
            Add collateral to trader's account
        Args:
            amm (str): name of the market, eg; ETH
            collateral (int): Collateral Amount

        Returns:
            Hexbytes: Transaction Hash
        '''
        try:
            # amm_contract_addr = _amm_name_to_addr(
            #     amm, self.network)  # for eg resolves to Amm_eth
            amm_info = self.abi.get_contract(amm)
            manager = self.manager_contract.functions
            func_params = [
                amm_info['address'],
                _int_to_bignum(collateral),
            ]

            tx_params = self._get_tx_params()
            func = manager.addCollateral(*func_params)

            receipt = None
            try:
                receipt = self._build_and_send_tx(func, tx_params)
            except Exception as e:
                return e
                # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

            tx = None
            try:
                tx = self.w3.eth.wait_for_transaction_receipt(
                    receipt, timeout=self.tx_timeout)
            except TimeExhausted as te:
                self.db.set(receipt.hex(), ("addCollateral",
                            func_params, tx_params["nonce"]))
                self.db.dump()
                return TransactionTimedOut(
                    StatusCode.REQUEST_TIMEOUT.value,
                    StatusCode.TRANSACTION_PENDING.value,
                    ErrorMessage.TRANSACTION_PENDING.value,
                    data={"tx_hash": receipt.hex()}).__dict__()
            time.sleep(1)
            # get trader's new leverage and margin
            position = self._trader_position_with_funding_payment(amm)
            # new_collateral, new_leverage = _normalize(position[1]), round(position[2]/position[1], 4)
            new_collateral = _normalize(position[1])

            _unrealized_pnl = _normalize(self._unrealized_pnl(amm))
            _margin_after = new_collateral + _unrealized_pnl

            ratio = _normalize(self._collateral_ratio(amm))
            new_leverage = round(1/ratio, 4)
            result = MarginRes(_margin_after, new_leverage,
                               ratio, tx).__dict__()

            return Response(StatusCode.OK.value, None, None, data=result).__dict__()
        except ContractLogicError as e:
            return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.EXECUTION_REVERTED.value, ErrorMessage.NO_POSITIONS_OPEN.value).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def remove_margin(
        self,
        amm: str,
        collateral: int
    ) -> Response:
        '''
            Remove collateral from trader's account
        Args:
            amm (str): name of the market, eg; ETH
            collateral (int): Collateral Amount

        Returns:
            Response Body
        '''
        try:
            # amm_contract_addr = _amm_name_to_addr(
            #     amm, self.network)  # for eg resolves to Amm_eth
            amm_info = self.abi.get_contract(amm)
            # check if value doesn't exceed trader's collateral
            position = self._trader_position(amm)

            _collateral_after = _normalize(position[1]) - collateral
            if _collateral_after < 0:
                raise InvalidParameterError(
                    StatusCode.BAD_REQUEST.value, StatusCode.COLLATERAL_NOT_ENOUGH.value, ErrorMessage.COLLATERAL_NOT_ENOUGH.value)
            # _position_curr = self._trader_position_with_funding_payment(amm)
            # _collateral = _normalize(_position_curr[1])
            # _unrealized_pnl = _normalize(self._unrealized_pnl(amm))

            # _margin_ratio_curr = _normalize(self._collateral_ratio(amm))
            # _margin = _collateral + _unrealized_pnl

            # _collateral_ratio_after = ( _margin - collateral ) / ( _margin/_margin_ratio_curr )

            # if _collateral_ratio_after < 0.0625:
            #     raise InvalidParameterError(StatusCode.BAD_REQUEST.value, StatusCode.COLLATERAL_NOT_ENOUGH.value, ErrorMessage.COLLATERAL_NOT_ENOUGH.value)

            manager = self.manager_contract.functions
            func_params = [
                amm_info['address'],
                _int_to_bignum(collateral),
            ]

            tx_params = self._get_tx_params()
            func = manager.removeCollateral(*func_params)

            receipt = None
            try:
                receipt = self._build_and_send_tx(func, tx_params)
            except Exception as e:
                return e
                # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

            tx = None
            try:
                tx = self.w3.eth.wait_for_transaction_receipt(
                    receipt, timeout=self.tx_timeout)
            except TimeExhausted as te:
                self.db.set(receipt.hex(), ("removeCollateral",
                            func_params, tx_params["nonce"]))
                self.db.dump()
                return TransactionTimedOut(
                    StatusCode.REQUEST_TIMEOUT.value,
                    StatusCode.TRANSACTION_PENDING.value,
                    ErrorMessage.TRANSACTION_PENDING.value,
                    data={"tx_hash": receipt.hex()}).__dict__()

            position = self._trader_position_with_funding_payment(amm)
            # new_collateral, new_leverage = _normalize(position[1]), round(position[2]/position[1], 4)
            new_collateral = _normalize(position[1])

            _unrealized_pnl = _normalize(self._unrealized_pnl(amm))
            _margin_after = new_collateral + _unrealized_pnl

            ratio = _normalize(self._collateral_ratio(amm))
            new_leverage = round(1/ratio, 4)
            result = MarginRes(_margin_after, new_leverage,
                               ratio, tx).__dict__()
            return Response(StatusCode.OK.value, None, None, data=result).__dict__()
        except ContractLogicError as e:
            return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.EXECUTION_REVERTED.value, ErrorMessage.INSUFFICIENT_COLLATERAL_TO_WITHDRAW.value).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def allowance(
        self,
    ) -> Any:
        """Allowance"""
        token = self.stable_token_contract.functions
        scaled_amount = token.allowance(
            self.address,
            self.abi.get_contract("Manager")['address']
        ).call()
        return scaled_amount

    def approve(
        self,
    ) -> None:
        """Approve the amount"""
        token = self.stable_token_contract.functions
        func_params = [
            self.abi.get_contract("Manager")['address'],
            self.max_approval_int,
        ]

        func = token.approve(*func_params)
        tx_params = self._get_tx_params()

        receipt = None
        try:
            receipt = self._build_and_send_tx(func, tx_params)
        except Exception as e:
            return e
            # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

        tx = None
        try:
            tx = self.w3.eth.wait_for_transaction_receipt(
                receipt, timeout=self.tx_timeout)
        except TimeExhausted as te:
            self.db.set(receipt.hex(), (func, tx_params["nonce"]))
            self.db.dump()
            return TransactionTimedOut(
                StatusCode.REQUEST_TIMEOUT.value,
                StatusCode.TRANSACTION_PENDING.value,
                ErrorMessage.TRANSACTION_PENDING.value,
                data={"tx_hash": receipt.hex()}).__dict__()

    def mark_price(
        self,
        amm: str = None,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            For a market, get current spot price

        Args:
            amm (str): name of the market, eg; ETH

        Returns:
            Any: spot price
        '''
        try:
            price = _normalize(self._spot_price(amm))
            return Response(StatusCode.OK.value, None, None, data={"mark_price": price}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def fluctuation_limit_ratio(
        self,
        amm: str = None,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            For a market, get fluctuation limit ratio

        Args:
            amm (str): name of the market, eg; ETH

        Returns:
            Any: fluctuation limit ratio
        '''
        try:
            if amm is None:
                raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                        ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
            # amm_contract_addr = _amm_name_to_addr(amm, self.network)
            amm_info = self.abi.get_contract(amm)
            amm_contract = _load_contract(
                self.w3,
                self.network,
                abi_name="Amm_" + amm.split("-")[0].upper(),
                address=_str_to_addr(amm_info['address']),
                abi=json.dumps(amm_info['abi'])
            )
            flr = amm_contract.functions.fluctuationLimitRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"fluctuation_limit_ratio": round(flr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def trade_limit_ratio(
        self,
        amm: str = None,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            For a market, get trade limit ratio

        Args:
            amm (str): name of the market, eg; ETH

        Returns:
            Any: trade limit ratio
        '''
        try:
            if amm is None:
                raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                        ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
            # amm_contract_addr = _amm_name_to_addr(amm, self.network)
            amm_info = self.abi.get_contract(amm)
            amm_contract = _load_contract(
                self.w3,
                self.network,
                abi_name="Amm_" + amm.split("-")[0].upper(),
                address=_str_to_addr(amm_info['address']),
                abi=json.dumps(amm_info['abi'])
            )
            tlr = amm_contract.functions.tradeLimitRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"trade_limit_ratio": round(tlr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def margin_ratio(
        self,
        amm: str = None,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            For a market, get collateral ratio of the trader

        Args:
            amm (str): name of the market, eg; ETH

        Returns:
            Any: collateral ratio of the trader
        '''
        try:
            ratio = _normalize(self._collateral_ratio(amm))
            return Response(StatusCode.OK.value, None, None, data={"margin_ratio": ratio}).__dict__()
        except ContractLogicError as e:
            return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.EXECUTION_REVERTED.value, ErrorMessage.NO_POSITIONS_OPEN.value).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def fee_ratio(
        self,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            Get fee ratio

        Args:

        Returns:
            Any: fee ratio
        '''
        try:
            fr = self.manager_contract.functions.feeRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"fee_ratio": round(fr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def init_margin_ratio(
        self,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            get init collateral ratio

        Args:

        Returns:
            Any: get initial collateral ratio
        '''
        try:
            icr = self.manager_contract.functions.initCollateralRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"init_margin_ratio": round(icr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def liquidation_fee_ratio(
        self,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            get liquidation fee ratio

        Args:

        Returns:
            Any: liquidation fee ratio
        '''
        try:
            lfr = self.manager_contract.functions.liquidationFeeRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"liquidation_fee_ratio": round(lfr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def maintenance_margin_ratio(
        self,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            get maintenance collateral ratio

        Args:

        Returns:
            Any: maintenance collateral ratio 
        '''
        try:
            mcr = self.manager_contract.functions.maintenanceCollateralRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"maintenance_margin_ratio": round(mcr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def partial_liquidation_ratio(
        self,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            get partial liquidation ratio

        Args:

        Returns:
            Any: partial liquidation ratio 
        '''
        try:
            plr = self.manager_contract.functions.partialLiquidationRatio().call()
            return Response(StatusCode.OK.value, None, None, data={"partial_liquidation_ratio": round(plr/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def price_impact(
        self,
        amm: str,
        size: int,
        **kwargs
    ) -> Response:
        '''
            get price impact
        Args:
            amm (str): name of the market, eg; ETH
            side (int): direction of the quoted asset
            quoteAssetAmount (int): quoted asset amount
            leverage (int): leverage on quote asset
        Returns:
            Any: fluctuation value 
        '''
        try:
            quoteAssetAmount = _normalize(
                self._output_price(amm, "BUY", size)[0])

            fluctuation = self._price_impact(amm, quoteAssetAmount, 1, 0)
            return Response(StatusCode.OK.value, None, None, data={"price_impact": round(fluctuation, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def wallet_balance(
        self,
        **kwargs
    ) -> Response:
        '''
            get wallet balance
        Args:
        Returns:
            Any: trader wallet balance
        '''
        try:
            balance = self._wallet_balance()
            return Response(StatusCode.OK.value, None, None, data={"wallet_balance": round(balance/10**6, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def unrealized_pnl(
        self,
        amm: str,
        **kwargs
    ) -> Response:
        '''
            Get unrealized pnl of a trader
        Args:
            amm: str
        Returns:
            Any: unrealized pnl of a trader
        '''
        try:
            unrealized_pnl = _normalize(self._unrealized_pnl(amm))
            return Response(StatusCode.OK.value, None, None, data={"unrealized_pnl": unrealized_pnl}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def positions(
        self,
        **kwargs
    ) -> Response:
        '''
            get price impact
        Args:
            amm (str): name of the market, eg; ETH
        Returns:
            Any: fluctuation value 
        '''
        try:
            res = []
            for key in self.abi.contracts.keys():
                if 'usdc' not in key:
                    continue  # filter all non-amm addresses

                amm = key.split('_')[1]
                position = self._trader_position(amm)

                size = _normalize(position[0])
                collateral = _normalize(position[1])

                if size == 0 or collateral == 0:
                    continue

                # leverage = round(position[2]/position[1], 4)
                _collateral_ratio = _normalize(self._collateral_ratio(amm))
                leverage = round(1/_collateral_ratio, 4)
                avg_entry_price = round(position[2]/position[0], 4)

                position_with_funding_payment = self._trader_position_with_funding_payment(
                    amm)
                unrealized_pnl = _normalize(self._unrealized_pnl(amm))

                # collateral + unrealized_pnl
                margin = _normalize(
                    position_with_funding_payment[1]) + unrealized_pnl

                side = "BUY" if size > 0 else "SELL"

                result = TraderPosition(amm.upper(
                ), side, size, collateral, leverage, avg_entry_price, margin, unrealized_pnl).__dict__()
                res.append(result)
            return Response(StatusCode.OK.value, None, None, data=res).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def index_price(
        self,
        amm: str = None,
        *args,
        **kwargs
    ) -> Response:
        ''' 
            For a market, get oracle price from chainlink

        Args:
            amm (str): name of the market, eg; ETH

        Returns:
            Any: oracle price from chainlink
        '''
        try:
            if amm is None:
                raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                        ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
            # oracle_addr = _amm_name_to_oracle_addr(amm, self.network)
            # oracle_contract = _load_oracle_contract(
            #     self.w3,
            #     address=_str_to_addr(oracle_addr),
            # )
            # price = oracle_contract.functions.latestRoundData().call()
            amm_info = self.abi.get_contract(amm)

            amm_reader = self.amm_reader_contract.functions
            amm_metadata = amm_reader.getAmmMetadata(
                amm_info['address']).call()

            return Response(StatusCode.OK.value, None, None, data={"index_price": round(amm_metadata[2]/10**18, 4)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def funding_rate(
        self,
        amm: str,
        *args,
        **kwargs
    ) -> Response:
        '''
            For a given market, get all the funding rates
        Args:
            amm (str): name of the market, eg; ETH-USDC
        Returns: 
        Any: funding rates (long/short)
        '''
        try:
            if amm is None:
                raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                        ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

            amm_info = self.abi.get_contract(amm)

            amm_reader = self.amm_reader_contract.functions
            amm_metadata = amm_reader.getAmmMetadata(
                amm_info['address']).call()

            funding_rate_long, funding_rate_short = round(
                amm_metadata[4]/10**18, 7), round(amm_metadata[5]/10**18, 7)
            total_long, total_short = round(
                amm_metadata[7]/10**18, 7), round(amm_metadata[8]/10**18, 7)
            mark, index = round(
                amm_metadata[3]/10**18, 7), round(amm_metadata[2]/10**18, 7)
            pfrLong, pfrShort = None, None

            fr = (mark - index)/(index * 24)
            if ((total_long == 0) or (total_short == 0)):
                fr = 0

            if (abs(fr) > 0.05):
                if (fr > 0):
                    fr = 0.05
                if (fr < 0):
                    fr = -0.05

            if (fr > 0):
                x = (total_long/total_short)
                pfrLong = fr
                pfrShort = fr * x

            if (fr < 0):
                x = (total_short/total_long)
                pfrLong = fr * x
                pfrShort = fr

            futures = amm.upper()
            return FundingRateRes(funding_rate_long, funding_rate_short, total_long, total_short, pfrLong, pfrShort, futures).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def max_base_asset_limit(
        self,
        amm: str = None,
        *args,
        **kwargs
    ) -> Response:
        '''
            For a market, get trade limit ratio

        Args:
            amm (str): name of the market, eg; ETH

        Returns:
            Any: trade limit ratio
        '''
        try:
            if amm is None:
                raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                        ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
            # amm_contract_addr = _amm_name_to_addr(amm, self.network)
            # amm_contract = _load_contract(
            #     self.w3,
            #     self.network,
            #     abi_name="Amm_" + amm.split("-")[0].upper(),
            #     address=_str_to_addr(amm_contract_addr),
            # )
            amm_info = self.abi.get_contract(amm)
            amm_contract = _load_contract(
                self.w3,
                self.network,
                abi_name="Amm_" + amm.split("-")[0].upper(),
                address=_str_to_addr(amm_info['address']),
                abi=json.dumps(amm_info['abi'])
            )
            mbl = amm_contract.functions.getMaxBaseAssetLimit().call()
            return Response(StatusCode.OK.value, None, None, data={"max_base_asset_limit": round(mbl/10**18, 7)}).__dict__()
        except PolysynthException as e:
            return e.__dict__()

    def cancel_transaction(self, tx_hash: Optional[str] = None) -> Any:
        try:
            if tx_hash:
                try:
                    receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                    data = {"tx_hash": receipt["transactionHash"].hex()}
                    return Response(StatusCode.ALREADY_EXISTS.value, StatusCode.TRANSACTION_EXISTS.value, ErrorMessage.TRANSACTION_EXISTS.value, data=data).__dict__()
                except Exception as e:
                    pass

            tx_params = self._get_cancel_tx_params()
            receipt = None
            signed_txn = self.w3.eth.account.sign_transaction(
                tx_params, private_key=self.private_key)

            try:
                receipt = self.w3.eth.send_raw_transaction(
                    signed_txn.rawTransaction)
            finally:
                self.last_nonce = Nonce(tx_params["nonce"] + 1)

            try:
                tx = self.w3.eth.wait_for_transaction_receipt(
                    receipt, timeout=self.tx_timeout)
                result = {
                    "tx_hash": tx["transactionHash"].hex(),
                    "gas_fees": tx["gasUsed"],
                }
                if self.db.exists(tx_hash):
                    self.db.rem(tx_hash)
                    self.db.dump()  # delete the pending tx entry
                return Response(StatusCode.OK.value, None, None, data=result).__dict__()
            except TimeExhausted as te:
                return TransactionTimedOut(
                    StatusCode.REQUEST_TIMEOUT.value,
                    StatusCode.TRANSACTION_PENDING.value,
                    ErrorMessage.TRANSACTION_PENDING.value,
                    data={"tx_hash": receipt.hex()}).__dict__()
        except Exception as e:
            return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_NOT_CANCELLED.value, ast.literal_eval(str(e))).__dict__()

    def retry_transaction(self, tx_hash: str) -> Any:
        try:
            try:
                receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                data = {"tx_hash": receipt["transactionHash"].hex()}
                return Response(StatusCode.ALREADY_EXISTS.value, StatusCode.TRANSACTION_EXISTS.value, ErrorMessage.TRANSACTION_EXISTS.value, data=data).__dict__()
            except:
                pass

            func_name, func_params, nonce = self.db.get(tx_hash)
            func = self.manager_contract.find_functions_by_name(func_name)[
                0](*func_params)
            tx_params = self._get_retry_tx_params(nonce)

            receipt = None
            try:
                receipt = self._build_and_send_tx(func, tx_params)
            except Exception as e:
                return e
                # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

            tx = None
            try:
                tx = self.w3.eth.wait_for_transaction_receipt(
                    receipt, timeout=self.tx_timeout)
                result = {
                    "tx_hash": tx["transactionHash"].hex(),
                    "gas_fees": tx["gasUsed"],
                }
                if self.db.exists(tx_hash):
                    self.db.rem(tx_hash)
                    self.db.dump()  # delete the pendig tx entry
                return Response(StatusCode.OK.value, None, None, data=result).__dict__()
            except TimeExhausted as te:
                return TransactionTimedOut(
                    StatusCode.REQUEST_TIMEOUT.value,
                    StatusCode.TRANSACTION_PENDING.value,
                    ErrorMessage.TRANSACTION_PENDING.value,
                    data={"tx_hash": receipt.hex()}).__dict__()

        except Exception as e:
            return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.RETRY_FAILED.value, ast.literal_eval(str(e))).__dict__()

    def get_transaction_status(self, tx_hash: str) -> Any:
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            result = {
                "tx_hash": receipt["transactionHash"].hex(),
                "gas_fees": receipt["gasUsed"],
                "block_number": receipt["blockNumber"],
                "status": receipt["status"],
                "message": "Transaction Successful" if receipt["status"] == 1 else "Transaction Reverted"
            }
            return Response(StatusCode.OK.value, None, None, data=result).__dict__()
        except Exception as e:
            return TransactionFailedError(StatusCode.NOT_FOUND.value, StatusCode.TRANSACTION_NOT_FOUND.value, ErrorMessage.TRANSACTION_NOT_FOUND.value).__dict__()

    def check_trade_constraints(self, amm: str, dir: str, quoteAssetAmount: int, leverage: int, slippage: int) -> Any:
        try:
            _side = _side_str_to_int(dir)
            _check_collateral(quoteAssetAmount)
            _check_leverage(leverage)
            _check_slippage(slippage)

            # check wallet balance
            # self._check_wallet(quoteAssetAmount, leverage)
            # check price impact
            self._check_fluctuation(amm, quoteAssetAmount, leverage, _side)
        except TypeError:
            invalid_args = ""
            if not isinstance(amm, str):
                invalid_args += "market"
            if not isinstance(quoteAssetAmount, int):
                invalid_args += " quoteAssetAmount"
            if not isinstance(leverage, int):
                invalid_args += " leverage"
            if not(isinstance(slippage, int) or isinstance(slippage, float)):
                invalid_args += " slippage"

            raise InvalidParameterError(StatusCode.BAD_REQUEST.value, StatusCode.INVALID_ARG_TYPE.value,
                                        ErrorMessage.INVALID_ARG_TYPE.value % (invalid_args+" "))

    def _estimate_gas_fee_wrap(self, speed: str):
        if (self.gas_estimate_custom):
            res = self.gas_estimate_custom()
            if (("maxPriorityFee" in res) and ("maxFee" in res)):
                return res
            return InvalidGasEstimateFunction(StatusCode.BAD_REQUEST.value, StatusCode.INVALID_GAS_ESTIMATE_FUNCTION.value, ErrorMessage.INVALID_GAS_ESTIMATE_FUNCTION).__dict__()
        else:
            # return _estimate_gas_fee("standard", self.network)
            res = _estimate_gas_fee(speed, self.network)
            res["maxPriorityFee"] = res["maxPriorityFee"]
            res["maxFee"] = res["maxFee"]
            if speed == 'fast':
                res["maxPriorityFee"] = res["maxPriorityFee"] * 1.5
                res["maxFee"] = res["maxFee"] * 1.5
            return res

    def _input_price(self, amm: str, side: int, quoteAssetAmount: int) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        # amm_contract = _load_contract(
        #     self.w3,
        #     self.network,
        #     abi_name="Amm_" + amm.split("-")[0].upper(),
        #     address=_str_to_addr(amm_contract_addr),
        # )
        # price = amm_contract.functions.getInputPrice(
        #     _side_str_to_int(side),
        #     _int_to_bignum(quoteAssetAmount)
        # ).call()
        amm_info = self.abi.get_contract(amm)
        price = self.amm_reader_contract.functions.getBaseAssetAmount(
            amm_info['address'], _side_str_to_int(side), _int_to_bignum(quoteAssetAmount)).call()
        return price

    def _output_price(self, amm: str, side: int, baseAssetAmount: int) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        # amm_contract = _load_contract(
        #     self.w3,
        #     self.network,
        #     abi_name="Amm_" + amm.split("-")[0].upper(),
        #     address=_str_to_addr(amm_contract_addr),
        # )
        # price = amm_contract.functions.getOutputPrice(
        #     _side_str_to_int(side),
        #     _int_to_bignum(baseAssetAmount)
        # ).call()
        amm_info = self.abi.get_contract(amm)
        price = self.amm_reader_contract.functions.getStableTokenAmount(
            amm_info['address'], _side_str_to_int(side), _int_to_bignum(baseAssetAmount)).call()
        return price

    def _spot_price(self, amm, **kwargs) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

        amm_contract_info = self.abi.get_contract(amm)

        # amm_contract = _load_contract(
        #     self.w3,
        #     self.network,
        #     abi_name="Amm_" + amm.split("-")[0].upper(),
        #     address=_str_to_addr(amm_contract_info['address']),
        #     abi=json.dumps(amm_contract_info['abi'])
        # )
        price = self.amm_reader_contract.functions.getAmmMetadata(
            amm_contract_info['address']).call()[3]

        # price = amm_contract.functions.getSpotPrice().call()
        return price

    def _quote_asset_limit(self, amm: str, quoteAssetAmount: int, leverage: int, side: int, slippage: int) -> Any:
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        notional = int(quoteAssetAmount * leverage * 10**18)

        amm_reader = self.amm_reader_contract.functions
        reserve = amm_reader.getBaseAssetAmount(
            _amm_info['address'], side, notional).call()

        _positionSize = reserve[0]
        quoteAssetLimit = None

        if slippage == 0:
            quoteAssetLimit = _positionSize
        else:
            quoteAssetLimit = _positionSize * \
                (1-slippage) if side == 0 else _positionSize * (1+slippage)

        return quoteAssetLimit

    def _stable_asset_limit(self, amm: str, slippage: int) -> Any:
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        amm_reader = self.amm_reader_contract.functions

        # size owned by trader
        _size = self._trader_position(amm)[0]

        _side = 0 if _size > 0 else 1

        _sold_token = amm_reader.getStableTokenAmount(
            _amm_info['address'], _side, abs(_size)).call()[0]

        _stable_token_limit = _sold_token * \
            (1 - slippage) if _size > 0 else _sold_token*(1 + slippage)

        return _stable_token_limit

    def _trader_position(self, amm: str) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        amm_reader = self.amm_reader_contract.functions

        position = amm_reader.getTraderPosition(
            _amm_info['address'], self.address).call()
        return position

    def _trader_position_with_funding_payment(self, amm: str) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        amm_reader = self.amm_reader_contract.functions

        position = amm_reader.getTraderPositionWithFundingPayment(
            _amm_info['address'], self.address).call()
        return position

    def _unrealized_pnl(self, amm: str) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)

        position = self.manager_contract.functions.getPositionNotionalAndUnrealizedPnl(
            _amm_info['address'],
            self.address,
            PnlCalcOption.SPOT_PRICE.value).call()

        unrealized_pnl = position[1]
        return unrealized_pnl

    def _get_spot_price(self, amm: str, id='latest', **kwargs) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        # amm_contract = _load_contract(
        #     self.w3,
        #     self.network,
        #     abi_name="Amm_" + amm.split("-")[0].upper(),
        #     address=_str_to_addr(amm_contract_addr),
        # )
        amm_info = self.abi.get_contract(amm)
        amm_contract = _load_contract(
            self.w3,
            self.network,
            abi_name="Amm_" + amm.split("-")[0].upper(),
            address=_str_to_addr(amm_info['address']),
            abi=json.dumps(amm_info['abi'])
        )
        price = amm_contract.functions.getSpotPrice().call(block_identifier=id)
        return price

    def _get_trader_position_with_funding_payment(self, amm: str, trader: str, id='latest') -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        amm_reader = self.amm_reader_contract.functions

        position = amm_reader.getTraderPositionWithFundingPayment(
            _amm_info['address'], trader).call(block_identifier=id)
        return position

    def _get_trader_position(self, amm: str, trader: str, id='latest') -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        amm_reader = self.amm_reader_contract.functions

        position = amm_reader.getTraderPosition(
            _amm_info['address'], trader).call(block_identifier=id)
        return position

    def _get_position_notional_and_unrealized_pnl(self, amm: str, trader: str, id='latest', option=0) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)

        position = self.manager_contract.functions.getPositionNotionalAndUnrealizedPnl(
            _amm_info['address'],
            trader,
            option).call(block_identifier=id)

        return position

    def _get_collateral_with_funding_payment(self, amm, trader, id='latest', **kwargs) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")
        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        # amm_contract = _load_contract(
        #     self.w3,
        #     abi_name="Amm_" + amm.split("-")[0].upper(),
        #     address=_str_to_addr(amm_contract_addr),
        # )
        amm_info = self.abi.get_contract(amm)
        amm_contract = _load_contract(
            self.w3,
            self.network,
            abi_name="Amm_" + amm.split("-")[0].upper(),
            address=_str_to_addr(amm_info['address']),
            abi=json.dumps(amm_info['abi'])
        )

        position = self._get_trader_position(amm, trader, id=id)

        _spot = self._get_position_notional_and_unrealized_pnl(
            amm, trader, id=id, option=0)
        _twap = self._get_position_notional_and_unrealized_pnl(
            amm, trader, id=id, option=1)

        res = _spot if _spot[1] > _twap[1] else _twap

        price = amm_contract.functions.getCollateralWithFundingPayment(
            position, res[1]).call(block_identifier=id)
        return price

    def _get_collateral_ratio(self, amm: str, trader: str, id='latest') -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        try:
            ratio = self.manager_contract.functions.getCollateralRatio(
                _amm_info['address'], trader).call(block_identifier=id)
            return ratio
        except:
            return 0

    def _collateral_ratio(self, amm: str) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

        # amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        ratio = self.manager_contract.functions.getCollateralRatio(
            _amm_info['address'], self.address).call()
        return ratio

    def _price_impact(self, amm: str, quoteAssetAmount: int, leverage: int, side: int) -> Any:
        if amm is None:
            raise MissingInputError(StatusCode.BAD_REQUEST.value, StatusCode.MISSING_REQUIRED_ARGS.value,
                                    ErrorMessage.MISSING_REQUIRED_ARGS.value % "symbol")

        # _amm_contract_addr = _amm_name_to_addr(amm, self.network)
        _amm_info = self.abi.get_contract(amm)
        _notional = int(quoteAssetAmount * leverage * 10**18)

        amm_reader = self.amm_reader_contract.functions

        reserve = amm_reader.getBaseAssetAmount(
            _amm_info['address'], side, _notional).call()

        _base_reserve, _quote_reserve = reserve[1], reserve[2]
        _new_price = _quote_reserve/_base_reserve

        _curr_price = _normalize(self._spot_price(amm))

        fluctuation = abs(_curr_price - _new_price)/_curr_price

        return fluctuation

    def _check_fluctuation(self, amm: str, quoteAssetAmount: int, leverage: int, side: int) -> Any:
        fluctuation = self._price_impact(amm, quoteAssetAmount, leverage, side)
        if fluctuation > self.fluctuation_limit:
            raise InvalidParameterError(StatusCode.BAD_REQUEST.value, StatusCode.FLUCTUATION_LIMIT_EXCEEDED.value,
                                        ErrorMessage.FLUCTUATION_LIMIT_EXCEEDED.value % fluctuation)
        else:
            pass

    def _wallet_balance(self, **kwargs):
        stable_token = self.stable_token_contract.functions
        balance = stable_token.balanceOf(self.address).call()
        return balance

    def _check_wallet(self, quoteAssetAmount: int, leverage: int) -> Any:
        # check wallet balance
        balance = self._wallet_balance()/10**6

        # fees = 0.07 % of notional
        fees = 0.07 * (quoteAssetAmount * leverage)/100
        total_amount = quoteAssetAmount + fees

        if (total_amount > balance):
            raise InvalidParameterError(StatusCode.BAD_REQUEST.value, StatusCode.INSUFFICIENT_WALLET_BALANCE.value,
                                        ErrorMessage.INSUFFICIENT_WALLET_BALANCE.value % (balance, total_amount))
        else:
            pass

    def mint_token(self):
        stable_token = self.stable_token_contract.functions

        tx_params = self._get_tx_params()
        func = stable_token.mintFake()

        receipt = None
        try:
            receipt = self._build_and_send_tx(func, tx_params)
        except Exception as e:
            return e
            # return TransactionFailedError(StatusCode.FAILED_TRANSACTION.value, StatusCode.TRANSACTION_REVERTED.value, ast.literal_eval(str(e))).__dict__()

        tx = None
        try:
            tx = self.w3.eth.wait_for_transaction_receipt(
                receipt, timeout=self.tx_timeout)
        except TimeExhausted as te:
            self.db.set(receipt.hex(), (func, tx_params["nonce"]))
            self.db.dump()
            return TransactionTimedOut(
                StatusCode.REQUEST_TIMEOUT.value,
                StatusCode.TRANSACTION_PENDING.value,
                ErrorMessage.TRANSACTION_PENDING.value,
                data={"tx_hash": receipt.hex()})

    def _build_and_send_tx(
        self, function: Optional[ContractFunction], tx_params: Optional[TxParams] = None
    ) -> HexBytes:
        """Build and send a transaction."""
        if not tx_params:
            tx_params = self._get_tx_params()
        transaction = function.buildTransaction(tx_params)
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        try:
            return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        finally:
            logger.debug(f"nonce: {tx_params['nonce']}")
            self.last_nonce = Nonce(tx_params["nonce"] + 1)

    def _get_tx_params(self, value: Wei = Wei(0), gas: Wei = Wei(5000000)) -> TxParams:
        """Get generic transaction parameters."""
        gasFee = self._estimate_gas_fee_wrap('standard')
        return {
            "from": _addr_to_str(self.address),
            "value": value,
            "maxFeePerGas": Web3.toWei(gasFee['maxFee'], 'gwei'),
            'maxPriorityFeePerGas': Web3.toWei(gasFee['maxPriorityFee'], 'gwei'),
            "nonce": max(
                self.last_nonce, self.w3.eth.get_transaction_count(
                    self.address)
            ),
            "chainId": int(self.w3.net.version),
        }

    def _get_cancel_tx_params(self, value: Wei = Wei(0), gas: Wei = Wei(5000000)) -> TxParams:
        """Get generic transaction parameters."""
        gasFee = self._estimate_gas_fee_wrap('fast')
        return {
            "from": _addr_to_str(self.address),
            "to": "0x0000000000000000000000000000000000000000",
            "value": "0x0",
            "gas": gas,
            "maxFeePerGas": Web3.toWei(gasFee['maxFee'], 'gwei'),
            'maxPriorityFeePerGas': Web3.toWei(gasFee['maxPriorityFee'], 'gwei'),
            "nonce": max(
                self.last_nonce, self.w3.eth.get_transaction_count(
                    self.address)
            ),
            "chainId": int(self.w3.net.version),
        }

    def _get_retry_tx_params(self, nonce: int, value: Wei = Wei(0), gas: Wei = Wei(5000000)) -> TxParams:
        """Get generic transaction parameters."""
        gasFee = self._estimate_gas_fee_wrap('fast')
        return {
            "from": _addr_to_str(self.address),
            "value": value,
            "maxFeePerGas": Web3.toWei(gasFee['maxFee'], 'gwei'),
            'maxPriorityFeePerGas': Web3.toWei(gasFee['maxPriorityFee'], 'gwei'),
            "nonce": nonce,
            "chainId": int(self.w3.net.version),
        }

    # def create_amm_contracts(self):
