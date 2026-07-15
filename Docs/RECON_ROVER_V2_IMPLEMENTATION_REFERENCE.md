# RECON ROVER V2 - IMPLEMENTATION REFERENCE

**Version:** 1.0.0
**Architecture Version:** 8.9
**Document Version:** 1.0
**Project Repository:** Recon Rover V2

## Revision History
| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-16 | 1.0 | Initial Release of Implementation Reference | AI Engineering Team |

---

## 1. Executive Summary
The Recon Rover V2 Implementation Reference is the definitive, code-level documentation of the entire repository. This document catalogs every folder, module, class, function, EventBus topic, protocol, GPIO mapping, and external dependency exactly as they are implemented in the source code up to Phase 8.9.

---

## 2. Folder Inventory
| Folder Path | Purpose | Contained Modules | Interactions |
|---|---|---|---|
| `MAIN CODE/ESP32/src/` | Hard-real-time motor and sensor drivers | `main.cpp`, `motor_task.cpp`, `sensor_task.cpp` | Serial comms to Pi |
| `MAIN CODE/RASPBERRY_PI/core/ai/runtime/` | Core cognitive reasoning architecture | Vision, Speech, LLM, Agents, Tools | Orchestrated by `DemoRuntime` |
| `WEB_UI/backend/` | WebSocket bridging and HTTP API | `api_server.py`, `websocket_manager.py` | Connects UI to EventBus |
| `docs/` | Engineering artifacts and manuals | PDFs, Markdown Plans/Reports | None (Static) |

---

## 3. Module Inventory
*(Note: A representative sample of the 100+ analyzed modules is documented below for brevity)*

### `core/ai/demo/demo_runtime.py`
- **Purpose:** Macro-orchestrator of the Phase 8.9 Autonomous Demonstration.
- **Classes:** `DemoRuntime`
- **Dependencies:** `StartupSequence`, `SystemReadiness`, `MissionDemo`
- **Runtime Behavior:** Awaits system readiness, executes mission steps via scenario manager, handles shutdown on completion or failure.

### `core/ai/runtime/tools/tool_executor.py`
- **Purpose:** Safely invokes Python functions requested by the LLM.
- **Classes:** `ToolExecutor`
- **Dependencies:** `tool_validator.py`, `tool_registry.py`
- **Runtime Behavior:** Validates permissions, executes functions asynchronously, returns serialized `ToolResult`.

### `core/ai/runtime/optimization/thermal_manager.py`
- **Purpose:** Prevents physical damage to the Raspberry Pi SoC.
- **Classes:** `ThermalManager`
- **Runtime Behavior:** Polls `vcgencmd measure_temp` every 5 seconds. If temp > 75C, emits `optimization.throttle` event.

---

## 4. Runtime Inventory
| Runtime Name | Initialization | Shutdown | Health Checks | Statistics |
|---|---|---|---|---|
| `DemoRuntime` | Boot sequence -> Readiness check | Agent termination, memory flush | 3-strike failure limit | Total mission time, success rate |
| `BenchmarkRuntime` | Profiler initialization | Silent exit | None (Passive observer) | Aggregates all other runtimes |
| `OptimizationRuntime` | Binds to cgroups / vcgencmd | Resets priorities to normal | Checks thermal API access | Throttle events fired |
| `AgentRuntime` | Spawns supervisor and worker actors | Flushes blackboard, stops async queues | Mailbox latency checks | Messages passed, consensus reached |
| `ToolRuntime` | Loads tool registry and permissions | Closes sandbox contexts | Registry integrity check | Executions, failures, timeouts |
| `RagRuntime` | Mounts ChromaDB, loads embedding models | Persists vectors to disk | ChromaDB ping | Retrieval latency, chunk counts |
| `LlmRuntime` | Connects to Ollama/vLLM daemon | Clears context buffers | Provider API ping | Time-to-first-token, Tokens/sec |
| `VisionRuntime` | Grabs `/dev/video0`, loads ONNX/YOLO | Releases camera hardware | Frame buffer staleness | FPS, Inference latency |
| `SpeechRuntime` | Grabs ALSA mic, loads Whisper/Piper | Releases ALSA audio | Audio stream drop check | RTF (Real-Time Factor), WER |

