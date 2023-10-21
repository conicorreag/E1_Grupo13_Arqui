import os

# FastAPI
from fastapi import FastAPI, Request
from consumer import celery_app

# celery
from celery_config.tasks import make_prediction
from celery.result import AsyncResult

app = FastAPI()


@app.get("/job/{id}")
def get_job_result(id: str):
    # Get the result of a specific job by its ID
    result = AsyncResult(id, app=celery_app)
    if result.ready():
        return {"status": result.status, "result": result.result}
    else:
        return {"status": result.status, "result": None}
    

@app.post("/job")
async def create_job(request: Request):
    # Obtener los datos del request (por ejemplo, si esperas JSON en el cuerpo del request):
    request_data = await request.json()
    # Crear y enviar un trabajo a los workers con los datos del request usando delay
    job = make_prediction.delay(request_data)  # Pasar request_data como argumento
    return {
        "message": "job published",
        "job_id": job.id,
    }


@app.get("/heartbeat")
def heartbeat():
    return {"status": "true"}

