from pydantic import BaseModel
from typing import List


class Incident(BaseModel):
    id: str
    service: str
    severity: str
    timestamp: str
    symptoms: List[str]
    logs: List[str]
    root_cause: str = ""
    resolution: str = ""
    outcome: str = "Open"