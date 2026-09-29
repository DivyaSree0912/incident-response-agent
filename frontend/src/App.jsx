import { useState } from "react";
import "./App.css";

function App() {
  const [investigating, setInvestigating] = useState(false);
  const [resolving, setResolving] = useState(false);

  const [result, setResult] = useState(null);
  const [resolved, setResolved] = useState(false);
  const [error, setError] = useState("");

  const investigateIncident = async () => {
    setInvestigating(true);
    setError("");
    setResult(null);
    setResolved(false);

    try {
      const response = await fetch(
        "/api/incidents/INC-002/investigate",
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Investigation failed");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setInvestigating(false);
    }
  };

  const resolveIncident = async () => {
    setResolving(true);
    setError("");

    try {
      const response = await fetch(
        "/api/incidents/INC-002/resolve",
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to resolve incident");
      }

      await response.json();

      setResolved(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setResolving(false);
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header>
        <h1>Incident Response Agent</h1>

        <p>
          AI-powered incident investigation with historical memory
        </p>
      </header>

      <main>

        {/* CURRENT INCIDENT */}
        <section className="incident-card">

          <div className="incident-header">

            <div>
              <p className="label">
                CURRENT INCIDENT
              </p>

              <h2>INC-002</h2>
            </div>

            <span className="severity">
              HIGH
            </span>

          </div>

          <p>
            <strong>Service:</strong> payment-api
          </p>

          <h3>Symptoms</h3>

          <ul>
            <li>High latency</li>
            <li>Request timeouts</li>
          </ul>

          <h3>Logs</h3>

          <ul>
            <li>ConnectionPoolTimeout</li>
            <li>DB connection limit reached</li>
          </ul>

          {/* INVESTIGATE BUTTON */}
          <button
            onClick={investigateIncident}
            disabled={investigating}
          >
            {investigating
              ? "Investigating..."
              : "Investigate Incident"}
          </button>

          {/* RESOLVE BUTTON */}
          {result && !resolved && (
            <button
              onClick={resolveIncident}
              disabled={resolving}
              className="resolve-button"
            >
              {resolving
                ? "Resolving..."
                : "Resolve Incident"}
            </button>
          )}

          {/* SUCCESS MESSAGE */}
          {resolved && (
            <p className="success">
              ✅ Incident resolved successfully.
            </p>
          )}

          {/* ERROR MESSAGE */}
          {error && (
            <p className="error">
              ⚠️ {error}
            </p>
          )}

        </section>


        {/* HISTORICAL MEMORY */}
        {result?.historical_matches?.length > 0 && (
          <section className="memory-card">

            <p className="label">
              🧠 HISTORICAL MEMORY
            </p>

            <h2>
              Similar Incidents Found
            </h2>

            {result.historical_matches.map((match, index) => (
              <div
                className="memory"
                key={index}
              >

                <h3>
                  {match.incident_id}
                </h3>

                <p>
                  {match.reason}
                </p>

              </div>
            ))}

          </section>
        )}


        {/* AI INVESTIGATION RESULT */}
        {result && (
          <section className="investigation-card">

            <p className="label">
              🤖 AI INVESTIGATION
            </p>

            <h2>
              Investigation Result
            </h2>

            {/* SUMMARY */}
            {result.summary && (
              <>
                <h3>
                  Summary
                </h3>

                <p>
                  {result.summary}
                </p>
              </>
            )}

            {/* ROOT CAUSE */}
            {result.root_cause && (
              <>
                <h3>
                  Root Cause
                </h3>

                <p>
                  {result.root_cause}
                </p>
              </>
            )}

            {/* EVIDENCE */}
            {result.evidence?.length > 0 && (
              <>
                <h3>
                  Evidence
                </h3>

                <ul>
                  {result.evidence.map((item, index) => (
                    <li key={index}>
                      {item}
                    </li>
                  ))}
                </ul>
              </>
            )}

            {/* RECOMMENDATION */}
            {result.recommended_action && (
              <>
                <h3>
                  Recommendation
                </h3>

                <p>
                  {result.recommended_action}
                </p>
              </>
            )}

            {/* CONFIDENCE */}
            {result.confidence !== undefined && (
              <>
                <h3>
                  Confidence
                </h3>

                <p>
                  {Math.round(result.confidence * 100)}%
                </p>
              </>
            )}

          </section>
        )}


        {/* NO HISTORICAL MATCHES */}
        {result &&
          (!result.historical_matches ||
            result.historical_matches.length === 0) && (
            <section className="no-memory">

              <p className="label">
                HISTORICAL MEMORY
              </p>

              <p>
                No relevant historical incidents
                found.
              </p>

            </section>
          )}

      </main>
    </div>
  );
}

export default App;