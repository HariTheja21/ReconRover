"""
reasoning_engine.py
Recon Rover V1 - AI Decision Engine

Evaluates the AIContext and AIMemory to produce candidate actions.
"""

from .ai_context import AIContext
from .ai_memory import AIMemory
from .ai_blackboard import AIBlackboard, CandidateAction

class ReasoningEngine:
    def evaluate(self, context: AIContext, memory: AIMemory, blackboard: AIBlackboard):
        """Generates candidate actions based on current context and short-term memory."""
        
        # 1. Evaluate Vision
        vision = context.vision_semantics
        if vision.get("objects"):
            for obj in vision["objects"]:
                if obj.get("label") == "human":
                    memory.remember("human_seen")
                    blackboard.candidate_actions.append(
                        CandidateAction(intent="GreetHuman", target="human", priority_score=10)
                    )
        
        # 2. Evaluate Audio
        audio = context.audio_semantics
        if audio.get("speech"):
            memory.remember("speech_heard")
            blackboard.candidate_actions.append(
                CandidateAction(intent="ProcessSpeech", parameters={"text": audio["speech"]}, priority_score=15)
            )
            
        # 3. Evaluate Mission / Idle
        if context.mission_state == "IDLE":
            blackboard.candidate_actions.append(
                CandidateAction(intent="Patrol", priority_score=5)
            )
