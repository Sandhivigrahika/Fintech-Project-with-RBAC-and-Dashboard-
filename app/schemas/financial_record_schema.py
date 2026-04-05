from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from app.enums.enums import RecordCategory, RecordType
from typing import Optional

class FinancialRecordCreate(BaseModel):
    customer_name: str
    mobile_number: str
    amount: float = Field(gt=0) # must be greater than 0
    type: RecordType
    category: RecordCategory
    date: datetime
    notes: Optional[str] = None

    @field_validator("customer_name", "mobile_number")
    def strip_fields(cls, v):
        return v.strip()


class FinancialRecordUpdate(BaseModel):
    customer_name:Optional[str]  = None
    mobile_number: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[RecordCategory] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator("customer_name", "mobile_number")
    def strip_fields(cls, v):
        return v.strip()


class FinancialRecordResponse(BaseModel):

    id: int
    customer_name: str
    mobile_number: Optional[str]
    amount: float
    type: RecordType
    category: RecordCategory
    date: datetime
    notes: Optional[str]
    created_at: datetime
    model_config = {"from_attributes": True}

