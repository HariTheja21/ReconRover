# AUTO-GENERATED FILE. DO NOT MODIFY.
from dataclasses import dataclass
from typing import Any

@dataclass
class Event:
    pass

@dataclass
class TelemetryReceived(Event):
    raw_data: str

@dataclass
class CommandIssued(Event):
    command_type: str
    payload: dict

@dataclass
class FaultReceived(Event):
    subsystem: int
    code: int

@dataclass
class HealthUpdate(Event):
    module_name: str
    status: str
    details: str

@dataclass
class ModuleReady(Event):
    module_name: str

@dataclass
class ModuleFailed(Event):
    module_name: str
    reason: str

@dataclass
class DiagnosticsUpdate(Event):
    cpu_percent: float
    ram_percent: float
    serial_latency_ms: float

@dataclass
class ShutdownRequested(Event):
    reason: str

@dataclass
class SensorStateUpdated(Event):
    sensor_id: str
    state: float

@dataclass
class ObstacleDetected(Event):
    location: str
    distance_cm: float

@dataclass
class BatteryLow(Event):
    voltage: float
    percentage: float

@dataclass
class GasDetected(Event):
    gas_level: float
    confidence: float

@dataclass
class WorldStateUpdated(Event):
    state: Any

@dataclass
class ObstacleAppeared(Event):
    distance: float
    angle: float

@dataclass
class ObstacleCleared(Event):
    direction: str

@dataclass
class HazardDetected(Event):
    hazard_type: str
    location: str

@dataclass
class HazardCleared(Event):
    hazard_type: str

@dataclass
class BatteryCritical(Event):
    level: float

@dataclass
class NavigationStateChanged(Event):
    old_state: str
    new_state: str

@dataclass
class NavigationDecision(Event):
    state: str

@dataclass
class RecoveryStarted(Event):
    reason: str

@dataclass
class RecoveryCompleted(Event):
    pass

@dataclass
class EmergencyStopRequested(Event):
    reason: str

@dataclass
class PathSelected(Event):
    direction: str

@dataclass
class MovementRequestEvent(Event):
    direction: str
    speed: float

@dataclass
class CommandPacketReady(Event):
    packet: Any

@dataclass
class SerialConnected(Event):
    port: str

@dataclass
class SerialDisconnected(Event):
    pass

@dataclass
class SerialError(Event):
    reason: str

@dataclass
class PacketDropped(Event):
    reason: str

@dataclass
class HealthReceived(Event):
    timestamp_ms: int
    data: dict

@dataclass
class ExplorationRequested(Event):
    pass

@dataclass
class AvoidObstacleRequested(Event):
    pass

@dataclass
class ReturnHomeRequested(Event):
    pass

@dataclass
class ScanEnvironmentRequested(Event):
    pass

@dataclass
class PauseRequested(Event):
    pass

@dataclass
class ResumeRequested(Event):
    pass

@dataclass
class GoalSelected(Event):
    goal_name: str

@dataclass
class NavigationBlocked(Event):
    pass

@dataclass
class GoalReached(Event):
    pass

@dataclass
class FrameCaptured(Event):
    timestamp: float

@dataclass
class FrameProcessed(Event):
    timestamp: float

@dataclass
class ObjectDetected(Event):
    timestamp_ms: int
    object_class: str
    confidence: float
    bbox: list

@dataclass
class SceneUpdated(Event):
    semantics: dict

@dataclass
class VisionHealthUpdated(Event):
    status: str

@dataclass
class CameraDisconnected(Event):
    pass

@dataclass
class CameraReconnected(Event):
    pass

@dataclass
class PersonDetected(Event):
    pass

@dataclass
class AnimalDetected(Event):
    pass

@dataclass
class MarkerDetected(Event):
    pass

@dataclass
class PathVisible(Event):
    pass

@dataclass
class UnknownObjectDetected(Event):
    pass

@dataclass
class AudioCaptured(Event):
    timestamp: float

@dataclass
class AudioProcessed(Event):
    timestamp: float

@dataclass
class SoundDetected(Event):
    semantics: dict

@dataclass
class AudioSceneUpdated(Event):
    semantics: dict

