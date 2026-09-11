# ResiliSim — Adaptive Event-Driven Decision Support Platform

> A research-oriented simulation and interactive decision-support platform for studying resilience under cascading failures, uncertainty, resource constraints, and delayed intervention.

ResiliSim models how disruptions propagate through interdependent systems and compares **baseline vs. adaptive response policies** using stochastic simulation.

The project combines a **discrete-event-inspired simulation engine, Monte Carlo experimentation, statistical analysis, FastAPI backend, and React dashboard** into a single research-oriented platform.

---

## 🚀 Overview

ResiliSim represents a system as interconnected components with different levels of **criticality, recovery time, and dependencies**.

When an initial component fails, the disruption can propagate through dependent components. Recovery is then influenced by:

* Failure propagation probability
* Recovery-time uncertainty
* Available intervention resources
* Resource regeneration
* Intervention delay
* Response-policy decisions

Two policies are evaluated under identical stochastic conditions:

**Baseline Policy** → prioritizes components mainly by criticality
**Adaptive Policy** → dynamically considers criticality, dependency pressure, and recovery urgency

This allows the project to study whether adaptive intervention strategies can improve resilience outcomes under increasingly difficult disruption scenarios.

---

## ✨ Key Features

* ⚙️ **30 scenario families** — 5 disruption types × 6 severity levels
* 🔗 **Dependency-driven cascading failures**
* 🎲 **Stochastic propagation and recovery uncertainty**
* 🧮 **Constrained intervention resources**
* ⏱️ **Delayed intervention modeling**
* 🔄 **Baseline vs. adaptive response policies**
* 📊 **Multiple resilience metrics**
* 🔬 **Paired Monte Carlo experimentation**
* 📈 **Wilcoxon signed-rank policy comparisons**
* 🧭 **Spearman sensitivity analysis**
* 🐍 **FastAPI backend**
* ⚛️ **React + Recharts interactive dashboard**
* 🧪 **Automated test suite**
* 📁 **CSV-based research outputs**
* 📝 **Research-design documentation**

---

## 🧩 Simulation Model

Each scenario contains a network of interdependent components such as:

```text
power
  │
  ├── network
  │     ├── compute
  │     │     └── database
  │     │           └── api
  │     │                 └── frontend
  │     │
  │     └── communications
  │
  └── ...
```

A failure in an upstream component can therefore create **dependency pressure** on downstream components.

The simulation models:

1. Initial component failures
2. Dependency-based failure propagation
3. Uncertain recovery durations
4. Resource regeneration
5. Policy-driven intervention allocation
6. Natural recovery
7. Service availability over time

The simulation runs in **0.5-hour time steps** with a maximum simulation horizon of **72 hours**.

---

## 🌪️ Scenario Design

ResiliSim defines exactly **30 scenarios**, generated from:

**5 disruption families × 6 severity levels = 30 scenarios**

### Disruption Families

| Family                    | Initial Disruption |
| ------------------------- | ------------------ |
| Infrastructure Outage     | Power              |
| Network Partition         | Network            |
| Compute Failure           | Compute            |
| Data-Service Failure      | Database           |
| Multi-Service Degradation | API + Dispatch     |

### Severity Levels

Severity levels **S1–S6** progressively modify:

* Propagation probability
* Recovery-time multiplier
* Resource budget
* Resource regeneration rate
* Intervention delay
* Uncertainty scale

This creates a controlled experimental space for studying resilience under progressively harder conditions.

---

## 🧠 Response Policies

### Baseline Policy

The baseline strategy uses a relatively static prioritization approach based primarily on **component criticality**.

It represents a simpler response strategy where the most critical components receive priority.

### Adaptive Policy

The adaptive strategy dynamically reprioritizes failed components using:

```text
Adaptive Priority =
Criticality
+ Dependency Pressure
+ Recovery Urgency
```

It also changes its resource allocation behavior based on the scenario's intervention delay.

This provides a controlled comparison between **static prioritization and dependency-aware adaptive decision-making**.

---

## 📊 Resilience Metrics

Each simulation records several outcomes:

| Metric                    | Description                                        |
| ------------------------- | -------------------------------------------------- |
| Recovery Time             | Time required for the system to recover            |
| Cumulative Disruption     | Total disruption accumulated during the simulation |
| Resource Utilization      | Fraction of available resources consumed           |
| Mean Service Availability | Criticality-weighted service availability          |
| Peak Failed Components    | Maximum number of simultaneously failed components |
| Interventions             | Number of intervention cycles                      |
| Event Count               | Number of failure/recovery events                  |

These metrics allow resilience to be evaluated from multiple perspectives rather than using recovery time alone.

---

## 🔬 Monte Carlo Experiment

The research runner is structured around a paired stochastic experiment:

```text
30 scenarios
     ×
50 independent repetitions
     =
1,500 paired Monte Carlo trials
```

Each paired trial evaluates **both policies using the same random seed**:

```text
                 Same Scenario + Same Seed
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       Baseline Policy         Adaptive Policy
              │                       │
              ▼                       ▼
        Simulation A            Simulation B
              │                       │
              └───────────┬───────────┘
                          ▼
                  Paired Comparison
```

Therefore:

* **1,500 paired experimental trials**
* **3,000 policy-specific simulation executions**

Using matched seeds reduces stochastic differences between the two policies and makes the comparison more controlled.

---

## 📈 Statistical Analysis

ResiliSim includes two analysis pipelines.

### Paired Wilcoxon Comparison

The `paired_summary` analysis performs **Wilcoxon signed-rank comparisons** between baseline and adaptive outcomes for each scenario.

This is applied to:

* Recovery time
* Cumulative disruption
* Resource utilization
* Mean service availability

