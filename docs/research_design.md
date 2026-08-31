
# ResiliSim Research Design

## Research question
How do adaptive response policies alter resilience outcomes under cascading failures,
resource constraints, uncertain propagation, and delayed intervention?

## Scenario design
The project defines exactly **30 scenario families**:
- 5 disruption families
- 6 severity levels per family

The families include infrastructure outage, network partition, compute failure,
data-service failure, and multi-service degradation.

Severity controls:
- failure propagation probability
- recovery-time multiplier
- available resource budget
- resource regeneration
- intervention delay
- uncertainty scale

## Decision policies
Two response policies are evaluated within each Monte Carlo trial:
- baseline: mostly static criticality-based prioritization
- adaptive: dependency-aware dynamic reprioritization

A **paired trial** runs both policies using the same random seed, improving comparability.

## Full experiment
30 scenarios × 50 independent seeds = **1,500 paired Monte Carlo trials**.

Each paired trial evaluates both policies, so the resulting dataset contains
**3,000 policy-specific simulation executions**. This distinction is intentional:
the resume phrase "1,500 Monte Carlo simulation runs across baseline and adaptive
response strategies" refers to 1,500 paired experimental trials, each containing
the baseline/adaptive comparison under matched stochastic conditions.

## Outcomes
- recovery time
- cumulative disruption
- resource utilization
- mean service availability
- peak failed components
- intervention count

## Statistical analysis
- paired Wilcoxon signed-rank comparisons by scenario
- Spearman sensitivity analysis for propagation probability, intervention delay,
  uncertainty, and resource budget

## Interactive system
The FastAPI service exposes scenario enumeration and paired-policy comparison.
The React interface lets users choose a scenario/seed, run both policies, inspect
metrics, and visualize availability over time.
