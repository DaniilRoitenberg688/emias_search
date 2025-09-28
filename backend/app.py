from fastapi import FastAPI
from routes import user_router, scan_router, group_doc_router, storage_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles



app = FastAPI(
    docs_url=None,
    redoc_url=None,
    root_path='/api',
    title='Emias scanning system'
)
app.mount("/static", StaticFiles(directory="static"), name="static")

######### На проде CORS не нужен
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/api/openapi.json',
        title=app.title + " - Swagger UI",
        swagger_js_url="/api/static/swagger-ui-bundle.js",
        swagger_css_url="/api/static/swagger-ui.css",
        swagger_favicon_url="/api/static/favicon.png"
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url='/api/openapi.json',
        title=app.title + " - ReDoc",
        redoc_js_url="/api/static/redoc.standalone.js",
        redoc_favicon_url="/api/static/favicon.png",
        with_google_fonts=False,
    )

@app.get('/ping', status_code=214)
def ping():
    return {'answer': 'pong'}

app.include_router(user_router)
app.include_router(scan_router)
app.include_router(group_doc_router)
app.include_router(storage_router)