### Sensitivity Analysis

The project also calculates **Spearman correlations** between scenario parameters and resilience outcomes.

Factors include:

* Propagation probability
* Resource budget
* Intervention delay
* Uncertainty scale

This helps investigate how scenario characteristics are associated with resilience outcomes under each policy.

---

## 🖥️ Interactive Dashboard

ResiliSim includes a React-based dashboard connected to the FastAPI backend.

The interface allows users to:

* Select a scenario
* Specify a random seed
* Run a baseline/adaptive comparison
* View recovery time
* View cumulative disruption
* View service availability
* View resource utilization
* Compare availability trajectories visually

The dashboard uses **Recharts** to visualize baseline and adaptive service availability over time.

```text
React Dashboard
       │
       ▼
   FastAPI API
       │
       ▼
 Scenario Selection
       │
       ▼
 Paired Simulation
   ┌───┴───┐
   ▼       ▼
Baseline Adaptive
   │       │
   └───┬───┘
       ▼
 Metrics + Timeline
```

---

## 🔌 API

The backend exposes a lightweight FastAPI service.

### Health Check

```http
GET /health
```

### Scenario Enumeration

```http
GET /scenarios
```

Returns the available scenario configurations and their parameters.

### Policy Comparison

```http
POST /compare
```

Example request:

```json
{
  "scenario_id": "compute_failure-S4",
  "seed": 42
}
```

The endpoint runs both policies under the requested scenario and returns their simulation results and timelines.

Interactive API documentation is available through FastAPI's generated Swagger interface at:

```text
http://localhost:8000/docs
```

---

## 🧪 Testing

The backend contains automated tests covering:

* Exact 30-scenario generation
* Unique scenario IDs
* Paired baseline/adaptive execution
* Metric validity ranges
* Reproducibility with identical seeds
* Sensitivity-analysis pipeline

Run the test suite with:

```bash
cd backend
pytest -q
```

---

## 📁 Research Outputs

Running the complete study generates:

```text
results/
├── simulation_results.csv
├── paired_policy_summary.csv
└── sensitivity_analysis.csv
```

### `simulation_results.csv`

Contains policy-specific simulation records including:

* Scenario
* Policy
* Seed
* Recovery time
* Cumulative disruption
* Resource utilization
* Service availability
* Interventions
* Peak failures
* Event count

### `paired_policy_summary.csv`

Contains baseline/adaptive metric summaries and Wilcoxon p-values for each scenario.

### `sensitivity_analysis.csv`

Contains Spearman correlation results between scenario factors and resilience outcomes.

---

## 🏗️ Project Structure

```text
ResiliSim/
│
├── backend/
│   ├── resilisim/
│   │   ├── api.py              # FastAPI endpoints
│   │   ├── analysis.py         # Statistical analysis
│   │   ├── models.py           # Simulation data models
│   │   ├── policies.py         # Baseline & adaptive policies
│   │   ├── scenarios.py        # Scenario catalog
│   │   └── simulation.py       # Simulation engine
│   │
│   ├── scripts/
│   │   ├── run_demo.py
│   │   └── run_full_study.py
│   │
│   ├── tests/
│   │   └── test_resilisim.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   └── package.json
│
├── docs/
│   └── research_design.md
│
├── results/
└── README.md
```

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* NumPy
* Pandas
* SciPy
* Pytest

### Frontend

* React
* Vite
* Recharts
* CSS

### Research & Simulation

* Stochastic simulation
* Monte Carlo experimentation
* Paired experimental design
* Wilcoxon signed-rank testing
* Spearman sensitivity analysis
* Dependency-based failure propagation

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ResiliSim
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn resilisim.api:app --reload
```

The API will run locally on:

```text
http://localhost:8000
```

### 4. Run a Simulation Demo

Open another terminal:

```bash
cd backend
python scripts/run_demo.py
```

### 5. Run the Full Research Experiment

```bash
cd backend
python scripts/run_full_study.py
```

This executes:

```text
30 scenarios × 50 repetitions × 2 policies
= 3,000 simulation executions
```

and generates the research CSV files in `results/`.

### 6. Start the React Dashboard

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the Vite development URL displayed in the terminal.

---

## 📚 Research Documentation

The `docs/research_design.md` file describes the experimental methodology, including:

* Research question
* Scenario construction
* Severity parameters
* Response-policy design
* Paired Monte Carlo methodology
* Outcome metrics
* Statistical analysis
* Interactive-system design

The documentation is intended to keep the experimental design separate from the implementation and make the study easier to reproduce and extend.

---

## 🔮 Future Directions

Potential extensions include:

* More realistic network topologies
* Additional adaptive decision policies
* Multi-objective policy optimization
* Reinforcement-learning-based response strategies
* More detailed resource constraints
* Dynamic dependency graphs
* Confidence intervals and effect-size analysis
* Scenario optimization and automated stress testing
* Larger-scale Monte Carlo experiments
* More advanced dashboard analytics

---

## 📌 Project Status

**Status: Functional research prototype**

ResiliSim currently provides an end-to-end workflow for:

**Scenario Generation → Stochastic Simulation → Policy Comparison → Statistical Analysis → Interactive Visualization**

The repository is designed to support reproducible experimentation rather than relying on predetermined performance improvements.

> **Important:** The code defines and supports the complete 30-scenario × 50-repetition experiment. Any claims about measured improvement between baseline and adaptive policies should be calculated from the generated experimental results rather than assumed beforehand.

---

## 👨‍💻 Author

**Krushna Tekane**

BTech Computer Science Engineering
Interested in Software Development, AI/ML, Simulation, and Research-Oriented Systems
