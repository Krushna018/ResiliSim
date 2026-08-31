
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class ComponentSpec:
    name: str
    capacity: float
    criticality: float
    base_recovery_hours: float
    dependencies: Tuple[str, ...] = ()

@dataclass(frozen=True)
class ScenarioSpec:
    scenario_id: str
    family: str
    severity: str
    initial_failures: Tuple[str, ...]
    propagation_probability: float
    recovery_multiplier: float
    resource_budget: float
    resource_regen_per_hour: float
    intervention_delay_hours: float
    uncertainty_scale: float
    components: Tuple[ComponentSpec, ...]

@dataclass
class ComponentState:
    available: bool = True
    health: float = 1.0
    recovery_remaining: float = 0.0
    allocated_resource: float = 0.0

@dataclass
class SimulationResult:
    scenario_id: str
    policy: str
    seed: int
    recovery_time_hours: float
    cumulative_disruption: float
    resource_utilization: float
    mean_service_availability: float
    interventions: int
    failed_components_peak: int
    event_count: int
    timeline: List[Dict[str, float]] = field(default_factory=list)
