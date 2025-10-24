from fastapi import FastAPI

# This is the ASGI app object that Uvicorn needs
app = FastAPI(
    title="Incident Tracker API",
    description="Monitors simulated outage data and reports incidents.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Incident Tracker API running!"}

"""Main FastAPI entrypoint for OutageSim.

- Initializes the FastAPI app.
- Includes routes from the /api package.
- Starts background monitoring task (scheduler).
"""