@dataclass
class AudioHealthUpdated(Event):
    status: str

@dataclass
class MicrophoneDisconnected(Event):
    pass

@dataclass
class MicrophoneReconnected(Event):
    pass

@dataclass
class HumanSpeechDetected(Event):
    pass

@dataclass
class ClapDetected(Event):
    pass

@dataclass
class KnockDetected(Event):
    pass

@dataclass
class VehicleDetected(Event):
    pass

@dataclass
class AlarmDetected(Event):
    pass

@dataclass
class SilenceDetected(Event):
    pass

@dataclass
class UnknownSoundDetected(Event):
    pass

@dataclass
class MissionRequested(Event):
    mission_type: str
    requested_by: str

@dataclass
class MissionCancelled(Event):
    mission_id: str
    reason: str

@dataclass
class MissionPaused(Event):
    mission_id: str

@dataclass
class MissionResumed(Event):
    mission_id: str

@dataclass
class ManualOverrideEnabled(Event):
    pass

@dataclass
class ManualOverrideDisabled(Event):
    pass

@dataclass
class MissionStarted(Event):
    mission_id: str
    mission_type: str
    owner: str

@dataclass
class MissionCompleted(Event):
    mission_id: str
    status: str

@dataclass
class MissionFailed(Event):
    mission_id: str
    reason: str

@dataclass
class MissionTimedOut(Event):
    mission_id: str

@dataclass
class MissionChanged(Event):
    old_mission_id: str
    new_mission_id: str

@dataclass
class MissionStatusUpdated(Event):
    mission_id: str
    status: str

@dataclass
class MissionOwnershipChanged(Event):
    mission_id: str
    new_owner: str

@dataclass
class MissionProgressUpdated(Event):
    mission_id: str
    progress_percentage: float

@dataclass
class EmergencyMissionStarted(Event):
    mission_id: str

@dataclass
class ApplicationStarting(Event):
    pass

@dataclass
class ApplicationReady(Event):
    pass

@dataclass
class ApplicationRunning(Event):
    pass

@dataclass
class ApplicationStopping(Event):
    pass

@dataclass
class ApplicationStopped(Event):
    pass

@dataclass
class ModuleRegistered(Event):
    module_name: str

@dataclass
class ModuleStarted(Event):
    module_name: str

@dataclass
class ModuleStopped(Event):
    module_name: str

@dataclass
class ModuleRecovered(Event):
    module_name: str

@dataclass
class SystemHealthy(Event):
    pass

@dataclass
class SystemDegraded(Event):
    pass

@dataclass
class SystemCritical(Event):
    pass

@dataclass
class StartupValidationPassed(Event):
    pass

@dataclass
class StartupValidationFailed(Event):
    reason: str

@dataclass
class CameraRequestEvent(Event):
    action: str

@dataclass
class ExpressionRequestEvent(Event):
    expression: str

@dataclass
class BehaviorStateChanged(Event):
    state: str

@dataclass
class ObjectsDetected(Event):
    objects: list

@dataclass
class CameraFailure(Event):
    reason: str

@dataclass
class SpeechDetected(Event):
    text: str

@dataclass
class DirectionEstimated(Event):
    azimuth: float
    elevation: float

@dataclass
class MicrophoneFailure(Event):
    reason: str

@dataclass
class DecisionUpdated(Event):
    intent: str
    parameters: dict

@dataclass
class DecisionConfidenceUpdated(Event):
    confidence: float

@dataclass
class ObjectiveChanged(Event):
    objective: str

@dataclass
class EmergencyDecision(Event):
    reason: str

@dataclass
class DecisionRequested(Event):
    pass

@dataclass
class LLMDecisionReady(Event):
    movement_intent: str
    priority: str
    reasoning_summary: str
    confidence: float
    mission_recommendation: str
    safety_assessment: str

@dataclass
class LLMDecisionFailed(Event):
    reason: str

@dataclass
class LLMHealthUpdated(Event):
    diagnostics: dict

@dataclass
class LLMInferenceStarted(Event):
    pass

@dataclass
class LLMInferenceFinished(Event):
    pass

@dataclass
class BatteryUpdated(Event):
    level: float

