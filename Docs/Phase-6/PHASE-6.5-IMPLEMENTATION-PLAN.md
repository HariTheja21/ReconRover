# Phase 6.5: Configuration & OTA Management - Implementation Plan

## Executive Summary
Phase 6.5 delivers the Configuration & OTA (Over-The-Air) Management Framework. This phase empowers operators to centrally manage rover parameters (motion limits, safety thresholds, camera resolutions) and deploy firmware updates directly from the Ground Station browser. 

## Objectives
- Implement `ConfigurationManager` to orchestrate backend profile storage, validation, and system-wide EventBus updates.
- Implement `OTAManager` to securely handle binary firmware uploads, validate SHA256 checksums, and orchestrate the simulated deployment pipeline.
- Implement `configuration.html` encompassing two distinct UI panels: one for Robot Configuration and one for OTA Firmware Updates.
- Ensure strict JSON validation on the frontend and backend to prevent unsafe configurations (e.g., negative obstacle distances) from being committed to the rover.

## Architecture
- **Configuration Storage:** JSON payloads are persisted in `data/config`. A dedicated `backups/` subdirectory handles rollback capabilities.
- **OTA Architecture:** Uploaded firmware payloads (`.bin`, `.tar.gz`) are temporarily stored in `data/ota_uploads`, checksummed by `OTAValidator`, and then passed to `OTADeployer` for flashing. Progress is streamed back to the frontend via `OTADeploymentEvent`.

## Safety & Constraints
- **OTA Locks:** The `OTAManager` enforces a strict singleton lock (`self.active_deployment`). A second OTA upload will be instantly rejected if a flash is currently in progress.
- **Power Warnings:** The UI clearly warns operators not to interrupt power during OTA flashes. 
- **Configuration Validation:** Hardcoded bounds in `ConfigurationValidator` ensure that malicious or typo-driven parameter changes (e.g., max_velocity = 500 m/s) are rejected before saving.
