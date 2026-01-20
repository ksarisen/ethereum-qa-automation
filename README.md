# Ethereum Sepolia QA Automation Case

## Overview
This project automates an end-to-end validation of an ETH transfer on the Sepolia testnet.  
It demonstrates QA best practices including schema validation, logging, artifact generation, and secure configuration.

## Features
- Random ETH amount generation
- Balance before/after verification
- Transaction signing using private key
- RPC receipt validation
- Schema validation
- JSON artifact generation
- Logging to console and file
- Secure `.env` configuration

## Project Structure
src/
config.py # Environment config
client.py # Web3 client logic
main.py # Test flow
logger.py # Logging setup
artifacts/ # JSON outputs

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a .env file based on .env.example.

## Run
```bash
python3 -m src.main
```

## Output
Logs written to run.log
JSON artifacts written to artifacts/

## Security
Private key stored only in .env
.env excluded via .gitignore