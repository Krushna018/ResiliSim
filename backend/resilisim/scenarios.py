
from __future__ import annotations
from .models import ComponentSpec, ScenarioSpec

def _components():
    return (
        ComponentSpec("power", 1.0, 1.00, 8.0, ()),
        ComponentSpec("network", 1.0, 0.95, 6.0, ("power",)),
        ComponentSpec("compute", 1.0, 0.90, 7.0, ("power","network")),
        ComponentSpec("database", 1.0, 0.95, 9.0, ("power","network","compute")),
        ComponentSpec("api", 1.0, 0.80, 4.0, ("network","compute","database")),
        ComponentSpec("frontend", 1.0, 0.55, 3.0, ("network","api")),
        ComponentSpec("dispatch", 1.0, 0.85, 6.0, ("network","database")),
        ComponentSpec("communications", 1.0, 0.90, 5.0, ("power","network")),
    )

FAMILIES = {
    "infrastructure_outage": ("power",),
    "network_partition": ("network",),
    "compute_failure": ("compute",),
    "data_service_failure": ("database",),
    "multi_service_degradation": ("api","dispatch"),
}

SEVERITIES = {
    "S1": dict(prop=0.08, rec=0.80, budget=8.0, regen=1.0, delay=0.0, unc=0.05),
    "S2": dict(prop=0.14, rec=0.95, budget=7.0, regen=0.9, delay=0.5, unc=0.08),
    "S3": dict(prop=0.20, rec=1.10, budget=6.0, regen=0.8, delay=1.0, unc=0.12),
    "S4": dict(prop=0.28, rec=1.25, budget=5.0, regen=0.7, delay=1.5, unc=0.16),
    "S5": dict(prop=0.36, rec=1.45, budget=4.0, regen=0.6, delay=2.0, unc=0.20),
    "S6": dict(prop=0.45, rec=1.70, budget=3.5, regen=0.5, delay=3.0, unc=0.25),
}

def build_scenario_catalog() -> list[ScenarioSpec]:
    """Return exactly 30 scenario families: 5 disruption families × 6 severities."""
    comps = _components()
    out = []
    for family, initial in FAMILIES.items():
        for sev, cfg in SEVERITIES.items():
            out.append(
                ScenarioSpec(
                    scenario_id=f"{family}-{sev}",
                    family=family,
                    severity=sev,
                    initial_failures=initial,
                    propagation_probability=cfg["prop"],
                    recovery_multiplier=cfg["rec"],
                    resource_budget=cfg["budget"],
                    resource_regen_per_hour=cfg["regen"],
                    intervention_delay_hours=cfg["delay"],
                    uncertainty_scale=cfg["unc"],
                    components=comps,
                )
            )
    assert len(out) == 30
    return out

def scenario_by_id(scenario_id: str) -> ScenarioSpec:
    for s in build_scenario_catalog():
        if s.scenario_id == scenario_id:
            return s
    raise KeyError(scenario_id)


def scenario_with_overrides(base: ScenarioSpec, **overrides) -> ScenarioSpec:
    """Return a new scenario using the provided overrides while preserving the rest."""
    values = {
        "scenario_id": base.scenario_id,
        "family": base.family,
        "severity": base.severity,
        "initial_failures": base.initial_failures,
        "propagation_probability": base.propagation_probability,
        "recovery_multiplier": base.recovery_multiplier,
        "resource_budget": base.resource_budget,
        "resource_regen_per_hour": base.resource_regen_per_hour,
        "intervention_delay_hours": base.intervention_delay_hours,
        "uncertainty_scale": base.uncertainty_scale,
        "components": base.components,
    }
    values.update(overrides)
    return ScenarioSpec(**values)
