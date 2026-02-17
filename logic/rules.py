import redis
from schemas import TransactionRequest
from decimal import Decimal

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=1)

LARGE_TRANSACTION_THRESHOLD = Decimal("10000.00")

# If transaction is greater than $10,000.00, adds 50 points to the risk score.
# Expects an integer
def check_large_transaction(tx: TransactionRequest) -> int:
    if tx.amount > LARGE_TRANSACTION_THRESHOLD:
        return 50
    return 0

# O(1) complexity
BLACKLISTED_MERCHANTS = {

    # Test merchants
    "MERCH_FRAUD_001",
    "EVIL_CORP_000",
    "SCAM_SQUARE_99"
}

def check_merchant_blacklist(tx: TransactionRequest) -> int:
    # If the merchant is in the list, returns 100 points, and auto denies
    if tx.merchant_id in BLACKLISTED_MERCHANTS:
        return 100
    return 0

def check_velocity_limit(tx: TransactionRequest) -> int:

    # If an account makes more than 3 transactions in one minute, add 80 points
    key = f"velocity:{tx.account_id}"

    current_count = redis_client.incr(key)

    # Starts time for velocity limit
    if current_count == 1:
        redis_client.expire(key, 60)

    if current_count > 3:
        return 80
    
    return 0