"""
vl_prompt_builder.py
Recon Rover V1 - Vision-Language Cognitive Integration

Optional utility if the VL engine needs to build its own intermediate prompts.
"""

class VLPromptBuilder:
    def __init__(self):
        pass
        
    def build_summary_prompt(self, raw_detections: str) -> str:
        """
        Used if we ever deploy a small dedicated local NLP model just to
        summarize vision. For now, handled deterministically by CaptionGenerator.
        """
        return f"Summarize these objects into a single sentence: {raw_detections}"
