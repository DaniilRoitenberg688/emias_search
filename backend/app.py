from fastapi import FastAPI
from routes import user_router

app = FastAPI(openapi_prefix='/api')

@app.get('/ping', status_code=214)
def ping():
    return {'answer': 'pong'}

app.include_router(user_router)



