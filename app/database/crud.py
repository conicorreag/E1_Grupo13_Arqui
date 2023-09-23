from sqlalchemy.orm import Session
from . import models
import uuid6


def create_stock(db: Session, stocks_id: int, datetime: str, symbol: str,
                 shortName: str, price: float, currency: str, source: str):
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

def create_transaction(db: Session,user_id:int,datetime:str,symbol:str,quantity:float,location):
    transaction = models.Transaction(
        user_id=user_id,
        datetime=datetime,
        symbol=symbol,
        quantity=quantity,
        status="waiting",
        location=location,
        request_id=uuid6.uuid7()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def validate_transaction(db: Session, request_id:int,validation:bool):
    transaction = db.query(models.Transaction).filter(models.Transaction.request_id ==request_id).first()
    if validation:
        transaction.status = "approved"
    else:
        transaction.status = "rejected"
    db.commit()
    db.refresh(transaction)
    return transaction

def get_user_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.datetime).all()

def update_user_wallet(db: Session, user_id: int, amount: float):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
    if not wallet:
        wallet = models.Wallet(user_id=user_id, balance=amount)
        db.add(wallet)
    else:
        wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet

def get_user_wallet(db: Session, user_id: int):
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()

