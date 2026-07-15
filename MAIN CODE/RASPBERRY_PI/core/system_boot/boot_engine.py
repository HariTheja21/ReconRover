import asyncio
import time
from typing import Dict, Any, Callable
from .boot_events import (
    BootStartedEvent, SubsystemStartedEvent, SubsystemFailedEvent,
    BootCompletedEvent, BootFailedEvent
)
from .boot_statistics import BootStatistics
from .boot_health import BootHealth
from .boot_sequence import BootSequence
from .dependency_checker import DependencyChecker
from .hardware_discovery import HardwareDiscovery
from .startup_validator import StartupValidator

class BootEngine:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.stats = BootStatistics()
        self.health = BootHealth()
        self.sequence = BootSequence().get_sequence()
        self.dependency_checker = DependencyChecker()
        self.hardware = HardwareDiscovery()
        self.validator = StartupValidator()

    async def execute_boot(self):
        start_time = time.time()
        self.publish("BootStartedEvent", BootStartedEvent(timestamp=start_time))

        for step in self.sequence:
            name = step["name"]
            deps = step["deps"]

            # Validate dependencies first
            if not self.dependency_checker.check_dependencies(name, deps):
                reason = f"Dependencies not met for {name}"
                self.stats.subsystems_failed += 1
                self.publish("SubsystemFailedEvent", SubsystemFailedEvent(name, reason))
                self.health.mark_failure(reason)
                self.publish("BootFailedEvent", BootFailedEvent(reason, name))
                return False

            # Simulate subsystem startup logic
            # In the real code, this would dynamically instantiate/start the module
            subsystem_start = time.time()
            
            # Special hardware checks mapped to sequence names
            if name == "ESP32":
                esp_ok = await self.hardware.verify_esp32()
                if not esp_ok:
                    self.stats.hardware_missing += 1
                    self.stats.subsystems_failed += 1
                    self.health.mark_failure("ESP32 hardware not found.")
                    self.publish("BootFailedEvent", BootFailedEvent("ESP32 hardware not found.", name))
                    return False
                self.stats.hardware_found += 1
            
            if name == "Camera":
                cam_ok = await self.hardware.check_camera()
                if not cam_ok:
                    # Depending on strictness, camera might be optional, but for this sequence we assume strict
                    self.stats.hardware_missing += 1
                    self.stats.subsystems_failed += 1
                    self.health.mark_failure("Camera hardware not found.")
                    self.publish("BootFailedEvent", BootFailedEvent("Camera hardware not found.", name))
                    return False
                self.stats.hardware_found += 1

            # Mark success
            self.dependency_checker.mark_started(name)
            self.stats.subsystems_started += 1
            startup_time_ms = int((time.time() - subsystem_start) * 1000)
            self.publish("SubsystemStartedEvent", SubsystemStartedEvent(name, startup_time_ms))
            
            # Slight delay to simulate async startup decoupling
            await asyncio.sleep(0.01)

        total_time_ms = int((time.time() - start_time) * 1000)
        self.stats.boot_time_ms = total_time_ms

        if self.validator.validate_boot(self.sequence, self.stats, self.health):
            diagnostics = {
                "subsystems": self.stats.subsystems_started,
                "hardware": self.stats.hardware_found
            }
            self.publish("BootCompletedEvent", BootCompletedEvent(total_time_ms, diagnostics))
            return True
        else:
            self.publish("BootFailedEvent", BootFailedEvent(self.health.failure_reason, "Validator"))
            return False