@dataclass
class DecisionSelected(Event):
    decision: str

@dataclass
class ObjectiveSelected(Event):
    objective: str
    constraints: list

@dataclass
class ObjectiveCompleted(Event):
    objective: str

@dataclass
class ObjectiveFailed(Event):
    objective: str
    reason: str

@dataclass
class AutonomyUpdated(Event):
    state: str

@dataclass
class AutonomyHealthUpdated(Event):
    status: str

@dataclass
class PlanningStarted(Event):
    pass

@dataclass
class PlanningFinished(Event):
    pass

@dataclass
class MemoryCreated(Event):
    memory_id: str

@dataclass
class MemoryUpdated(Event):
    memory_id: str

@dataclass
class MemoryRetrieved(Event):
    query_tags: list

@dataclass
class MemorySummarized(Event):
    pass

@dataclass
class MemoryHealthUpdated(Event):
    status: str

@dataclass
class VisionLanguageContextUpdated(Event):
    semantics: str

@dataclass
class ObservationGenerated(Event):
    observation: str

@dataclass
class SceneSummaryUpdated(Event):
    summary: str

@dataclass
class SpeechRecognized(Event):
    semantics: dict

@dataclass
class AudioLanguageContextUpdated(Event):
    semantics: str

@dataclass
class AudioObservationGenerated(Event):
    observation: str

@dataclass
class AudioSummaryUpdated(Event):
    summary: str

@dataclass
class NavigationStateUpdated(Event):
    state: str

@dataclass
class HealthUpdated(Event):
    status: str

@dataclass
class MissionUpdated(Event):
    status: str

@dataclass
class MultimodalContextUpdated(Event):
    pass

@dataclass
class ContextReadyForLLM(Event):
    prompt_block: str

@dataclass
class LLMInferenceCompleted(Event):
    pass

@dataclass
class SystemHealthUpdated(Event):
    status: str

@dataclass
class DecisionPlanReady(Event):
    plan_id: str
    priority: int
    immediate_action: str
    short_term_actions: list
    long_term_goals: list

@dataclass
class DecisionRejected(Event):
    reason: str

@dataclass
class DecisionHealthUpdated(Event):
    status: str

@dataclass
class EmergencyStop(Event):
    reason: str

@dataclass
class ExecutionRequest(Event):
    plan_id: str
    priority: int
    action: str

@dataclass
class ExecutionStarted(Event):
    plan_id: str

@dataclass
class ExecutionCompleted(Event):
    plan_id: str

@dataclass
class ExecutionCancelled(Event):
    plan_id: str
    reason: str

@dataclass
class ExecutionFailed(Event):
    plan_id: str
    reason: str

@dataclass
class ExecutionHealthUpdated(Event):
    status: str

@dataclass
class ESP32Connected(Event):
    port: str

@dataclass
class ESP32Disconnected(Event):
    reason: str

@dataclass
class HeartbeatTimeout(Event):
    last_seen: float
    time_since: float

@dataclass
class HardwareHealthUpdated(Event):
    status: str

@dataclass
class RuntimeStatisticsUpdated(Event):
    uptime: float
    cpu_usage: float
    ram_usage: float
    total_events: int

@dataclass
class SystemShutdownRequested(Event):
    reason: str
    class EventBus: 
    def __init__(self): 
    self._subscribers: Dict[Type[Event], List[Callable[[Event], Awaitable[None]]]] = {}
    self._queue: asyncio.Queue = asyncio.Queue()
    def subscribe(self, event_type: Type[Event], callback
    if event_type not in self._subscribers: 
    def publish(self, event: Event)
    try: 
    except asyncio.QueueFull: 
    self.log.error(f"Event bus queue full! Dropped event: {event}")
    async def _process_events(self): 
    while self._running: 
    if event_type in self._subscribers: 
    for callback in self._subscribers[event_type]: 
    except Exception as e: 
    self.log.error(f"Error in subscriber {callback.__name__} for {event_type.__name__}: {e}")
    except asyncio.CancelledError: 
    self.log.error(f"Event bus loop error: {e}")
    async def start(self): 
    async def stop(self): 
    if self._task: 

