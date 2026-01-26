#Boilerplate created using Gemini
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CurrencyCode(str, Enum):
    """ISO 4217 Currency Codes"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    # Add others as needed

class TransactionStatus(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    DENY = "DENY"

class TransactionRequest(BaseModel):
    # Strict mode prevents Pydantic from "coercing" data (e.g., turning a float into an int)
    model_config = ConfigDict(strict=True)

    transaction_id: UUID = Field(description="Unique identifier for the transaction")
    account_id: str = Field(min_length=5, max_length=20, pattern=r"^[A-Z0-9]+$")
    
    # Financial data MUST use Decimal, not float
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)] 
    currency: CurrencyCode
    
    merchant_id: str
    merchant_category_code: str = Field(pattern=r"^\d{4}$", description="4-digit MCC code")
    
    ip_address: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("timestamp")
    @classmethod
    def ensure_not_in_future(cls, v: datetime) -> datetime:
        if v > datetime.now(timezone.utc):
            raise ValueError("Transaction timestamp cannot be in the future")
        return v

class RiskAssessment(BaseModel):
    """The response schema your API sends back"""
    transaction_id: UUID
    decision: TransactionStatus
    risk_score: int = Field(ge=0, le=100)
    triggered_rules: list[str] = []
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))