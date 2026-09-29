from fastapi import FastAPI, HTTPException
from backend.models import Incident


app = FastAPI(title="Incident Response Agent")


# Temporary in-memory incident storage
incidents = [
    Incident(
        id="INC-001",
        service="payment-api",
        severity="HIGH",
        timestamp="2026-09-28T10:30:00",
        symptoms=[
            "high latency",
            "request timeouts"
        ],
        logs=[
            "ConnectionPoolTimeout",
            "DB connection limit reached"
        ],
        root_cause="Database connection pool exhaustion",
        resolution="Increase database connection pool size",
        outcome="Resolved"
    ),

    Incident(
        id="INC-002",
        service="payment-api",
        severity="HIGH",
        timestamp="2026-09-28T14:30:00",
        symptoms=[
            "high latency",
            "request timeouts"
        ],
        logs=[
            "ConnectionPoolTimeout",
            "DB connection limit reached"
        ],
        root_cause="",
        resolution="",
        outcome="Open"
    ),

    Incident(
        id="INC-003",
        service="auth-service",
        severity="MEDIUM",
        timestamp="2026-09-28T15:00:00",
        symptoms=[
            "login failures",
            "slow authentication"
        ],
        logs=[
            "RedisConnectionError"
        ],
        root_cause="Redis connection failure",
        resolution="Restart Redis connection pool",
        outcome="Resolved"
    )
]


@app.get("/")
def root():
    return {
        "message": "Incident Response Agent backend is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/incidents")
def get_incidents():
    return incidents


@app.get("/api/incidents/{incident_id}")
def get_incident(incident_id: str):

    for incident in incidents:
        if incident.id == incident_id:
            return incident

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )


@app.post("/api/incidents")
def create_incident(incident: Incident):

    for existing in incidents:
        if existing.id == incident.id:
            raise HTTPException(
                status_code=400,
                detail="Incident ID already exists"
            )

    incidents.append(incident)

    return {
        "message": "Incident created successfully",
        "incident": incident
    }
@app.post("/api/incidents/{incident_id}/investigate")
def investigate_incident(incident_id: str):

    for incident in incidents:
        if incident.id == incident_id:

            return {
                "summary": f"Investigation started for {incident.id}",
                "root_cause": incident.root_cause,
                "evidence": incident.logs,
                "historical_matches": [],
                "recommended_action": (
                    incident.resolution
                    if incident.resolution
                    else "No recommendation available yet."
                ),
                "confidence": 0.75
            }

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )
@app.post("/api/incidents/{incident_id}/resolve")
def resolve_incident(incident_id: str):

    for incident in incidents:
        if incident.id == incident_id:

            incident.outcome = "Resolved"

            return {
                "message": "Incident resolved successfully",
                "incident": incident
            }

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )