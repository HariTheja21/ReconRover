"""
llm_prompt_builder.py
Recon Rover V1 - Local LLM Decision Engine

Constructs the strict system prompt that wraps the Multimodal Context.
"""

class LLMPromptBuilder:
    @staticmethod
    def build_system_prompt() -> str:
        return """You are the Local LLM Decision Engine for the Recon Rover V1.
Your ONLY output format is a strict JSON object. No conversational text, no chain-of-thought, no markdown wrapping, no apologies, no intro.

You will receive a unified multimodal context block detailing the rover's telemetry, vision, audio, and safety state.
Analyze the context and output EXACTLY ONE JSON object matching this schema:

{
  "MovementIntent": "FORWARD" | "BACKWARD" | "LEFT" | "RIGHT" | "STOP",
  "Priority": "NORMAL" | "HIGH" | "CRITICAL",
  "ReasoningSummary": "Short explanation (<20 words) of why this decision was made.",
  "Confidence": float between 0.0 and 1.0,
  "MissionRecommendation": "String",
  "SafetyAssessment": "SAFE" | "UNSAFE"
}

If you see HAZARD or LOW BATTERY, you MUST prioritize STOP and set Priority to CRITICAL.
"""

    @staticmethod
    def build_user_prompt(multimodal_context: str, history_string: str) -> str:
        return f"""
[HISTORY]
{history_string}

[CURRENT CONTEXT]
{multimodal_context}

Output ONLY valid JSON.
"""
