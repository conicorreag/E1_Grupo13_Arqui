from fastapi import FastAPI
from api import routes
from database.database import create_tables

app = FastAPI()


app.include_router(routes.router)

if __name__ == "__main__":
    create_tables()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
