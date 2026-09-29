import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from groq import Groq

from .prompts import SYSTEM_PROMPT
from .schemas import AgentOutput, HistoricalMatch


load_dotenv()


class IncidentInvestigationAgent:
    """AI agent that investigates incidents using current and historical evidence."""

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Add it to the project's .env file."
            )

        self.client = Groq(api_key=api_key)

        # Keep the model configurable so the team can change it
        # without modifying the agent implementation.
        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

    def investigate_incident(
        self,
        incident: Dict[str, Any],
        historical_memories: List[Dict[str, Any]] | None = None,
    ) -> AgentOutput:
        """
        Investigate a current incident using historical memories.

        Parameters:
            incident:
                The current incident and its available evidence.

            historical_memories:
                Previously resolved incidents retrieved from memory.

        Returns:
            A structured AgentOutput.
        """

        if historical_memories is None:
            historical_memories = []

        user_input = {
            "current_incident": incident,
            "historical_memories": historical_memories,
        }

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(user_input, indent=2),
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("The AI model returned an empty response.")

        try:
            result = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"The AI model returned invalid JSON: {content}"
            ) from exc

        return self._build_agent_output(result)

    @staticmethod
    def _build_agent_output(result: Dict[str, Any]) -> AgentOutput:
        """Convert the model's JSON response into our AgentOutput structure."""

        historical_matches = []

        for match in result.get("historical_matches", []):
            historical_matches.append(
                HistoricalMatch(
                    incident_id=str(match.get("incident_id", "")),
                    reason=str(match.get("reason", "")),
                )
            )

        try:
            confidence = float(result.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0

        # Keep confidence inside the expected range.
        confidence = max(0.0, min(1.0, confidence))

        evidence = result.get("evidence", [])

        if not isinstance(evidence, list):
            evidence = [str(evidence)]

        return AgentOutput(
            summary=str(result.get("summary", "")),
            root_cause=str(result.get("root_cause", "")),
            evidence=[str(item) for item in evidence],
            historical_matches=historical_matches,
            recommended_action=str(
                result.get("recommended_action", "")
            ),
            confidence=confidence,
        )


def investigate_incident(
    incident: Dict[str, Any],
    historical_memories: List[Dict[str, Any]] | None = None,
) -> AgentOutput:
    """
    Convenience function for the backend.

    Member 3 can later call this function directly.
    """

    agent = IncidentInvestigationAgent()

    return agent.investigate_incident(
        incident=incident,
        historical_memories=historical_memories,
    )