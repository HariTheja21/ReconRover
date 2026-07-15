class DemoManager:
    def __init__(self, bridge, startup, shutdown, readiness, recovery, validator, scenario_mgr, mission, report):
        self.bridge = bridge
        self.startup = startup
        self.shutdown = shutdown
        self.readiness = readiness
        self.recovery = recovery
        self.validator = validator
        self.scenario_mgr = scenario_mgr
        self.mission = mission
        self.report = report
        
    async def run_full_demo(self) -> bool:
        start_ok = self.startup.execute()
        if not start_ok:
            return False
            
        ready_count = self.readiness.check_readiness()
        self.bridge.publish_event("SystemReady", {"subsystems_verified": ready_count, "timestamp": 0.0})
        
        scenario = self.scenario_mgr.load_scenario()
        if not self.validator.validate_scenario(scenario):
            return False
            
        self.bridge.publish_event("MissionDemoStarted", {"scenario_id": scenario["id"], "timestamp": 0.0})
        
        success = await self.mission.execute_scenario(scenario)
        
        if success:
            self.bridge.publish_event("MissionDemoCompleted", {"scenario_id": scenario["id"], "success": True, "timestamp": 0.0})
        else:
            recovered = self.recovery.attempt_recovery()
            if not recovered:
                self.bridge.publish_event("MissionDemoFailed", {"scenario_id": scenario["id"], "reason": "Simulation Failure", "timestamp": 0.0})
                
        final_report = self.report.generate(success)
        self.bridge.publish_event("FinalPerformanceReport", {"report": final_report, "timestamp": 0.0})
        
        shut_ok = self.shutdown.execute()
        self.bridge.publish_event("SystemShutdown", {"safe": shut_ok, "timestamp": 0.0})
        
        return success
