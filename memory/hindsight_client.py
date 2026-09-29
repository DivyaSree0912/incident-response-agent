import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

if not API_KEY:
    raise ValueError("HINDSIGHT_API_KEY is missing")

if not BANK_ID:
    raise ValueError("HINDSIGHT_BANK_ID is missing")


hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=API_KEY
)


def close_hindsight():
    """Close the Hindsight HTTP client."""
    hindsight.close()