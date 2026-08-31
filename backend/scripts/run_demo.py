
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"backend"))

from resilisim.scenarios import build_scenario_catalog
from resilisim.simulation import run_paired_trial

def main():
    s = build_scenario_catalog()[16]
    b, a = run_paired_trial(s, seed=42, keep_timeline=True)
    print("Scenario:", s.scenario_id)
    for r in [b, a]:
        print(r.policy, {
            "recovery_time_hours": r.recovery_time_hours,
            "cumulative_disruption": round(r.cumulative_disruption, 3),
            "resource_utilization": round(r.resource_utilization, 3),
            "mean_service_availability": round(r.mean_service_availability, 3),
            "peak_failed": r.failed_components_peak,
        })

if __name__ == "__main__":
    main()
