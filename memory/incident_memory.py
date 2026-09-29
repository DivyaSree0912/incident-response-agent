from memory.hindsight_client import hindsight, BANK_ID


def retain_incident(incident):
    content = f"""
Incident ID: {incident["id"]}

Service: {incident["service"]}

Severity: {incident["severity"]}

Timestamp: {incident["timestamp"]}

Symptoms:
{", ".join(incident["symptoms"])}

Logs:
{", ".join(incident["logs"])}

Root Cause:
{incident.get("root_cause", "Unknown")}

Resolution:
{incident.get("resolution", "Not provided")}

Lessons Learned:
{incident.get("lessons", "Not provided")}
"""

    result = hindsight.retain(
        bank_id=BANK_ID,
        content=content,
        context="production incident and resolution",
        metadata={
            "incident_id": incident["id"],
            "service": incident["service"],
            "severity": incident["severity"],
            "type": "incident"
        },
        document_id=f"incident_{incident['id']}"
    )

    return result


def recall_incidents(incident):
    query = f"""
Find previous incidents similar to this incident.

Current incident:

Service:
{incident["service"]}

Severity:
{incident["severity"]}

Symptoms:
{", ".join(incident["symptoms"])}

Logs:
{", ".join(incident["logs"])}

Find previous incidents with:
- similar symptoms
- similar logs
- similar service behavior
- similar failures
- useful previous resolutions
- relevant lessons learned
"""

    result = hindsight.recall(
        bank_id=BANK_ID,
        query=query
    )

    historical_matches = []

    for memory in result.results:
        historical_matches.append({
            "id": memory.id,
            "text": memory.text,
            "type": memory.type,
            "context": memory.context
        })

    return historical_matches