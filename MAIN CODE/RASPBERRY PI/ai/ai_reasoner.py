"""
ai_reasoner.py
Recon Rover V1 - AI Decision Engine

Combines Context and Rules to produce Intents.
"""

import time
from .ai_context import AIContext
from .ai_memory import AIMemory
from .ai_state_machine import AIStateMachine, AIState
from .ai_rules import AIRuleEngine
from .ai_health import AIHealth
from .ai_statistics import AIStatistics

class AIReasoner:
    def __init__(self, context: AIContext, memory: AIMemory, state_machine: AIStateMachine, health: AIHealth, stats: AIStatistics):
        self.context = context
        self.memory = memory
        self.state_machine = state_machine
        self.rules = AIRuleEngine()
        self.health = health
        self.stats = stats

    def evaluate(self) -> AIState:
        """
        Runs the rule engine against the current context and attempts a state transition.
        Returns the new state (or current state if no change).
        """
        start_time = time.perf_counter()
        
        target_state = self.rules.evaluate(self.context)
        
        if target_state != self.state_machine.current_state:
            # Attempt transition
            success = self.state_machine.transition(target_state)
            self.health.record_transition(success)
            
            if success:
                # Log transition stats
                if target_state == AIState.EMERGENCY:
                    self.stats.record_emergency()
                elif target_state == AIState.RETURNING:
                    self.stats.record_return_home()
                elif target_state == AIState.AVOIDING:
                    self.stats.record_hazard_response()
                    
                self.stats.track_state_duration(target_state.name)
        
        duration_ms = (time.perf_counter() - start_time) * 1000
        self.health.record_decision(duration_ms)
        self.stats.record_decision()
        
        # Update Health Tracker
        self.health.update_state(self.state_machine.current_state.name, self.context.current_objective, self.context.confidence)
        
        return self.state_machine.current_state
