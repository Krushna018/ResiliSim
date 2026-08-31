
from __future__ import annotations
import math
import random
from copy import deepcopy
from .models import ComponentState, SimulationResult
from .policies import BaselinePolicy, AdaptivePolicy

MAX_HOURS = 72
DT = 0.5

def _dependents(components):
    dep = {c.name: [] for c in components}
    for c in components:
        for d in c.dependencies:
            dep[d].append(c.name)
    return dep

def _service_availability(spec, states):
    weighted_total = sum(c.criticality for c in spec.components)
    weighted_up = sum(c.criticality for c in spec.components if states[c.name].available)
    return weighted_up / weighted_total

def _fail(name, comp_map, states, rng, scenario):
    st = states[name]
    if not st.available:
        return False
    comp = comp_map[name]
    st.available = False
    st.health = 0.0
    jitter = rng.gauss(1.0, scenario.uncertainty_scale)
    st.recovery_remaining = max(
        0.5, comp.base_recovery_hours * scenario.recovery_multiplier * max(jitter, 0.35)
    )
    return True

def run_simulation(scenario, policy, seed: int, keep_timeline: bool = False) -> SimulationResult:
    rng = random.Random(seed)
    comp_map = {c.name: c for c in scenario.components}
    dependents = _dependents(scenario.components)
    states = {c.name: ComponentState() for c in scenario.components}

    event_count = 0
    interventions = 0
    available_resource = scenario.resource_budget
    resource_spent = 0.0
    peak_failed = 0
    cumulative_disruption = 0.0
    availability_sum = 0.0
    steps = 0
    timeline = []

    for f in scenario.initial_failures:
        if _fail(f, comp_map, states, rng, scenario):
            event_count += 1

    t = 0.0
    while t <= MAX_HOURS:
        failed = [n for n, st in states.items() if not st.available]
        peak_failed = max(peak_failed, len(failed))

        # Dependency/uncertainty-driven propagation.
        new_failures = []
        for c in scenario.components:
            if not states[c.name].available:
                continue
            down_deps = sum(1 for d in c.dependencies if not states[d].available)
            if not down_deps:
                continue
            p = min(
                0.95,
                scenario.propagation_probability * down_deps *
                rng.uniform(1.0-scenario.uncertainty_scale, 1.0+scenario.uncertainty_scale)
            )
            if rng.random() < p * DT:
                new_failures.append(c.name)
        for n in new_failures:
            if _fail(n, comp_map, states, rng, scenario):
                event_count += 1

        failed = [n for n, st in states.items() if not st.available]

        # Recover resource pool over time and assign to failed components.
        available_resource = min(
            scenario.resource_budget,
            available_resource + scenario.resource_regen_per_hour * DT
        )
        if failed and t >= scenario.intervention_delay_hours:
            ranked = sorted(
                failed,
                key=lambda n: policy.priority(
                    comp_map[n],
                    states[n],
                    sum(1 for x in dependents[n] if not states[x].available)
                ),
                reverse=True,
            )
            budget_to_use = available_resource * policy.allocation_fraction(t, scenario)
            if budget_to_use > 1e-9:
                interventions += 1
            for n in ranked:
                if budget_to_use <= 1e-9:
                    break
                st = states[n]
                # One resource unit per half-hour can remove one hour of recovery work.
                alloc = min(1.0, budget_to_use, available_resource)
                st.allocated_resource = alloc
                st.recovery_remaining -= alloc * 1.3
                budget_to_use -= alloc
                available_resource -= alloc
                resource_spent += alloc

        # Natural recovery also progresses, but more slowly without intervention.
        for n in list(failed):
            st = states[n]
            st.recovery_remaining -= DT * 0.35
            if st.recovery_remaining <= 0:
                st.available = True
                st.health = 1.0
                st.recovery_remaining = 0.0
                st.allocated_resource = 0.0
                event_count += 1

        avail = _service_availability(scenario, states)
        availability_sum += avail
        cumulative_disruption += (1.0 - avail) * DT
        steps += 1
        if keep_timeline:
            timeline.append({
                "hour": round(t, 2),
                "availability": avail,
                "failed_components": sum(not s.available for s in states.values()),
                "available_resource": available_resource,
            })

        if all(st.available for st in states.values()):
            recovery_time = t
            break
        t += DT
    else:
        recovery_time = MAX_HOURS

    max_possible_resource = scenario.resource_budget + scenario.resource_regen_per_hour * max(recovery_time, DT)
    resource_utilization = min(1.0, resource_spent / max(max_possible_resource, 1e-9))
    mean_availability = availability_sum / max(steps, 1)

    return SimulationResult(
        scenario_id=scenario.scenario_id,
        policy=policy.name,
        seed=seed,
        recovery_time_hours=float(recovery_time),
        cumulative_disruption=float(cumulative_disruption),
        resource_utilization=float(resource_utilization),
        mean_service_availability=float(mean_availability),
        interventions=int(interventions),
        failed_components_peak=int(peak_failed),
        event_count=int(event_count),
        timeline=timeline,
    )

def run_paired_trial(scenario, seed: int, keep_timeline: bool = False):
    """One Monte Carlo trial compares baseline and adaptive policies under the same seed."""
    baseline = run_simulation(scenario, BaselinePolicy(), seed, keep_timeline)
    adaptive = run_simulation(scenario, AdaptivePolicy(), seed, keep_timeline)
    return baseline, adaptive
