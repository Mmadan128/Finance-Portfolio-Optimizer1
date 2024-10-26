from web3 import Web3

# Create an instance of Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))  # Use a valid Infura/Alchemy URL

# Test the toChecksumAddress method
test_address = '0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD'  # A valid Ethereum address
try:
    checksum_address = w3.toChecksumAddress(test_address)
    print(f"Checksum Address: {checksum_address}")
except Exception as e:
    print(f"Error: {e}")
