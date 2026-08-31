
from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .scenarios import build_scenario_catalog, scenario_by_id, scenario_with_overrides
from .simulation import run_paired_trial

app = FastAPI(title="ResiliSim API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompareRequest(BaseModel):
    scenario_id: str
    seed: int = 42
    propagation_probability: float | None = None
    recovery_multiplier: float | None = None
    resource_budget: float | None = None
    resource_regen_per_hour: float | None = None
    intervention_delay_hours: float | None = None
    uncertainty_scale: float | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/scenarios")
def scenarios():
    return [{
        "scenario_id": s.scenario_id,
        "family": s.family,
        "severity": s.severity,
        "resource_budget": s.resource_budget,
        "propagation_probability": s.propagation_probability,
        "intervention_delay_hours": s.intervention_delay_hours,
        "uncertainty_scale": s.uncertainty_scale,
    } for s in build_scenario_catalog()]

@app.post("/compare")
def compare(req: CompareRequest):
    try:
        s = scenario_by_id(req.scenario_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown scenario")

    overrides = {
        key: value for key, value in {
            "propagation_probability": req.propagation_probability,
            "recovery_multiplier": req.recovery_multiplier,
            "resource_budget": req.resource_budget,
            "resource_regen_per_hour": req.resource_regen_per_hour,
            "intervention_delay_hours": req.intervention_delay_hours,
            "uncertainty_scale": req.uncertainty_scale,
        }.items() if value is not None
    }
    if overrides:
        s = scenario_with_overrides(s, **overrides)

    baseline, adaptive = run_paired_trial(s, req.seed, keep_timeline=True)
    return {
        "scenario": req.scenario_id,
        "baseline": baseline.__dict__,
        "adaptive": adaptive.__dict__,
    }
