from web3 import Account
from src.client import create_web3, check_connection, get_balance, send_transaction, wait_for_confirmations, wait_for_receipt
from src.config import *
from src.logger import logger
from src.utils import generate_random_amount, normalize_for_json, save_artifact, is_duplicate_tx, get_timestamp_tr
from src.validators import validate_transaction_receipt

def main():
    w3 = create_web3(RPC_URL)
    check_connection(w3)

    sender = Account.from_key(PRIVATE_KEY)

    # Step 1: Balance before
    balance_before = get_balance(w3, RECIPIENT_ADDRESS)
    logger.info(f"Balance before: {balance_before} wei ({float(w3.from_wei(balance_before, 'ether'))} ETH)")

    # Step 2: Random amount
    amount_eth = generate_random_amount(MIN_AMOUNT, MAX_AMOUNT)
    amount_wei = int(w3.to_wei(amount_eth, "ether"))
    logger.info(f"Random ETH amount: {amount_eth} ETH ({amount_wei} wei)")

    # Step 3: Send transaction
    tx_hash = send_transaction(w3, sender, RECIPIENT_ADDRESS, amount_wei)
    logger.info(f"Transaction sent: {tx_hash}")

    # Step 4: Wait for confirmation
    receipt = wait_for_receipt(w3, tx_hash)

    # Step 5: Wait for confirmations
    confirmations, chain_head = wait_for_confirmations(w3, receipt)

    # Step 6: Verify result.to and result.value (eth_getTransactionByHash equivalent)
    tx = w3.eth.get_transaction(tx_hash)

    assert tx["to"].lower() == RECIPIENT_ADDRESS.lower(), "Recipient mismatch in transaction"
    assert tx["value"] == amount_wei, "Amount mismatch in transaction"

    logger.info("Transaction fields (to, value) verified via RPC")

    # Step 7: Schema validation
    validate_transaction_receipt(receipt, RECIPIENT_ADDRESS)

    # Step 8: Balance after
    balance_after = get_balance(w3, RECIPIENT_ADDRESS)
    logger.info(f"Balance after: {balance_after} wei ({float(w3.from_wei(balance_after, 'ether'))} ETH)")

    # Step 9: Balance assertion
    assert balance_after - balance_before == amount_wei, "Balance verification failed"
    logger.info("Balance verification passed")

    # Step 10: Artifact
    artifact = {
        "summary": {
            "sender": sender.address,
            "receiver": RECIPIENT_ADDRESS,
            "amount_eth": amount_eth,
            "amount_wei": amount_wei,
            "tx_hash": tx_hash,
            "block_number": receipt.blockNumber,
            "block_hash": receipt.blockHash.hex(),
            "chain_head": chain_head,
            "gas_used": receipt.gasUsed,
            "status": receipt.status,
            "confirmations": confirmations,
            "network": NETWORK,
            "timestamp": get_timestamp_tr(),
        },
        "raw_full_receipt": normalize_for_json(dict(receipt))
    }

    # Step 11: Duplicate check
    if is_duplicate_tx(tx_hash):
        logger.warning("Duplicate transaction detected, artifact not saved.")
    else:
        save_artifact(artifact)

if __name__ == "__main__":
    main()