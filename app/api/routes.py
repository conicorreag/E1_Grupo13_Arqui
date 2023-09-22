from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from sqlalchemy.sql import cast
from sqlalchemy.types import DateTime
from database import crud
from database.models import Stock, Transaction
from database import database
import configparser
import json
from api.functions import create_list_from_stock_data, get_location
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()
config.read("credentials.secret")

HOST = config.get("Credentials", "HOST")
PORT = 9000
USER = config.get("Credentials", "USER")
PASSWORD = config.get("Credentials", "PASSWORD")
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
        object_stock = crud.create_stock(db, stock["stocks_id"], stock["datetime"], stock["symbol"], stock["shortName"], stock["price"], stock["currency"], stock["source"])
    print("Stocks created")


@router.get("/stocks")
def show_stocks(db: Session = Depends(database.get_db)):
    subquery = (
        db.query(Stock.symbol, func.max(cast(Stock.datetime, DateTime)).label("max_datetime"))
        .group_by(Stock.symbol)
        .subquery()
    )
    
    stocks_data = (
        db.query(Stock.shortName, Stock.symbol, Stock.price)
        .join(subquery, and_(Stock.symbol == subquery.c.symbol, cast(Stock.datetime, DateTime) == subquery.c.max_datetime))
        .group_by(Stock.shortName, Stock.symbol, Stock.price)
        .all()
    )
    
    stocks_formatted = "<br><br>".join([f"<strong>{name}</strong> (<strong>{symbol}</strong>) - Most recent price: {price}" for name, symbol, price in stocks_data])
    html_content = f"<html><body>{stocks_formatted}</body></html>"
    
    return HTMLResponse(content=html_content)





@router.get("/stocks/{symbol}")
def get_stocks_by_symbol_paginated(
    symbol: str = Path(..., title="Symbol"),
    page: int = Query(1, description="Page number", gt=0),
    size: int = Query(30, description="Number of events per page", gt=0),
    db: Session = Depends(database.get_db)
):
    # Realiza la consulta a la base de datos para obtener las filas con el symbol dado
    stocks_query = (
        db.query(Stock)
        .filter(Stock.symbol == symbol)
        .order_by(Stock.datetime)
    )

    total_events = stocks_query.count()
    stocks_paginated = stocks_query.offset((page - 1) * size).limit(size).all()

    # Genera el contenido HTML
    html_content = f"<html><body><h1>{symbol}</h1><table><tr><th>Datetime</th><th>Price</th><th>Currency</th><th>Source</th></tr>"
    
    for stock in stocks_paginated:
        html_content += f"<tr><td>{stock.datetime}</td><td>{stock.price}</td><td>{stock.currency}</td><td>{stock.source}</td></tr>"
    
    html_content += "</table>"

    # Agregar enlaces a las páginas anteriores y siguientes
    total_pages = (total_events - 1) // size + 1
    if page > 1:
        prev_page = page - 1
        html_content += f'<a href="?page={prev_page}&size={size}">Previous</a>'
    if page < total_pages:
        next_page = page + 1
        html_content += f'<a href="?page={next_page}&size={size}">Next</a>'

    html_content += "</body></html>"
    
    return HTMLResponse(content=html_content)
@router.post("/transactions/validate")
async def purchase_validation(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    purchase = data["request_id"]
    validation = data["valid"]
    return crud.validate_transaction(db,purchase,validation)

@router.post("/transactions")
async def purchase_request(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    ip = request.client.host
    location = get_location(ip)
    transaction = crud.create_transaction(db,user_id=data["user_id"],datetime=data["datetime"],symbol=data["symbol"],quantity=data["quantity"], location=location)
    request_id = transaction.id
    broker_message = {
        "request_id":request_id,
        "group_id":GROUP_ID,
        "symbol":data["symbol"],
        "datetime":data["datetime"],
        "deposit_token":"",
        "quantity":data["quantity"],
        "seller":0
    }
    client.connect(HOST, PORT)
    client.publish(TOPIC,json.dumps(broker_message))
    return transaction

@router.get("/transactions")
async def get_user_transactions(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    return crud.get_user_transactions(db, data["user_id"])

@router.put("/wallet")
async def update_user_wallet(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    return crud.update_user_wallet(db, data["user_id"], data["amount"])