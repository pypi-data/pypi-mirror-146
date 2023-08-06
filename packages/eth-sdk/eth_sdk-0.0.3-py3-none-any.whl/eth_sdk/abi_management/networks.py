class NetworkNotSupported(Exception):
    pass


INFURA_PROJECT_URL = '4210ba8eb536423e8ae5d774c5064fa1'
ETHERSCAN_API_KEY = 'ICZKZRP33RIZSYZJSJJ1S1ZNU64CY3KDNG'
ARBITRUM_API_KEY = 'TEX3HHVFQIKWVBUVHR1ZN2Z2ZVP56JRM34'
AVALANCHE_API_KEY = 'GFMXK6EAYPYTFSSFUCYPWRYWU2HY4G85PZ'

network_ids = {
  'MAINNET': 1,
  'ROPSTEN': 3,
  'RINKEBY': 4,
  'GOERLI': 5,
  'KOVAN': 42,
  'ARBITRUM': 42161,
  'AVALANCHE': 43114
  # ARBITRUM_TESTNET = 421611,
}

network_api_urls = {
  network_ids['MAINNET']: 'https://api.etherscan.io/api',
  network_ids['ROPSTEN']: 'https://api-ropsten.etherscan.io/api',
  network_ids['RINKEBY']: 'https://api-rinkeby.etherscan.io/api',
  network_ids['GOERLI']: 'https://api-goerli.etherscan.io/api',
  network_ids['KOVAN']: 'https://api-kovan.etherscan.io/api',
  network_ids['ARBITRUM']: 'https://api.arbiscan.io/api',
  network_ids['AVALANCHE']: 'https://api.snowtrace.io/api'
  # network_ids['ARBITRUM_TESTNET']: 'https://api-testnet.arbiscan.io/api',
}

network_api_keys = {
  network_ids['MAINNET']: ETHERSCAN_API_KEY,
  network_ids['ROPSTEN']: ETHERSCAN_API_KEY,
  network_ids['RINKEBY']: ETHERSCAN_API_KEY,
  network_ids['GOERLI']: ETHERSCAN_API_KEY,
  network_ids['KOVAN']: ETHERSCAN_API_KEY,
  network_ids['ARBITRUM']: ARBITRUM_API_KEY,
  network_ids['AVALANCHE']: AVALANCHE_API_KEY
  # network_ids['ARBITRUM_TESTNET']: ARBITRUM_API_KEY,
}

rpc_providers = {
  network_ids['MAINNET']: f'https://mainnet.infura.io/v3/{INFURA_PROJECT_URL}',
  network_ids['ROPSTEN']: f'https://ropsten.infura.io/v3/{INFURA_PROJECT_URL}',
  network_ids['RINKEBY']: f'https://rinkeby.infura.io/v3/{INFURA_PROJECT_URL}',
  network_ids['GOERLI']: f'https://goerli.infura.io/v3/{INFURA_PROJECT_URL}',
  network_ids['KOVAN']: f'https://kovan.infura.io/v3/{INFURA_PROJECT_URL}',
  network_ids['ARBITRUM']: f'https://speedy-nodes-nyc.moralis.io/e1c5a8db51ab3e9318677d1d/arbitrum/mainnet',
  network_ids['AVALANCHE']: 'https://api.avax.network/ext/bc/C/rpc'
}


def get_network_id(network_name: str) -> str:
  network_name = network_name.upper()

  try:
    network_id = network_ids[network_name]
  except KeyError:
    raise NetworkNotSupported(f"Only the following networks are currently supported: {network_ids.keys()}")

  return network_id


def get_api_url(network_name: str) -> str:
  network_id = get_network_id(network_name)

  return network_api_urls[network_id]


def get_api_key(network_name: str) -> str:
  network_id = get_network_id(network_name)

  return network_api_keys[network_id]


def get_rpc_provider(network_name: str) -> str:
  network_id = get_network_id(network_name)

  return rpc_providers[network_id]