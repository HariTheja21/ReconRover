# Phase 5.0: Hardware Bring-up & System Boot Framework - Implementation Plan

## Executive Summary
Phase 5.0 orchestrates the complete initialization of the Recon Rover V2 software stack. By leveraging the modular architecture built across Phases 1-4, this framework implements a deterministic, dependency-aware boot sequence. It ensures that the Raspberry Pi safely validates internal subsystems (EventBus, Runtime, Safety) before verifying external physical hardware (ESP32 UART, Camera). It prevents the rover from entering an operational state if critical physical or software components are missing.

## Objectives
- Implement `BootManager` and `BootEngine` to provide a unified AsyncIO entry point for the entire stack.
- Define the exact `BootSequence` topologically ordering the 16 primary subsystems (Config $\to$ EventBus $\to$ ESP32 $\dots \to$ Mission).
- Implement `DependencyChecker` to ensure no module boots unless its prerequisites have successfully started.
- Implement `HardwareDiscovery` to dynamically probe Linux device files (e.g., `/dev/ttyUSB0`, `/dev/video0`) to confirm physical connections.
- Implement `StartupValidator` to provide a strict `PASS/FAIL` verdict before releasing the system to Mission Mode.

## Architecture
- `MAIN CODE/RASPBERRY_PI/core/system_boot/boot_manager.py`: High-level AsyncIO API.
- `MAIN CODE/RASPBERRY_PI/core/system_boot/boot_engine.py`: The core sequence executor.
- `MAIN CODE/RASPBERRY_PI/core/system_boot/boot_sequence.py`: The static topological map of the system.
- `MAIN CODE/RASPBERRY_PI/core/system_boot/dependency_checker.py`: State tracker for booted modules.
- `MAIN CODE/RASPBERRY_PI/core/system_boot/hardware_discovery.py`: OS-level physical peripheral checks.
- `MAIN CODE/RASPBERRY_PI/core/system_boot/startup_validator.py`: Final safety check gate.

## Boot Flow
1. The `BootManager` is invoked by the main Python script.
2. The `BootEngine` begins iterating through the `BootSequence`.
3. For each module, the `DependencyChecker` asserts all required previous modules are online.
4. If the module represents external hardware (e.g., `ESP32`, `Camera`), `HardwareDiscovery` polls the OS.
5. If any check fails, the engine instantly halts, emitting a `BootFailedEvent`.
6. If all 16 steps succeed, the `StartupValidator` confirms the matrix and emits `BootCompletedEvent`.

## Failure Handling
The system employs a strict fail-safe boot. If the ESP32 is unplugged or fails to enumerate on the UART bus, the Boot Framework refuses to launch the Navigation or Mission layers, preventing the software from issuing commands into the void.

## Telemetry & Events
The boot process is highly observable. The `publish_callback` allows the engine to broadcast `SubsystemStartedEvent` and `SubsystemFailedEvent` directly to the `EventBus` (once it is initialized), allowing remote operator UIs to track the boot progress bar in real time.
