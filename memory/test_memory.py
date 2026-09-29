from memory.incident_memory import retain_incident, recall_incidents
from memory.hindsight_client import close_hindsight

# ============================================================
# INCIDENT 1
# This incident is already solved, so we store its solution.
# ============================================================

incident_1 = {
    "id": "INC-001",
    "service": "payment-api",
    "severity": "HIGH",
    "timestamp": "2026-09-28T10:30:00",
    "symptoms": [
        "high latency",
        "request timeouts"
    ],
    "logs": [
        "ConnectionPoolTimeout",
        "DB connection limit reached"
    ],
    "root_cause": "Database connection pool exhausted",
    "resolution": "Increased database connection pool size",
    "lessons": "Check connection pool when payment requests timeout"
}


print("\n==============================")
print("STEP 1: RETAIN INCIDENT 1")
print("==============================")

retain_result = retain_incident(incident_1)

print("Incident 1 retained!")
print(retain_result)


# ============================================================
# INCIDENT 2
# Notice that we DO NOT provide the root cause or resolution.
# Hindsight must find the previous incident.
# ============================================================

incident_2 = {
    "id": "INC-002",
    "service": "payment-api",
    "severity": "HIGH",
    "timestamp": "2026-09-29T11:15:00",
    "symptoms": [
        "slow payment requests",
        "request timeouts",
        "high database connections"
    ],
    "logs": [
        "PaymentRequestTimeout",
        "DB connection usage high"
    ]
}


print("\n==============================")
print("STEP 2: RECALL SIMILAR INCIDENTS")
print("==============================")

historical_matches = recall_incidents(incident_2)


print("\nHistorical matches found:")

if not historical_matches:
    print("No historical incidents found.")

else:
    for match in historical_matches:
        print("\n--------------------------------")
        print("Memory ID:", match["id"])
        print("Type:", match["type"])
        print("Context:", match["context"])
        print("Text:")
        print(match["text"])


print("\n==============================")
print("HINDSIGHT MEMORY TEST COMPLETE")
print("==============================")

close_hindsight()