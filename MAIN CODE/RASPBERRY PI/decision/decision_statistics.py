"""
decision_statistics.py
Recon Rover V1 - Decision Interpretation & Action Planning

Tracks planning statistics.
"""

class DecisionStatistics:
    def __init__(self):
        self.plans_generated = 0
        
    def record_plan(self):
        self.plans_generated += 1
