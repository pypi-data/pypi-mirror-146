import requests
from web3 import Web3
from polysynth.enum import ErrorMessage, StatusCode
from polysynth.exception import InvalidParameterError

from .constants import (
    _external_abis, _stable_contracts_usdc, _chainid_to_network_name)


path = "assets/"
addrs = ["matic", "mumbai", "local"]
toScrap = {"StableTokenFake": "StableToken", "Manager": "Manager", "Amm_ETH": "Amm_eth-usdc",
           "Amm_BTC": "Amm_btc-usdc", "Amm_MATIC": "Amm_matic-usdc", "AmmReader": "AmmReader"}


class ABI:
    def __init__(self, chain_id: int, network_name: str) -> None:
        self.chain_id = chain_id
        if network_name is None:
            network_name = _chainid_to_network_name[chain_id]

        r = requests.get(
            'https://protocol-meta.s3.ap-southeast-1.amazonaws.com/polysynth/'+str(chain_id)+'/'+network_name+'.json')

        try:
            data = r.json()
        except:
            raise('unable to parse contract config. contact support.')

        self.contracts = {}
        for key, value in data['contracts'].items():
            if (key in toScrap):
                self.contracts[toScrap[key]] = {
                    'address': value["address"],
                    'abi': value['abi']
                }

        if 'StableToken' not in self.contracts:
            self.contracts['StableToken'] = {
                'address': _stable_contracts_usdc[str(chain_id)],
                'abi': _external_abis['StableToken']
            }

    def get_contract(self, name: str):
        try:
            if 'USDC' in name or 'usdc' in name:
                name = "Amm_" + name.lower()
            return self.contracts[name]
        except:
            raise InvalidParameterError(
                StatusCode.BAD_REQUEST.value, StatusCode.UKNOWN_ADDRESS.value, ErrorMessage.INVALID_MARKET.value % name)
