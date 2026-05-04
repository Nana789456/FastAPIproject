from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.core.security import auth_middleware
from app.api.v1.endpoints import send_sms, callbacks, status, blacklist


app = FastAPI(title="SMS Sender Microservice")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SMS Sender Microservice",
        version="1.0.0",
        description="Microservice for sending SMS",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {
            "type": "http",
            "scheme": "basic"
        }
    }
    openapi_schema["security"] = [{"basicAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


app.middleware("http")(auth_middleware)


app.include_router(send_sms.router, prefix="/v1", tags=["SMS"])
app.include_router(callbacks.router, prefix="/v1/callback", tags=["callbacks"])
app.include_router(status.router, prefix="/v1", tags=["status"])
app.include_router(blacklist.router, prefix="/v1", tags=["blacklist"])