"""
decision_health.py
Recon Rover V1 - Decision Interpretation & Action Planning

Tracks the health of the interpretation layer.
"""

class DecisionHealth:
    def __init__(self):
        self.status = "OK"
        self.rejected_decisions = 0
        self.safety_vetoes = 0
        
    def record_rejection(self):
        self.rejected_decisions += 1
        self._evaluate()
        
    def record_safety_veto(self):
        self.safety_vetoes += 1
        self._evaluate()
        
    def _evaluate(self):
        if self.safety_vetoes > 5:
            self.status = "DEGRADED (AI Hallucinating Unsafe Actions)"
        else:
            self.status = "OK"
