# see: https://chainid.network/chains/
_netid_to_name = {
    137: "matic",
    80001: "mumbai",
    31337: "local"
}

_chainid_to_network_name = {
    137: 'matic_prod',
    80001: 'matic_test'
}

_contract_addresses_proxy_v1 = {
    "mumbai": {
        "StableToken": "0xd7BbeBAaF371284C91367f069036B9BE69bf8029",
        "Manager": "0x5F79C2bE1eC9B1B0221F244c48ba5137e9B33FD6",
        "Amm_eth-usdc": "0x01eD4fe17031b99286cAEF2d7D2f5d956bb01BF7",
        "Amm_btc-usdc": "0x60220aE888A00269E48109FBCedB093e86d927F6",
        "Amm_matic-usdc": "0xd859defa555cCb2139d9CDdd4CFaFD8eCbcb23C8",
        "AmmReader": "0xbFc95eEF9dB780dC3E438D41AB02f03BFA0DFF0F"
    },
    "local": {
        "StableToken": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
        "Manager": "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707",
        "Amm_eth-usdc": "0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82",
        "Amm_btc-usdc": "0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE",
        "Amm_matic-usdc": "0x59b670e9fA9D0A427751Af201D676719a970857b",
        "AmmReader": "0xB7f8BC63BbcaD18155201308C8f3540b07f84F5e"
    },
    "matic": {
        "StableToken": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
        "Manager": "0x6D171813A179520Dc5f1F62a699940eC537730F4",
        "Amm_eth-usdc": "0x44ecda99159270f6e2a328d3ae03d0aa2e4c6e89",
        "Amm_btc-usdc": "0x017af3e292554580671c6cf51321d2eda64de862",
        "Amm_matic-usdc": "0x2b538e01c3686d4a0a38657106c0cf442c74979f",
        "Amm_sol-usdc": "0x355b5f5a394ca7058bb853879cce8e5b13167432",
        "Amm_dot-usdc": "0x26691b6e1cb0f908926149fa58326ad4966d0aa5",
        "AmmReader": "0xe3774bF2EAc6716e1ef67B77AEcd6eBB3A2f84Ca"
    }
}

_contract_addresses_oracle = {
    "mumbai": {
        "eth-usdc": "0x0715A7794a1dc8e42615F059dD6e406A6594651A",
        "btc-usdc": "0x007A22900a3B98143368Bd5906f8E17e9867581b",
        "matic-usdc": "0xd0D5e3DB44DE05E9F294BB0a3bEEaF030DE24Ada",
    },
    "local": {
        "eth-usdc": "0x0715A7794a1dc8e42615F059dD6e406A6594651A",
        "btc-usdc": "0x007A22900a3B98143368Bd5906f8E17e9867581b",
        "matic-usdc": "0xd0D5e3DB44DE05E9F294BB0a3bEEaF030DE24Ada",
    },
    "matic": {
        "eth-usdc": "0xF9680D99D6C9589e2a93a78A04A279e509205945",
        "btc-usdc": "0xc907E116054Ad103354f2D350FD2514433D57F6f",
        "matic-usdc": "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0",
        "sol-usdc": "0x10C8264C0935b3B9870013e057f330Ff3e9C56dC",
        "dot-usdc": "0xacb51F1a83922632ca02B25a8164c10748001BdE",
    }
}

_external_abis = {
    'AggregatorV3InterfaceABI': [{"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "description", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint80", "name": "_roundId", "type": "uint80"}], "name": "getRoundData", "outputs": [{"internalType": "uint80", "name": "roundId", "type": "uint80"}, {"internalType": "int256", "name": "answer", "type": "int256"}, {"internalType": "uint256", "name": "startedAt", "type": "uint256"}, {"internalType": "uint256", "name": "updatedAt", "type": "uint256"}, {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "latestRoundData", "outputs": [{"internalType": "uint80", "name": "roundId", "type": "uint80"}, {"internalType": "int256", "name": "answer", "type": "int256"}, {"internalType": "uint256", "name": "startedAt", "type": "uint256"}, {"internalType": "uint256", "name": "updatedAt", "type": "uint256"}, {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "version", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}],
    'StableToken': [{"inputs": [{"internalType": "string", "name": "name_", "type": "string", }, {"internalType": "string", "name": "symbol_", "type": "string", }, ], "stateMutability": "nonpayable", "type": "constructor", }, {"anonymous": "false", "inputs": [{"indexed": "true", "internalType": "address", "name": "owner", "type": "address", }, {"indexed": "true", "internalType": "address", "name": "spender", "type": "address", }, {"indexed": "false", "internalType": "uint256", "name": "value", "type": "uint256", }, ], "name": "Approval", "type": "event", }, {"anonymous": "false", "inputs": [{"indexed": "true", "internalType": "address", "name": "from", "type": "address", }, {"indexed": "true", "internalType": "address", "name": "to", "type": "address", }, {"indexed": "false", "internalType": "uint256", "name": "value", "type": "uint256", }, ], "name": "Transfer", "type": "event", }, {"inputs": [{"internalType": "address", "name": "owner", "type": "address", }, {"internalType": "address", "name": "spender", "type": "address", }, ], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256", }, ], "stateMutability": "view", "type": "function", }, {"inputs": [{"internalType": "address", "name": "spender", "type": "address", }, {"internalType": "uint256", "name": "amount", "type": "uint256", }, ], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool", }, ], "stateMutability": "nonpayable", "type": "function", }, {"inputs": [{"internalType": "address", "name": "account", "type": "address", }, ], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256", }, ], "stateMutability": "view", "type": "function", }, {"inputs": [], "name":"decimals", "outputs":[{"internalType": "uint8", "name": "", "type": "uint8", }, ], "stateMutability": "view", "type": "function", }, {"inputs": [{"internalType": "address", "name": "spender", "type": "address", }, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256", }, ], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool", }, ], "stateMutability": "nonpayable", "type": "function", }, {"inputs": [{"internalType": "address", "name": "spender", "type": "address", }, {"internalType": "uint256", "name": "addedValue", "type": "uint256", }, ], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool", }, ], "stateMutability": "nonpayable", "type": "function", }, {"inputs": [], "name":"name", "outputs":[{"internalType": "string", "name": "", "type": "string", }, ], "stateMutability": "view", "type": "function", }, {"inputs": [], "name":"symbol", "outputs":[{"internalType": "string", "name": "", "type": "string", }, ], "stateMutability": "view", "type": "function", }, {"inputs": [], "name":"totalSupply", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256", }, ], "stateMutability": "view", "type": "function", }, {"inputs": [{"internalType": "address", "name": "recipient", "type": "address", }, {"internalType": "uint256", "name": "amount", "type": "uint256", }, ], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool", }, ], "stateMutability": "nonpayable", "type": "function", }, {"inputs": [{"internalType": "address", "name": "sender", "type": "address", }, {"internalType": "address", "name": "recipient", "type": "address", }, {"internalType": "uint256", "name": "amount", "type": "uint256", }, ], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool", }, ], "stateMutability": "nonpayable", "type": "function", }, ]
}

_stable_contracts_usdc = {
    '80001': '0xd7BbeBAaF371284C91367f069036B9BE69bf8029',
    '137': '0x2791bca1f2de4661ed88a30c99a7a9449aa84174'
}
