from fastapi import FastAPI
from routes import user_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(openapi_prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/ping', status_code=214)
def ping():
    return {'answer': 'pong'}

app.include_router(user_router)



