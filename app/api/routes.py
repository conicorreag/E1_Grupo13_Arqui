from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session
from database import crud
from database.models import Stock
from database import database
import json

from fastapi.responses import RedirectResponse 
from api.webpay import webpay_plus_create, webpay_plus_commit
from api.functions import create_list_from_stock_data, get_location, sumar_dias_a_fechas

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import httpx
load_dotenv()

HOST = os.getenv("HOST")
PORT = 9000
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
REQUESTS_TOPIC = "stocks/requests"
VALIDATION_TOPIC = "stocks/validation"
GROUP_ID = "13"
JOB_URL = "http://producer:8080/job"
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
    token_purchase = data["token"]
    status,token =  await webpay_plus_commit(data["token"])
    transaction = crud.validate_user_transaction(db, token_purchase, status)
    send_validation(transaction)
    crud.make_user_pay_transaction(db, transaction)
    return transaction
    

@router.patch("/transactions/general/")
async def set_validation(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    purchase = data["request_id"]
    validation = data["valid"]
    return crud.validate_general_transaction(db, purchase, validation)


@router.post("/transactions/general/")
async def purchase_request(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    transaction = crud.create_general_transaction(db, datetime=data["datetime"], symbol=data["symbol"], quantity=data["quantity"], request_id=data["request_id"])
    return transaction


@router.post("/transactions/")
async def purchase_request(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    ip = request.client.host
    location = get_location(ip)
    transaction = crud.create_user_transaction(db, user_sub=data["user_sub"], datetime=data["datetime"], symbol=data["symbol"], quantity=data["quantity"], location=location)
    response =  await webpay_plus_create(transaction.id, transaction.total_price)
    crud.add_token_to_transaction(db, transaction, response["token"])
    if (transaction.status != "rejected"):
        send_request(transaction,response["token"])
    return json.dumps({"url":response["url"],"request_id":transaction.request_id,"token":response["token"]})


def send_request(transaction,token):
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
    client.publish(REQUESTS_TOPIC, json.dumps(broker_message))


def send_validation(transaction):
    request_id = transaction.request_id
    is_valid = transaction.status == "approved"
    broker_message = {
        "request_id": request_id,
        "group_id": GROUP_ID,
        "seller": 0,
        "valid": is_valid
    }
    client.connect(HOST, PORT)
    client.publish(VALIDATION_TOPIC, json.dumps(broker_message))


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


@router.post("/create_prediction/")

# LE LLEGA {final_date: '2024-02-01', quantity: '8', symbol: 'AMZN', user_sub: 'google-oauth2|101188055086216254198'}

async def create_prediction(request: Request, db: Session = Depends(database.get_db)):
    request_data = await request.json()
    print("llegó a crear-----------------------")

    # sacar datos:  # {historial: [{fecha: 1/2/5, precio: 1}, {fecha: 132/5, precio: 12}], N: 3}
    today_date = datetime.today()
    future_date = datetime.strptime(request_data["final_date"], "%Y-%m-%d")
    days = (future_date - today_date).days
    initial_date = datetime.now() - timedelta(days=days)
   

    result = crud.get_historical_prices(db, request_data["symbol"], initial_date)

    # Formatear los resultados en la estructura deseada
    historical_prices = [{"fecha": entry.datetime, "precio": entry.price} for entry in result]
    historical_dates = [entry.datetime for entry in result]
    future_dates = sumar_dias_a_fechas(historical_dates, days)
    print("-------historical_dates-------")
    print(historical_dates)
    print("--------days--------")
    print(days)
    print("-------future_dates-------")
    print(future_dates)


    N = crud.get_N(db, request_data["symbol"])
    print("-------N-------")
    print(N)


    # Crear un diccionario final
    datos = {"historial": historical_prices, "N": N}
    
    async with httpx.AsyncClient() as client:
        response = await client.post("http://producer:8080/job", json=datos)
    
    print("-------response-------")
    print(response.json())
    job_id = response.json().get("job_id")
    crud.create_prediction(db=db, user_sub=request_data["user_sub"], job_id=job_id, symbol=request_data["symbol"], initial_date=today_date, final_date=request_data["final_date"], future_dates=future_dates, quantity=request_data["quantity"], final_price=0, future_prices=[])
    return response.json()



@router.get("/user_predictions/{user_sub}")
async def get_user_predictions(user_sub: str, db: Session = Depends(database.get_db)):
    predictions = crud.get_user_predictions(db, user_sub)
    for prediction in predictions:
        if prediction.status == "waiting":
            async with httpx.AsyncClient() as client:
                job_id = prediction.job_id
                response = await client.get(f"http://producer:8080/job/{job_id}")
                lista_ys = response.json().get("result")
            if lista_ys:
                crud.update_prediction(db, prediction.job_id, lista_ys)
    return crud.get_user_predictions(db, user_sub)


@router.get("/prediction/{prediction_id}")
async def get_prediction(prediction_id: int, db: Session = Depends(database.get_db)):
    return crud.get_prediction(db, prediction_id)
    

@router.get("/job_heartbeat/")
async def heartbeat_job():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://producer:8080/heartbeat")
    return response.json()