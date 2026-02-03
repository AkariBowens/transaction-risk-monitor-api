from schemas import TransactionRequest
from decimal import Decimal

LARGE_TRANSACTION_THRESHOLD = Decimal("10000.00")

# If transaction is greater than $10,000.00, adds 50 points to the risk score.
# Expects an integer
def check_large_transaction(tx: TransactionRequest) -> int:
    if tx.amount >= LARGE_TRANSACTION_THRESHOLD:
        return 50
    return 0

