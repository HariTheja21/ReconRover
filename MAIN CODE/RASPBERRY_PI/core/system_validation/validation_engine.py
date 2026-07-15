import asyncio
import time
from typing import Callable

from .validation_events import (
    ValidationStartedEvent, TestStartedEvent, TestCompletedEvent,
    ValidationFailedEvent, ValidationCompletedEvent
)
from .validation_statistics import ValidationStatistics
from .validation_health import ValidationHealth
from .test_runner import TestRunner
from .loop_validator import LoopValidator
from .latency_analyzer import LatencyAnalyzer

class ValidationEngine:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.stats = ValidationStatistics()
        self.health = ValidationHealth()
        self.runner = TestRunner(publish_callback)
        self.validator = LoopValidator()
        self.latency = LatencyAnalyzer()

    async def execute_validation(self) -> bool:
        start_time = time.time()
        self.publish("ValidationStartedEvent", ValidationStartedEvent(timestamp=start_time))

        results = await self.runner.execute_all_tests()
        
        all_passed = True
        for name, res in results.items():
            passed = res.get("passed", False)
            latency = res.get("latency_ms", 0)
            
            self.latency.record_latency(latency)
            
            self.publish("TestCompletedEvent", TestCompletedEvent(name, passed, res))
            
            if passed:
                self.stats.tests_passed += 1
            else:
                self.stats.tests_failed += 1
                self.publish("ValidationFailedEvent", ValidationFailedEvent(name, str(res.get("error", "Failed"))))
                self.health.mark_failure(f"Test failed: {name}")
                all_passed = False

        if all_passed and self.latency.validate_latency(max_allowed_ms=100):
            self.health.mark_validated()
            
            total_time_ms = int((time.time() - start_time) * 1000)
            self.stats.total_latency_ms = sum(self.latency.latencies)
            self.stats.average_latency_ms = int(self.latency.get_average_latency())
            
            metrics = {
                "tests_passed": self.stats.tests_passed,
                "average_latency_ms": self.stats.average_latency_ms
            }
            self.publish("ValidationCompletedEvent", ValidationCompletedEvent(total_time_ms, metrics))
            return True
        else:
            if all_passed:
                self.health.mark_failure(f"Latency exceeded maximum threshold. Max: {self.latency.get_max_latency()}ms")
            return False
