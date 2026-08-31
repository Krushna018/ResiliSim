
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, spearmanr

METRICS = [
    "recovery_time_hours",
    "cumulative_disruption",
    "resource_utilization",
    "mean_service_availability",
]

def results_to_frame(results):
    rows = []
    for r in results:
        rows.append({
            "scenario_id": r.scenario_id,
            "policy": r.policy,
            "seed": r.seed,
            "recovery_time_hours": r.recovery_time_hours,
            "cumulative_disruption": r.cumulative_disruption,
            "resource_utilization": r.resource_utilization,
            "mean_service_availability": r.mean_service_availability,
            "interventions": r.interventions,
            "failed_components_peak": r.failed_components_peak,
            "event_count": r.event_count,
        })
    return pd.DataFrame(rows)

def paired_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for scenario_id, grp in df.groupby("scenario_id"):
        row = {"scenario_id": scenario_id}
        for m in METRICS:
            means = grp.groupby("policy")[m].mean()
            row[f"baseline_{m}"] = means.get("baseline", np.nan)
            row[f"adaptive_{m}"] = means.get("adaptive", np.nan)
            b = grp[grp.policy=="baseline"].sort_values("seed")[m].to_numpy()
            a = grp[grp.policy=="adaptive"].sort_values("seed")[m].to_numpy()
            if len(b) == len(a) and len(b) > 1 and np.any(b != a):
                try:
                    stat, p = wilcoxon(b, a)
                except ValueError:
                    p = 1.0
            else:
                p = 1.0
            row[f"{m}_wilcoxon_p"] = p
        out.append(row)
    return pd.DataFrame(out)

def sensitivity_analysis(df: pd.DataFrame, scenario_catalog) -> pd.DataFrame:
    meta = pd.DataFrame([{
        "scenario_id": s.scenario_id,
        "propagation_probability": s.propagation_probability,
        "resource_budget": s.resource_budget,
        "intervention_delay_hours": s.intervention_delay_hours,
        "uncertainty_scale": s.uncertainty_scale,
    } for s in scenario_catalog])
    merged = df.merge(meta, on="scenario_id")
    rows = []
    factors = [
        "propagation_probability",
        "resource_budget",
        "intervention_delay_hours",
        "uncertainty_scale",
    ]
    outcomes = ["recovery_time_hours","cumulative_disruption","mean_service_availability"]
    for policy, g in merged.groupby("policy"):
        for factor in factors:
            for outcome in outcomes:
                rho, p = spearmanr(g[factor], g[outcome])
                rows.append({
                    "policy": policy,
                    "factor": factor,
                    "outcome": outcome,
                    "spearman_rho": rho,
                    "p_value": p,
                })
    return pd.DataFrame(rows)
