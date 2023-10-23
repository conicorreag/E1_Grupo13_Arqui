from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session
from database import crud
from database.models import Stock
from database import database
import json
from fastapi.responses import RedirectResponse 
from api.webpay import webpay_plus_create, webpay_plus_commit
from api.functions import create_list_from_stock_data, get_location
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
load_dotenv()

HOST = os.getenv("HOST")
PORT = 9000
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TOPIC = "stocks/requests"
GROUP_ID = "13"
client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)


def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código:", rc)


def on_connect(client, userdata, flags, rc):
    print("Solicitud de compra enviada: ", rc)


router = APIRouter()


@router.post("/create_stocks/")
async def create_stock(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    print(data)
    list_data = create_list_from_stock_data(data)
    for stock in list_data:
        crud.create_stock(db, stock["stocks_id"], stock["datetime"], stock["symbol"], stock["shortName"], stock["price"], stock["currency"], stock["source"])


@router.get("/stocks")
def show_stocks(db: Session = Depends(database.get_db)):
    return crud.get_recent_stocks(db)


@router.get("/stocks/{symbol}")
def get_stocks_by_symbol_paginated(
    symbol: str = Path(..., title="Symbol"),
    page: int = Query(1, description="Page number", gt=0),
    size: int = Query(30, description="Number of events per page", gt=0),
    db: Session = Depends(database.get_db)
):
    stocks_query = (
        db.query(Stock)
        .filter(Stock.symbol == symbol)
        .order_by(Stock.datetime)
    )

    stocks_paginated = stocks_query.offset((page - 1) * size).limit(size).all()

    return stocks_paginated


@router.patch("/transactions/")
async def set_validation(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    purchase = data["request_id"]
    status,token =  await webpay_plus_commit(data["token"])
    if status == "approved":
        transaction = crud.validate_transaction(db, purchase, True)
        send_request(data, transaction , token)
        return status,token,transaction
    else:
        crud.validate_transaction(db, purchase, False)
        return status
    

@router.patch("/transactions/general/")
async def set_validation(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    purchase = data["request_id"]
    validation = data["valid"]
    return crud.validate_transaction(db, purchase, validation,True)

@router.post("/transactions/general/")
async def purchase_request(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    print(data)
    transaction = crud.create_transaction(db, user_sub=data["user_sub"], datetime=data["datetime"], symbol=data["symbol"], quantity=data["quantity"],transactions_general =True)
    print("transaccion general creada ", transaction)
    return transaction

@router.post("/transactions/")
async def purchase_request(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    print(data)
    ip = request.client.host
    location = get_location(ip)
    transaction,total_price = crud.create_transaction(db, user_sub=data["user_sub"], datetime=data["datetime"], symbol=data["symbol"], quantity=data["quantity"], location=location)
    response =  await webpay_plus_create(transaction.id,total_price)
    print(response)
    if (transaction.status != "rejected"):
        send_request(data, transaction,response["token"])
    return {"url":response["url"],"request_id":transaction.request_id,"token":response["token"]}


def send_request(data, transaction,token):
    request_id = transaction.request_id
    broker_message = {
        "request_id": request_id,
        "group_id": GROUP_ID,
        "symbol": transaction.symbol,
        "datetime": transaction.datetime,
        "deposit_token": token,
        "quantity": transaction.quantity,
        "seller": 0
    }
    client.connect(HOST, PORT)
    client.publish(TOPIC, json.dumps(broker_message))



@router.get("/transactions/{user_sub}")
async def get_user_transactions(user_sub: str, db: Session = Depends(database.get_db)):
    return crud.get_user_transactions(db, user_sub)


@router.put("/wallet/")
async def update_user_wallet(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    return crud.update_user_wallet(db, data["user_sub"], data["amount"])


@router.get("/wallet/{user_sub}")
async def get_user_wallet(user_sub: str, db: Session = Depends(database.get_db)):
    return crud.get_user_wallet(db, user_sub)
