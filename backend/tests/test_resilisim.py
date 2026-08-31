
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"backend"))

from resilisim.scenarios import build_scenario_catalog
from resilisim.simulation import run_paired_trial, run_simulation
from resilisim.policies import BaselinePolicy, AdaptivePolicy
from resilisim.analysis import results_to_frame, sensitivity_analysis

def test_exactly_30_scenarios():
    scenarios = build_scenario_catalog()
    assert len(scenarios) == 30
    assert len({s.scenario_id for s in scenarios}) == 30

def test_paired_trial_returns_both_policies():
    s = build_scenario_catalog()[0]
    b, a = run_paired_trial(s, seed=123)
    assert b.policy == "baseline"
    assert a.policy == "adaptive"
    assert b.scenario_id == a.scenario_id == s.scenario_id

def test_metrics_ranges():
    s = build_scenario_catalog()[-1]
    for p in [BaselinePolicy(), AdaptivePolicy()]:
        r = run_simulation(s, p, seed=7)
        assert r.recovery_time_hours >= 0
        assert r.cumulative_disruption >= 0
        assert 0 <= r.resource_utilization <= 1
        assert 0 <= r.mean_service_availability <= 1
        assert r.failed_components_peak >= 1

def test_reproducible_seed():
    s = build_scenario_catalog()[10]
    r1 = run_simulation(s, AdaptivePolicy(), seed=99)
    r2 = run_simulation(s, AdaptivePolicy(), seed=99)
    assert r1.recovery_time_hours == r2.recovery_time_hours
    assert r1.cumulative_disruption == r2.cumulative_disruption

def test_sensitivity_pipeline():
    scenarios = build_scenario_catalog()[:4]
    results = []
    for s in scenarios:
        for seed in [1,2,3]:
            results.extend(run_paired_trial(s, seed))
    df = results_to_frame(results)
    sens = sensitivity_analysis(df, scenarios)
    assert not sens.empty
    assert {"spearman_rho","p_value","factor","outcome","policy"} <= set(sens.columns)


def test_custom_scenario_overrides_are_applied():
    s = build_scenario_catalog()[0]
    custom = s
    custom = custom.__class__(
        scenario_id=s.scenario_id,
        family=s.family,
        severity=s.severity,
        initial_failures=s.initial_failures,
        propagation_probability=0.42,
        recovery_multiplier=1.25,
        resource_budget=9.0,
        resource_regen_per_hour=1.5,
        intervention_delay_hours=1.75,
        uncertainty_scale=0.18,
        components=s.components,
    )
    assert custom.propagation_probability == 0.42
    assert custom.resource_budget == 9.0
    assert custom.intervention_delay_hours == 1.75
    assert custom.uncertainty_scale == 0.18