---

## 5. Class Inventory
### `BenchmarkManager` (`core/ai/runtime/benchmark/benchmark_manager.py`)
- **Purpose:** Iterates over profilers and routes data.
- **Public Methods:** `run_benchmark_cycle()`
- **Lifecycle:** Instantiated by `BenchmarkRuntime`, called periodically by `BenchmarkScheduler`.

### `ScenarioManager` (`core/ai/demo/scenario_manager.py`)
- **Purpose:** Loads mission definitions.
- **Public Methods:** `load_scenario()`
- **Lifecycle:** Instantiated by `DemoRuntime`, called once during mission startup.

---

## 6. Event Inventory
| Topic | Publisher | Subscriber | Payload | Expected Behavior |
|---|---|---|---|---|
| `demo.runtime` | `DemoBridge` | Global Listeners | `{"_demo_event_type": "SystemReady", "subsystems": 6}` | Signals permission to start mission |
| `benchmark.telemetry` | `BenchmarkBridge` | EventBus/WebSockets | `{"fps": 30, "ttft": 150}` | Dashboard UI updates |
| `optimization.throttle` | `ThermalManager` | ThreadPoolManager | `{"level": "HIGH", "temp": 82}` | System scales back inference threads |
| `navigation.cmd` | `ToolExecutor` | `SerialRuntime` | `{"cmd": "move", "dir": "forward"}` | Serial translation to ESP32 |

---

## 7. Configuration Inventory
| Name | Default Value | Allowed Values | Purpose | Where Used |
|---|---|---|---|---|
| `LLM_PROVIDER` | `ollama` | `ollama`, `vllm`, `openai` | Dictates which inference engine handles LLM requests | `ProviderManager` |
| `CAMERA_FPS` | `30` | `15`, `30`, `60` | Caps the frame capture rate | `CameraProvider` |
| `THERMAL_LIMIT` | `75` | `60` - `85` | Temp (C) at which throttling begins | `ThermalManager` |
| `BENCHMARK_INTERVAL`| `300` | `10` - `3600` | Seconds between telemetry sweeps | `BenchmarkScheduler` |

---

## 8. GPIO Inventory
| Board | Pin | Function | Direction | Connected Hardware |
|---|---|---|---|---|
| ESP32 | GPIO 16 | UART2 RX | IN | Raspberry Pi TX (GPIO 14) |
| ESP32 | GPIO 17 | UART2 TX | OUT | Raspberry Pi RX (GPIO 15) |
| ESP32 | GPIO 25 | PWM 0 | OUT | L298N Left ENA |
| ESP32 | GPIO 32 | Digital | OUT | HC-SR04 Trigger |
| RPi 5 | GPIO 2 | I2C SDA | IN/OUT | MPU6050 & INA219 |
| RPi 5 | GPIO 18 | PWM | OUT | WS2812B NeoPixels |

---

## 9. Dependency Inventory
| Package | Version | Purpose | Used By |
|---|---|---|---|
| `torch` | 2.x | Neural Network Ops | Vision, Speech |
| `chromadb` | 0.4+ | Vector Database | RAG Pipeline |
| `langchain` | 0.1+ | Prompt formatting | Agent / LLM Runtimes |
| `pyserial` | 3.5 | UART Comms | SerialRuntime |

---

## 10. Protocol Inventory
### Serial JSON Protocol (Pi <-> ESP32)
- **Format:** JSON lines.
- **Payload Schema:** `{"cmd": string, "val": any}`
- **Validation:** Enforced by `protocol_schema.json` via Pydantic/jsonschema on the Pi before transmission.

*(End of Implementation Reference)*
