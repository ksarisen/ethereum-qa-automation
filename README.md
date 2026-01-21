# Ethereum QA Automation Framework

End-to-end QA automation framework for Ethereum Sepolia testnet.  
This project demonstrates real-world SDET practices including JSON-RPC validation, schema validation, structured logging, artifact generation, confirmation tracking, and secure configuration.

It validates not only functional correctness, but also blockchain consistency using transaction mining and confirmation logic.

---

## Overview

This project automates an end-to-end ETH transfer validation flow on the Sepolia testnet.

The test flow includes:
- Reading recipient balance before transaction
- Generating a random transfer amount (0.001–0.01 ETH)
- Creating, signing and sending a transaction
- Polling until the transaction is mined
- Waiting for minimum blockchain confirmations
- Fetching and validating the transaction receipt
- Performing schema + semantic validation
- Verifying balance delta correctness
- Producing auditable JSON artifacts
- Logging all steps in a structured format

The goal is not only functional correctness, but also **maintainability, traceability, and clean test design**.

---

## Features

- End-to-end ETH transfer validation on Sepolia testnet
- Randomized, data-driven transaction amount generation (0.001–0.01 ETH)
- Secure transaction creation, signing, and broadcasting via JSON-RPC
- Transaction polling until mined, followed by confirmation-based finality validation
- Direct RPC validation of transaction fields (to, value)
- Schema and semantic validation of transaction receipt
- Balance delta verification (before vs after)
- Structured logging to console and file
- JSON artifact generation for auditability and traceability
- Duplicate transaction protection using transaction hash
- Secure configuration management using .env
- Modular, maintainable project structure (client / utils / validators separation)

---

## Confirmation Logic

A transaction is considered:

- **Mined** when it is included in a block (receipt available)
- **Confirmed** when additional blocks are added on top of its block

Confirmation count is calculated using:

The minimum number of confirmations is configurable via:

```python
MIN_CONFIRMATIONS = 3
```

The framework continuously polls the chain head and logs each new block until the required confirmation count is reached.

Example logs:

```yaml
Transaction mined in block: 10086656
Waiting for confirmations (target: 3)...
New block: 10086657 → confirmations: 2
New block: 10086658 → confirmations: 3
Transaction finalized with 3 confirmations
```

---

## Project Structure

```sql
src/
  config.py       # Environment & configuration
  client.py       # Web3 + RPC interactions
  main.py         # End-to-end test flow
  logger.py       # Logging configuration
  validators.py   # Schema & semantic validation
  utils.py        # Helper functions

artifacts/        # Generated JSON artifacts (gitignored)
run.log           # Execution logs (gitignored)
```

---

## Setup

Create virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a .env file (based on .env.example) and define:

```env
RPC_URL = https://sepolia.infura.io/v3/YOUR_KEY
PRIVATE_KEY = your_private_key_here
RECIPIENT_ADDRESS = 0xF2a0272d5D0122eafA508A0AfAa1176727A64EC6
MIN_CONFIRMATIONS = 3
MIN_AMOUNT = 0.001
MAX_AMOUNT = 0.01
```

---

## Run

```bash
python3 -m src.main
```

---

## Output

Each execution produces:
- Console + file logs (`run.log`)
- A JSON artifact under `artifacts/` structured into two layers:
  - `summary`: concise, human-readable test result and key metadata
  - `raw`: full transaction receipt returned by the JSON-RPC node
- The artifacts/ directory is created automatically at runtime if it does not exist.

Example artifact:

```json
{
  "summary": {
    "sender": "0x...",
    "receiver": "0x...",
    "amount_eth": 0.004271,
    "amount_wei": 4271000000000000,
    "tx_hash": "0x...",
    "block_number": 10081495,
    "block_hash": "0x...",
    "gas_used": 21000,
    "status": 1,
    "confirmations": 3,
    "network": "sepolia",
    "timestamp": "2026-01-20T06:42:00+03:00"
  },
  "raw": {
    "... full transaction receipt object ..."
  }
}
```

---

## Security Considerations

- Private key is never hardcoded
- Secrets are stored only in .env
- .env, logs and artifacts are excluded via .gitignore
- No sensitive data is committed to source control

---

## Technologies Used

- Python 3.9+
- web3.py
- JSON-RPC (Ethereum)
- jsonschema
- python-dotenv
- Logging module

---

## Author

Kerem Sarısen
QA / SDET focused on automation, reliability and clean test design.