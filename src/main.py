import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import os
from src.logger import logger
from src.client import get_account, send_transaction, w3, check_connection
from src.config import MAX_AMOUNT, MIN_AMOUNT, RECIPIENT_ADDRESS, NETWORK

import random

def validate_receipt_schema(receipt):
    assert isinstance(receipt.blockNumber, int), "blockNumber must be int"
    assert isinstance(receipt.status, int), "status must be int"
    assert receipt.status in [0, 1], "status must be 0 or 1"
    assert receipt.transactionHash is not None, "transactionHash missing"
    assert receipt.blockHash is not None, "blockHash missing"
    assert receipt.to.lower() == RECIPIENT_ADDRESS.lower(), "Recipient mismatch"

    logger.info("Receipt schema validation passed")

def save_artifact(data):
    os.makedirs("artifacts", exist_ok = True)
    filename = f"artifacts/tx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f, indent = 2)

    logger.info(f"Artifact saved: {filename}")
    
def get_balance(address):
    return w3.eth.get_balance(address)

def generate_random_amount(min_eth, max_eth):
    amount = round(random.uniform(min_eth, max_eth), 6)
    logger.info(f"Random ETH amount: {amount}")

    return amount

def eth_to_wei(w3, eth_amount):
    return w3.to_wei(eth_amount, 'ether')

if __name__ == "__main__":
    check_connection()

    # Step 1: Balance before
    balance_before = get_balance(RECIPIENT_ADDRESS)
    logger.info(f"Balance before: {balance_before}")

    # Step 2: Random amount
    amount_eth = generate_random_amount(MIN_AMOUNT, MAX_AMOUNT)
    amount_wei = eth_to_wei(w3, amount_eth)

    # Step 3: Send transaction
    sender = get_account()
    tx_hash = send_transaction(sender, RECIPIENT_ADDRESS, amount_wei)

    # Step 4: Wait for confirmation
    logger.info("Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logger.info(f"Block: {receipt.blockNumber}")

    # Step 5: Schema validation
    validate_receipt_schema(receipt)   # Schema validation

    # Step 6: Balance after
    balance_after = get_balance(RECIPIENT_ADDRESS)
    logger.info(f"Balance after: {balance_after}")

    # Step 7: Assertion
    assert balance_after - balance_before == amount_wei, "Balance verification failed"
    logger.info("Balance verification passed")

    # Step 8: Artifact
    artifact = {
        "sender": sender.address,
        "receiver": RECIPIENT_ADDRESS,
        "amount_eth": amount_eth,
        "amount_wei": amount_wei,
        "tx_hash": tx_hash,
        "block_number": receipt.blockNumber,
        "block_hash": receipt.blockHash.hex(),
        "status": receipt.status,
        "timestamp": datetime.now(ZoneInfo("Europe/Istanbul")).isoformat(),
        "network": NETWORK
    }

    save_artifact(artifact)

    

    
