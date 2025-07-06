from fastapi import FastAPI
from src.routes import tickets

app = FastAPI(
    title="TicketHub",
    description="API for managing and retrieving support tickets",
    version="1.0.0"
)

# Include the ticket routes under the /tickets prefix
app.include_router(tickets.router, prefix="/tickets")

# Basic health check endpoint
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

from src.routes import auth
app.include_router(auth.router, prefix="/auth")
from fastapi.openapi.utils import get_openapi


from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="TicketHub",
        version="1.0.0",
        description="Simple ticket system with optional JWT auth",
        routes=app.routes,
    )

    # Add BearerAuth so Swagger shows "Authorize" button
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply security only to protected endpoints
    for path, methods in openapi_schema["paths"].items():
        for method in methods.values():
            if "/tickets/stats" in path:
                method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
