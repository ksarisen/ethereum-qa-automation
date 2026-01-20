from web3 import Web3
from src.logger import logger
from src.config import PRIVATE_KEY, RPC_URL

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def check_connection():
    if not w3.is_connected():
        raise Exception("Web3 connection failed")
    logger.info("Connected to Sepolia")

def get_account():
    return w3.eth.account.from_key(PRIVATE_KEY)

def send_transaction(sender, recipient, value_wei):
    nonce = w3.eth.get_transaction_count(sender.address)

    tx = {
        'to': recipient,
        'value': value_wei,
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'chainId': 11155111  # Sepolia
    }

    signed_tx = sender.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    logger.info(f"Transaction sent: {tx_hash.hex()}")
    return tx_hash.hex()
