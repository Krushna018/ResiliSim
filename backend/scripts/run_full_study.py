
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"backend"))

import pandas as pd
from resilisim.scenarios import build_scenario_catalog
from resilisim.simulation import run_paired_trial
from resilisim.analysis import results_to_frame, paired_summary, sensitivity_analysis

def main():
    scenarios = build_scenario_catalog()
    results = []
    paired_trials = 0

    for s in scenarios:
        for rep in range(50):
            seed = 10_000 + rep
            b, a = run_paired_trial(s, seed)
            results.extend([b, a])
            paired_trials += 1

    df = results_to_frame(results)
    out = ROOT/"results"
    out.mkdir(exist_ok=True)
    df.to_csv(out/"simulation_results.csv", index=False)

    summary = paired_summary(df)
    summary.to_csv(out/"paired_policy_summary.csv", index=False)

    sens = sensitivity_analysis(df, scenarios)
    sens.to_csv(out/"sensitivity_analysis.csv", index=False)

    print(f"Scenario families: {len(scenarios)}")
    print("Repetitions per scenario: 50")
    print(f"Monte Carlo paired trials: {paired_trials}")
    print(f"Policy-specific simulation executions: {len(df)}")
    print("Policies compared: baseline, adaptive")
    print("\nMean metrics by policy:")
    print(df.groupby("policy")[[
        "recovery_time_hours","cumulative_disruption",
        "resource_utilization","mean_service_availability"
    ]].mean().round(4).to_string())
    print("\nSaved results to:", out)

if __name__ == "__main__":
    main()
