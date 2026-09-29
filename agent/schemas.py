from dataclasses import dataclass, field
from typing import List


@dataclass
class HistoricalMatch:
    incident_id: str
    reason: str


@dataclass
class AgentOutput:
    summary: str
    root_cause: str
    evidence: List[str] = field(default_factory=list)
    historical_matches: List[HistoricalMatch] = field(default_factory=list)
    recommended_action: str = ""
    confidence: float = 0.0