import time
from web3 import Web3
from src.logger import logger
from src.config import PRIVATE_KEY, MIN_CONFIRMATIONS

def create_web3(rpc_url: str):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    return w3

def check_connection(w3):
    if not w3.is_connected():
        raise Exception("Web3 connection failed")
    logger.info("Connected to Sepolia")

def get_account(w3):
    return w3.eth.account.from_key(PRIVATE_KEY)

def get_balance(w3, address):
    return w3.eth.get_balance(address)

def send_transaction(w3, sender, recipient, value_wei):
    nonce = w3.eth.get_transaction_count(sender.address)

    estimated_gas = w3.eth.estimate_gas({
        'from': sender.address,
        'to': recipient,
        'value': value_wei
    })

    tx = {
        'to': recipient,
        'value': value_wei,
        'gas': estimated_gas,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'chainId': 11155111  # Sepolia
    }

    signed_tx = sender.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()

def wait_for_receipt(w3, tx_hash, timeout = 300, poll_interval = 3):
    logger.info("Polling until transaction receipt appears...")

    start = time.time()

    while True:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                logger.info(f"Transaction mined in block: {receipt.blockNumber}")
                return receipt
        except Exception:
            pass  

        if time.time() - start > timeout:
            raise TimeoutError(f"Transaction not confirmed within {timeout} seconds")

        time.sleep(poll_interval)


def wait_for_confirmations(w3, receipt, poll_interval = 3):
    logger.info(f"Waiting for confirmations (target: {MIN_CONFIRMATIONS})...")

    tx_block = receipt.blockNumber
    last_seen_block = None

    while True:
        current_block = w3.eth.block_number

        if current_block != last_seen_block:
            confirmations = current_block - tx_block + 1
            logger.info(f"New block: {current_block} → confirmations: {confirmations}")
            last_seen_block = current_block

            if confirmations >= MIN_CONFIRMATIONS:
                logger.info(f"Transaction finalized with {confirmations} confirmations ✅")
                return confirmations, current_block # 👈 chain_head

        time.sleep(poll_interval)