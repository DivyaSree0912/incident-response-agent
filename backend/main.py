from fastapi import FastAPI, HTTPException
from backend.models import Incident

from agent.agent import investigate_incident as run_agent_investigation
from memory.incident_memory import recall_incidents, retain_incident


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

            incident_data = incident.model_dump()

            # 1. Recall similar historical incidents from Hindsight
            historical_memories = recall_incidents(incident_data)

            # 2. Send current incident + historical memories to AI Agent
            result = run_agent_investigation(
                incident=incident_data,
                historical_memories=historical_memories,
            )

            # 3. Return the AI investigation result
            return result

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )
@app.post("/api/incidents/{incident_id}/resolve")
def resolve_incident(incident_id: str):

    for incident in incidents:
        if incident.id == incident_id:

            incident.outcome = "Resolved"

            # Store the resolved incident in Hindsight
            retain_incident(incident.model_dump())

            return {
                "message": "Incident resolved successfully",
                "incident": incident
            }

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )