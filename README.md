# ResiliSim

# ResiliSim: Adaptive Event-Driven Decision Support Platform

ResiliSim is a research-oriented discrete-event simulation and interactive
decision-support system for studying resilience under cascading disruptions.

## What is implemented

- exactly **30 scenario families** (5 disruption types × 6 severities)
- dependency-driven cascading failure model
- uncertain propagation and recovery times
- constrained intervention resources
- delayed response
- baseline and adaptive response policies
- recovery time, cumulative disruption, resource utilization, and service availability
- paired Monte Carlo experimentation
- full **1,500-trial research runner**
- paired Wilcoxon policy comparisons
- sensitivity analysis using Spearman correlations
- FastAPI backend
- React dashboard for interactive scenario/policy comparison

## Resume-aligned experiment

The full study is intentionally structured as:

**30 scenario families × 50 independent stochastic repetitions = 1,500 paired Monte Carlo trials**

Each trial evaluates both baseline and adaptive response policies under the same
random seed, resulting in 3,000 policy-specific simulation records.

This paired design is stronger experimentally than running unrelated seeds for the
two policies.

## Run the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn resilisim.api:app --reload
```

API docs:
`http://localhost:8000/docs`

## Run a simulation demo

```bash
cd backend
python scripts/run_demo.py
```

## Run the complete 1,500-trial study

```bash
cd backend
python scripts/run_full_study.py
```

Generated outputs:
- `results/simulation_results.csv`
- `results/paired_policy_summary.csv`
- `results/sensitivity_analysis.csv`

## Run tests

```bash
cd backend
pytest -q
```

## Run the React interface

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the Vite URL printed in the terminal.

## Project structure

```text
ResiliSim/
├── backend/
│   ├── resilisim/
│   │   ├── api.py
│   │   ├── analysis.py
│   │   ├── models.py
│   │   ├── policies.py
│   │   ├── scenarios.py
│   │   └── simulation.py
│   ├── scripts/
│   └── tests/
├── frontend/
│   └── src/
├── docs/
│   └── research_design.md
└── results/
```

## Resume note

The code structurally supports the 30-scenario and 1,500-trial claims. Run the
full study before claiming that the 1,500-trial experiment was *conducted*.
Any specific percentage improvement between baseline and adaptive policies
should be calculated from the generated CSV results rather than predetermined.
