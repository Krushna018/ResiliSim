
from __future__ import annotations
from abc import ABC, abstractmethod

class ResponsePolicy(ABC):
    name = "abstract"

    @abstractmethod
    def priority(self, component, state, dependents_down: int) -> float:
        raise NotImplementedError

    def allocation_fraction(self, hour: float, scenario) -> float:
        return 0.75

class BaselinePolicy(ResponsePolicy):
    """Simple first-order response: prioritize criticality only."""
    name = "baseline"

    def priority(self, component, state, dependents_down: int) -> float:
        return component.criticality

    def allocation_fraction(self, hour: float, scenario) -> float:
        # Deliberately conservative static plan.
        return 0.65 if hour < 8 else 0.75

class AdaptivePolicy(ResponsePolicy):
    """Adaptive response reprioritizes components as dependency pressure changes."""
    name = "adaptive"

    def priority(self, component, state, dependents_down: int) -> float:
        dependency_pressure = 0.18 * dependents_down
        recovery_urgency = 0.10 / max(state.recovery_remaining, 0.5)
        return component.criticality + dependency_pressure + recovery_urgency

    def allocation_fraction(self, hour: float, scenario) -> float:
        # React more aggressively after the scenario-specific intervention delay.
        return 0.55 if hour < scenario.intervention_delay_hours else 0.90
