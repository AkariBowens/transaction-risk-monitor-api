from fastapi import FastAPI, HTTPException, status
from schemas import TransactionRequest, RiskAssessment, TransactionStatus
import uuid

app = FastAPI(title="Real-Time Risk Monitor")

@app.post(
    "/v1/assess-risk", 
    response_model=RiskAssessment, 
    status_code=status.HTTP_200_OK
)

async def assess_transaction_risk(transaction: TransactionRequest):
    """
    Receives a transaction, validates it via Pydantic, 
    and returns a risk decision.
    """
    
    # 1. Placeholder for Risk Logic (Coming in Step 3)
    # For now, we simply 'ALLOW' everything that passes Pydantic validation.
    decision = TransactionStatus.ALLOW
    risk_score = 0
    triggered_rules = []

    # 2. Return the assessment based on the response schema
    return RiskAssessment(
        transaction_id=transaction.transaction_id,
        decision=decision,
        risk_score=risk_score,
        triggered_rules=triggered_rules
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)