from fastapi import FastAPI
from app.api import routes_services, routes_incidents

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
app.include_router(routes_services.router)
app.include_router(routes_incidents.router)
