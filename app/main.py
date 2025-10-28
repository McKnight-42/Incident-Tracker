from fastapi import FastAPI
from app.api import incidents, services

app = FastAPI(
    title="Incident Tracker API",
    description="Monitors simulated outage data and reports incidents.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Incident Tracker API running!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Include routers
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
