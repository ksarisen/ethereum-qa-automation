import os
from dotenv import load_dotenv

load_dotenv()

NETWORK = "sepolia"

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS")
NETWORK = "sepolia"
MIN_CONFIRMATIONS = 3

MIN_AMOUNT = float(os.getenv("MIN_AMOUNT", 0.001))
MAX_AMOUNT = float(os.getenv("MAX_AMOUNT", 0.01))

if not RPC_URL:
    raise Exception("RPC_URL is missing")
if not PRIVATE_KEY:
    raise Exception("PRIVATE_KEY is missing")
if not RECIPIENT_ADDRESS:
    raise Exception("RECIPIENT_ADDRESS is missing")
