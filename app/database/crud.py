from sqlalchemy.orm import Session
from . import models


def create_stock(db: Session, stocks_id: int, datetime: str, symbol: str, shortName: str, price: float, currency: str, source: str):
    stock = models.Stock(
        stocks_id=stocks_id,
        datetime=datetime,
        symbol=symbol,
        shortName=shortName,
        price=price,
        currency=currency,
        source=source
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def get_stock(db: Session, symbol: str):
    return db.query(models.Stock).filter(models.Stock.symbol == symbol).first() 

def create_transaction(db: Session,user_id:int,datetime:str,symbol:str,quantity:float):
    transaction = models.Transaction(
        user_id=user_id,
        datetime=datetime,
        symbol=symbol,
        quantity=quantity,
        status="waiting"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def validate_transaction(db: Session, request_id:int,validation:bool):
    transaction = db.query(models.Transaction).filter(models.Transaction.id ==request_id)
    if validation:
        transaction.status = "aproved"
    else:
        transaction.status = "rejected"
    db.commit()


