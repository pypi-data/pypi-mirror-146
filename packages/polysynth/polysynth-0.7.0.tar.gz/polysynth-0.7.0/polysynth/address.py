from typing import Dict

from web3 import Web3
from web3.types import ChecksumAddress


address_mumbai: Dict[str, ChecksumAddress] = {
    k: Web3.toChecksumAddress(v)
    for k, v in {
        "StableToken": "0x2E4c42aB89E8f928C74571Bb54C2DaA28605937B",
        "Manager": "0xc7Bf6E9a1EE40EB452712F219Ffd57D0feE0691c",
        "Amm_eth-usdc": "0x9fFeBA1A8cD88D0BDb996Cf75A993fdAfEE8f4f6",
        "Amm_btc-usdc": "0xec8c5521c4Df81be57436a5DC9e2Ac4C888E0054",
        "Amm_matic-usdc": "0x74456feE1Cf361787EA0545B7f075A72084a3965",
        "AmmReader": "0x314426488153C2867Dbb1FC1dee3B406F9E3c7B0"
    }.items()
}


address_matic: Dict[str, ChecksumAddress] = {
    k: Web3.toChecksumAddress(v)
    for k, v in {
        "StableToken": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",            
        "Manager": "0x84B056EB1107f8F8B127a57De0222A8A211C1e42",
        "Amm_eth-usdc": "0x80081DD1EEedbc8631c3077D4204bEa7270de891",
        "Amm_btc-usdc": "0xAE6dFb1923052890a077A135498F2B34A40F69Cc",
        "Amm_matic-usdc": "0x07429D7fDd2651d2712D87fd434669B1908dd5DA",
        "Amm_sol-usdc": "0xa23Ac746740cfE9013d94e62f7b0f1376EdCa759",
        "Amm_dot-usdc": "0x6F88D5D707908e961228C4708D19a6252B546e13",
        "AmmReader": "0x3e33b0FefD9C1886bd07C3308212f0f4a7c4A38d"
    }.items()
}