from agent.agent import investigate_incident


incident = {
    "incident_id": "INC-002",
    "service": "payment-api",
    "severity": "high",
    "symptoms": [
        "API latency increased to 5.1 seconds",
        "HTTP 500 errors increased to 41%",
    ],
    "logs": [
        "Database connection pool exhausted",
        "ConnectionPoolTimeout",
    ],
}

historical_memories = [
    {
        "incident_id": "INC-001",
        "service": "payment-api",
        "severity": "high",
        "symptoms": [
            "High API latency",
            "Database connection failures",
        ],
        "root_cause": "Database connection pool exhaustion",
        "resolution": "Increased connection pool capacity and adjusted timeout settings",
    }
]


result = investigate_incident(
    incident=incident,
    historical_memories=historical_memories,
)


print("\n=== AGENT INVESTIGATION ===")
print("Summary:", result.summary)
print("Root cause:", result.root_cause)
print("Evidence:")

for item in result.evidence:
    print(" -", item)

print("Historical matches:")

for match in result.historical_matches:
    print(" -", match.incident_id, ":", match.reason)

print("Recommended action:", result.recommended_action)
print("Confidence:", result.confidence)