from src.logger import logger

def validate_transaction_receipt(receipt, expected_recipient: str):
    """
    Performs both contract validation (structure/types) and semantic validation (business rules).
    """

    # --- Contract / Schema-level validations ---
    assert hasattr(receipt, "blockNumber"), "Missing field: blockNumber"
    assert hasattr(receipt, "status"), "Missing field: status"
    assert hasattr(receipt, "transactionHash"), "Missing field: transactionHash"
    assert hasattr(receipt, "blockHash"), "Missing field: blockHash"
    assert hasattr(receipt, "to"), "Missing field: to"

    assert isinstance(receipt.blockNumber, int), "blockNumber must be int"
    assert isinstance(receipt.status, int), "status must be int"

    # --- Semantic / Business validations ---
    assert receipt.status in [0, 1], "status must be 0 (fail) or 1 (success)"
    assert receipt.status == 1, "Transaction failed on-chain"

    assert receipt.transactionHash is not None, "transactionHash is null"
    assert receipt.blockHash is not None, "blockHash is null"

    assert receipt.to is not None, "Recipient address is null"
    assert receipt.to.lower() == expected_recipient.lower(), (
        f"Recipient mismatch: expected {expected_recipient}, got {receipt.to}"
    )

    logger.info("Receipt validation passed")
