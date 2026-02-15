from fastapi import FastAPI, HTTPException, status
from schemas import TransactionRequest, RiskAssessment, TransactionStatus
from logic.rules import check_large_transaction, check_merchant_blacklist, check_velocity_limit
from logic.utils import mask_string
import uuid
import logging
import sys

app = FastAPI(title="Real-Time Risk Monitor")

@app.get("/")
async def health_check():
    return {"status": "online", "service": "Transaction Risk Monitor"}

# Logger
logging.basicConfig(
    level = logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger('risk-monitor')


@app.post(
    "/v1/assess-risk", 
    response_model=RiskAssessment, 
    status_code=status.HTTP_200_OK
)

async def assess_transaction_risk(transaction: TransactionRequest):

    masked_acc = mask_string(transaction.account_id)
    masked_ip = mask_string(transaction.ip_address, visible_start=4, visible_end=3)

    logger.info(f"Processing transaction: {transaction.transaction_id} for account: {masked_acc} | IP: {masked_ip}")
    
    # Receives a transaction, validates it via Pydantic, and returns a risk decision.
    total_score = 0
    triggered_rules = []

    large_transaction_score = check_large_transaction(transaction)
    if large_transaction_score > 0:
        total_score += large_transaction_score
        triggered_rules.append("LARGE_TRANSACTION_DETECTION")
    
    blacklist_score = check_merchant_blacklist(transaction)
    if blacklist_score > 0:
        total_score += blacklist_score
        triggered_rules.append("BLACKLISTED_MERCHANT_ATTEMPT")

    try:
        velocity_score = check_velocity_limit(transaction)
        if velocity_score > 0:
            total_score += velocity_score
            triggered_rules.append("VELOCITY_LIMIT_EXCEEDED")
    except Exception as e:
        # Mostly triggers when Redis is down
        print(f"Redis error: {e}")

    # Determines transaction's final risk score
    if total_score > 71:
        final_decision = TransactionStatus.DENY
    elif total_score >= 31:
        final_decision=TransactionStatus.REVIEW
    else: 
        final_decision=TransactionStatus.ALLOW

    # Logger decision
    logger.info(f"Decision for {transaction.transaction_id}: {final_decision} | Score: {total_score}")

    # Returns the assessment based on the response schema
    return RiskAssessment(
        transaction_id=transaction.transaction_id,
        decision=final_decision,
        risk_score=total_score,
        triggered_rules=triggered_rules
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)