"""
main.py
Recon Rover V1 - Entry Point

Delegates to the new System Orchestrator (Phase 4.1).
"""

import asyncio
from system.app import App

if __name__ == "__main__":
    app = App()
    
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        pass
