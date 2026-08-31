
import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import {LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer} from "recharts";
import "./styles.css";

const API = "http://localhost:8000";

function App() {
  const [scenarios, setScenarios] = useState([]);
  const [selected, setSelected] = useState("");
  const [seed, setSeed] = useState(42);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [scenarioConfig, setScenarioConfig] = useState({
    propagation_probability: 0.2,
    recovery_multiplier: 1.0,
    resource_budget: 8.0,
    resource_regen_per_hour: 1.0,
    intervention_delay_hours: 1.0,
    uncertainty_scale: 0.12,
  });

  useEffect(() => {
    async function loadScenarios() {
      try {
        const response = await fetch(`${API}/scenarios`);
        if (!response.ok) throw new Error(`Request failed with ${response.status}`);
        const data = await response.json();
        setScenarios(data);
        if (data.length) {
          const first = data[0];
          setSelected(first.scenario_id);
          setScenarioConfig({
            propagation_probability: first.propagation_probability,
            recovery_multiplier: 1.0,
            resource_budget: first.resource_budget,
            resource_regen_per_hour: 1.0,
            intervention_delay_hours: first.intervention_delay_hours,
            uncertainty_scale: first.uncertainty_scale,
          });
        }
      } catch (err) {
        setError(`Could not load scenarios: ${err.message}`);
      }
    }

    loadScenarios();
  }, []);

  useEffect(() => {
    const scenario = scenarios.find((s) => s.scenario_id === selected);
    if (!scenario) return;
    setScenarioConfig((prev) => ({
      ...prev,
      propagation_probability: scenario.propagation_probability,
      resource_budget: scenario.resource_budget,
      intervention_delay_hours: scenario.intervention_delay_hours,
      uncertainty_scale: scenario.uncertainty_scale,
    }));
  }, [selected, scenarios]);

  function updateScenarioConfig(field, value) {
    setScenarioConfig((prev) => ({
      ...prev,
      [field]: Number(value),
    }));
  }

  async function run() {
    if (!selected) return;
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API}/compare`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
          scenario_id: selected,
          seed: Number(seed),
          ...scenarioConfig,
        })
      });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Request failed with ${response.status}`);
      }
      setResult(await response.json());
    } catch (err) {
      setError(`Comparison failed: ${err.message}`);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const chartData = result ? result.baseline.timeline.map((b,i)=>({
    hour:b.hour,
    baseline:b.availability,
    adaptive:result.adaptive.timeline[i]?.availability ?? null
  })) : [];

  return (
    <div className="page">
      <h1>ResiliSim</h1>
      <p className="subtitle">Adaptive event-driven decision support</p>
      <div className="controls">
        <select value={selected} onChange={e=>setSelected(e.target.value)}>
          {scenarios.map(s=><option key={s.scenario_id}>{s.scenario_id}</option>)}
        </select>
        <input type="number" value={seed} onChange={e=>setSeed(e.target.value)}/>
        <button onClick={run} disabled={loading || !selected}>
          {loading ? "Comparing..." : "Compare policies"}
        </button>
      </div>

      <div className="controls controls--stacked">
        <label>
          Propagation probability
          <input type="number" min="0" max="1" step="0.01" value={scenarioConfig.propagation_probability} onChange={e=>updateScenarioConfig("propagation_probability", e.target.value)}/>
        </label>
        <label>
          Recovery multiplier
          <input type="number" min="0.1" step="0.05" value={scenarioConfig.recovery_multiplier} onChange={e=>updateScenarioConfig("recovery_multiplier", e.target.value)}/>
        </label>
        <label>
          Resource budget
          <input type="number" min="0" step="0.5" value={scenarioConfig.resource_budget} onChange={e=>updateScenarioConfig("resource_budget", e.target.value)}/>
        </label>
        <label>
          Resource regen/hour
          <input type="number" min="0" step="0.1" value={scenarioConfig.resource_regen_per_hour} onChange={e=>updateScenarioConfig("resource_regen_per_hour", e.target.value)}/>
        </label>
        <label>
          Intervention delay (h)
          <input type="number" min="0" step="0.5" value={scenarioConfig.intervention_delay_hours} onChange={e=>updateScenarioConfig("intervention_delay_hours", e.target.value)}/>
        </label>
        <label>
          Uncertainty scale
          <input type="number" min="0" max="1" step="0.01" value={scenarioConfig.uncertainty_scale} onChange={e=>updateScenarioConfig("uncertainty_scale", e.target.value)}/>
        </label>
      </div>

      {error && <div className="error">{error}</div>}

      {result && <>
        <div className="cards">
          {["baseline","adaptive"].map(p => <div className="card" key={p}>
            <h3>{p}</h3>
            <div>Recovery: {result[p].recovery_time_hours.toFixed(1)} h</div>
            <div>Disruption: {result[p].cumulative_disruption.toFixed(2)}</div>
            <div>Availability: {(100*result[p].mean_service_availability).toFixed(1)}%</div>
            <div>Resource utilization: {(100*result[p].resource_utilization).toFixed(1)}%</div>
          </div>)}
        </div>
        <div className="chart">
          <ResponsiveContainer width="100%" height={360}>
            <LineChart data={chartData}>
              <XAxis dataKey="hour"/><YAxis domain={[0,1]}/><Tooltip/><Legend/>
              <Line dataKey="baseline" dot={false}/>
              <Line dataKey="adaptive" dot={false}/>
            </LineChart>
          </ResponsiveContainer>
        </div>
      </>}
    </div>
  );
}
createRoot(document.getElementById("root")).render(<App/>);
