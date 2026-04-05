from fastapi import HTTPException
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.models.financial_record import FinancialRecord
from app.enums.enums import RecordType, RecordCategory
from app.centralised_helpers.normailze_phone_number import normalise_indian_mobile_number


#gets the overall financial summary of all users
def get_financial_summary_service(db: Session):

    total_income = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == RecordType.INCOME,
        FinancialRecord.is_deleted==False
    ).scalar() or 0

    total_expenses = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == RecordType.EXPENSE,
        FinancialRecord.is_deleted==False
    ).scalar() or 0


    net_balance = total_income - total_expenses

    total_customers = db.query(
        func.count(FinancialRecord.mobile_number.distinct())
    ).filter(
        FinancialRecord.is_deleted == False
    ).scalar() or 0


    return {
        "total_income" : round(total_income,2),
        "total_expense": round(total_expenses,2),
        "net_balance": round(net_balance,2),
        "total_customers": total_customers,
        "summary": f"Across {total_customers} customers, total income is ₹{round(total_income, 2)} "
                     f"against total expenses of ₹{round(total_expenses, 2)}. "
                     f"Net balance stands at ₹{round(net_balance, 2)}. "
    }

#get summary per user using their mobile number which is an index
def get_summary_customer_service(db: Session, mobile_number: str):
    base_filter = [FinancialRecord.is_deleted== False] #reusable filter to remove all the instances where record is_deleted=True

    if not mobile_number:
        raise HTTPException(400, "Mobile number is required")

    mobile_number = normalise_indian_mobile_number(mobile_number) #uses the helper from centralised_helpers

    base_filter.append(FinancialRecord.mobile_number == mobile_number)

    total_income = db.query(func.sum(FinancialRecord.amount)).filter(*base_filter,
                    FinancialRecord.type == RecordType.INCOME).scalar()

    if total_income is None:
        total_income =0

    total_expenses = db.query(func.sum(FinancialRecord.amount)).filter(
        *base_filter,
        FinancialRecord.type == RecordType.EXPENSE).scalar()

    if total_expenses is None:
        total_expenses =0

    net_balance = total_income - total_expenses

    #filter() = which rows -> count() = how many survived

    total_transactions = db.query(func.count(FinancialRecord.id)).filter(*base_filter).scalar()

    if total_transactions is None:
        total_transactions = 0


    return {
        "total_income": round(total_income,2),
        "total_expenses": round(total_expenses,2),
        "net_balance": round(net_balance,2),
        "total_transactions": total_transactions,
    }


def category_wise_summary(db: Session, category: RecordCategory):
    base_filter = [FinancialRecord.is_deleted== False,
                   FinancialRecord.category== category]


    total_income_category = (db.query(func.sum(FinancialRecord.amount))
                             .filter(*base_filter, FinancialRecord.type==RecordType.INCOME).scalar() or 0)

    total_expense_category = (db.query(func.sum(FinancialRecord.amount))
                              .filter(*base_filter,FinancialRecord.type==RecordType.EXPENSE).scalar() or 0)


    net_category = total_income_category - total_expense_category


    total_transactions = (db.query(func.count())
                          .filter(*base_filter).scalar()) or 0


    return {
        "category": category.value,
        "total_income": round(total_income_category, 2),
        "total_expense": round(total_expense_category,2),
        "net_amount": round(net_category,2),
        "total_transactions": total_transactions
    }


def recent_activity_customer(db: Session, mobile_number: str, limit: int =5):


    if not mobile_number:
        raise HTTPException(400, "Mobile number is required")

    mobile_number = normalise_indian_mobile_number(mobile_number)

    records = db.query(FinancialRecord).filter(
        FinancialRecord.mobile_number == mobile_number,
        FinancialRecord.is_deleted == False
    ).order_by(FinancialRecord.date.desc()).limit(limit).all()

    if not records:

        raise HTTPException(status_code=404, detail="No records found for this customer")

    return {
        "mobile_number": mobile_number,
        "recent_transactions": [
            {
                "id": r.id,
                "amount": r.amount,
                "type": r.type.value,
                "category": r.category.value,
                "date": r.date,
                "notes": r.notes
            } for r in records
        ]
    }


def monthly_trend_service(db: Session):
    results = db.query(
        extract("year", FinancialRecord.date).label("year"),
        extract("month", FinancialRecord.date).label("month"),
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.is_deleted == False
    ).group_by(
        "year",
        "month",
        FinancialRecord.type
    ).order_by(
        "year",
        "month"
    ).all()


    trends = {}

    for row in results:
        y = int(row.year)
        m = int(row.month)
        key = f"{y}-{m:02d}"

        if key not in trends:
            trends[key] = {"income":0, "expense":0}


        if row.type == RecordType.INCOME:
            trends[key]["income"] = round(row.total,2)
        else:
            trends[key]["expense"] = round(row.total,2)



    return {"monthly_trends": trends}












