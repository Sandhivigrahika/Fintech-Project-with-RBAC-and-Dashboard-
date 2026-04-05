'''
This file contains the business logic for
1. creating record
2. viewing record
3. updating record
4. Deleting record
5. Filtering record based on criteria such as date,category, or type
'''

from fastapi import HTTPException

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.enums.enums import RecordType, RecordCategory
from app.schemas.financial_record_schema import FinancialRecordCreate, FinancialRecordUpdate, FinancialRecordResponse
from app.models.financial_record import FinancialRecord
from app.centralised_helpers.normailze_phone_number import normalise_indian_mobile_number
import math




def create_financial_record_service(data: FinancialRecordCreate,
                                    db: Session,
                                    ):
    mobile_number = None
    if data.mobile_number:
        mobile_number = normalise_indian_mobile_number(data.mobile_number)
    try:
        record = FinancialRecord(
            customer_name=data.customer_name,
            mobile_number=mobile_number,
            amount=data.amount,
            type=data.type,
            category=data.category,
            date=data.date,
            notes=data.notes
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Unexpected error: {str(e)}",
    )

def get_financial_records_service(
        db: Session,
        #pagination
        page:int = 1,
        page_size: int = 10,
        customer_name: Optional[str] = None,
        mobile_number: Optional[str] = None,
        category: Optional[RecordCategory]= None,
        type: Optional[RecordType] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,

):
    #pagination guard
    if page<1:
        page =1
    if page_size <1:
        page_size =10
    elif page_size > 100:
        page_size = 100

    query = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)

    #apply filters if provided
    if mobile_number:
        mobile_number = normalise_indian_mobile_number(mobile_number)
        query = query.filter(FinancialRecord.mobile_number==mobile_number)

    if customer_name:
        query = query.filter(FinancialRecord.customer_name.ilike(f"%{customer_name}%")) #ilike  for case insensitivity

    if category:
        query = query.filter(FinancialRecord.category == category)

    if type:
        query = query.filter(FinancialRecord.type == type)

    '''date range filtering, date_from, date_to'''

    if date_from and date_to and date_from > date_to:
        raise HTTPException(400, "Invalid date range")

    if date_from:
        query = query.filter(FinancialRecord.date >= date_from)

    if date_to:
        query = query.filter(FinancialRecord.date <= date_to)



    #get total count before pagination
    total = query.count()

    #apply pagination
    records = query.order_by(FinancialRecord.date.desc(), FinancialRecord.id.desc()).offset((page-1) * page_size).limit(page_size).all()
    #used both date and id for ordering so that in case date is same, there's a fallback


    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total/page_size),
        "records": [FinancialRecordResponse.model_validate(r) for r in records]
    }



def update_financial_record_service (record_id : int,
                                     data: FinancialRecordUpdate,
                                     db: Session):



    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id, FinancialRecord
                                              .is_deleted==False).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    #only update the fields that are provided
    if data.customer_name is not None:
        record.customer_name = data.customer_name

    if data.mobile_number is not None:
        mobile_number = normalise_indian_mobile_number(data.mobile_number)
        record.mobile_number = mobile_number

    if data.amount is not None:
        record.amount = data.amount

    if data.type is not None:
        record.type = data.type

    if data.category is not None:
        record.category = data.category

    if data.date is not None:
        record.date = data.date
    if data.notes is not None:
        record.notes = data.notes


    try:
        db.commit()
        db.refresh(record)
        return {
            "message": "Record updated successfully",
            "record": FinancialRecordResponse.model_validate(record)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Unexpected error: {str(e)}")





def delete_financial_record(record_id: int,
                            db: Session
                              ):

    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()

    if not record:
         raise HTTPException(status_code=404, detail="Record not found")


    try:
        record.is_deleted = True
        db.commit()
        return {"message": f"Record {record_id} deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"unexpected error: {str(e)}")







