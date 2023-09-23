from fastapi import FastAPI
from api import routes
from database.database import create_tables
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    # Otras URL permitidas si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(routes.router)

if __name__ == "__main__":
    create_tables()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
