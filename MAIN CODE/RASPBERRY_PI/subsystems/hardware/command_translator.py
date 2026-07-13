"""
command_translator.py
Recon Rover V1 - Hardware Interface

Translates Action plans into byte strings.
"""

import json

class CommandTranslator:
    def translate_execution_request(self, action: str) -> bytes:
        """
        Maps the abstract semantic action (e.g., 'FORWARD') to a physical protocol payload.
        """
        # Create the standard JSON packet
        packet = {
            "type": "command",
            "command": "MOVE",
            "args": {"direction": action}
        }
        
        # Serialize to bytes with a newline for framing
        return json.dumps(packet).encode('utf-8') + b'\n'
        
    def translate_emergency_stop(self) -> bytes:
        """
        Hardcoded absolute safety packet.
        """
        packet = {
            "type": "command",
            "command": "STOP",
            "args": {"reason": "EMERGENCY"}
        }
        return json.dumps(packet).encode('utf-8') + b'\n'
