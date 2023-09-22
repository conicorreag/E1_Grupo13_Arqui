from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy.sql import cast
from sqlalchemy.types import DateTime
from database import crud
from database.models import Stock
from database import database
from api.functions import create_list_from_stock_data
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.post("/create_stocks/")
async def create_stock(request: Request,
                       db: Session = Depends(database.get_db)):
    data = await request.json()
    print(data)
    list_data = create_list_from_stock_data(data)
    for stock in list_data:
        crud.create_stock(db, stock["stocks_id"], stock["datetime"],
                          stock["symbol"], stock["shortName"], stock["price"],
                          stock["currency"], stock["source"])
    print("Stocks created")


@router.get("/stocks")
def show_stocks(db: Session = Depends(database.get_db)):
    subquery = (
        db.query(Stock.symbol, func.max(cast(Stock.datetime,
                                             DateTime)).label("max_datetime"))
        .group_by(Stock.symbol)
        .subquery()
    )

    stocks_data = (
        db.query(Stock.shortName, Stock.symbol, Stock.price)
        .join(subquery, and_(Stock.symbol == subquery.c.symbol, cast(
              Stock.datetime, DateTime) == subquery.c.max_datetime))
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
