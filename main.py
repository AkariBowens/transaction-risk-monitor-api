from fastapi import FastAPI, HTTPException, status
from schemas import TransactionRequest, RiskAssessment, TransactionStatus
from logic.rules import check_large_transaction
import uuid

app = FastAPI(title="Real-Time Risk Monitor")

@app.get("/")

@app.post(
    "/v1/assess-risk", 
    response_model=RiskAssessment, 
    status_code=status.HTTP_200_OK
)

async def assess_transaction_risk(transaction: TransactionRequest):
    
    # Receives a transaction, validates it via Pydantic, and returns a risk decision.
    total_score = 0
    triggered_rules = []

    large_transaction_score = check_large_transaction(transaction)
    if large_transaction_score > 0:
        total_score += large_transaction_score
        triggered_rules.append("LARGE_TRANSACTION_DETECTION")

    # Determines transaction's final risk score
    if total_score > 71:
        final_decision = TransactionStatus.DENY
    elif total_score >= 31:
        final_decision=TransactionStatus.REVIEW
    else: 
        final_decision=TransactionStatus.ALLOW

    # 2. Returns the assessment based on the response schema
    return RiskAssessment(
        transaction_id=transaction.transaction_id,
        decision=final_decision,
        risk_score=total_score,
        triggered_rules=triggered_rules
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)