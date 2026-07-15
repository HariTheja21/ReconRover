# Phase 6.7: Multi-Operator Collaboration - Implementation Plan

## Executive Summary
Phase 6.7 introduces the Multi-Operator Collaboration Framework, transforming the Ground Station from a single-user dashboard into a synchronized, multi-tenant command center. This phase focuses on safely coordinating control ownership (e.g., who is currently driving the rover) and enforcing strict role-based access control (RBAC) to prevent operator conflicts.

## Objectives
- Implement `OperatorManager` and `SessionCoordinator` to track operator presence, handling connect, disconnect, and idle timeout events.
- Build `RoleManager` and `PermissionManager` to define granular permissions (e.g., DRIVE, MISSION, CAMERA, OTA) across 6 distinct operator roles (Administrator, Mission Commander, Pilot, Observer, Diagnostics, Maintenance).
- Implement `OwnershipManager` to enforce mutual exclusion on critical resources, ensuring two operators cannot send conflicting drive commands simultaneously.
- Create `collaboration.html` with a synchronized Activity Feed and Presence Sidebar to provide operators with live situational awareness of their team.

## Architecture
- **Presence Pipeline:** Operators connect via WebSockets. The `SessionCoordinator` monitors heartbeats. If a heartbeat is missed for 5 minutes, the operator is marked `IDLE`. If the socket drops, they are marked `OFFLINE` and all owned resources are forcibly released via `OwnershipManager.release_all_for_operator()`.
- **Ownership Pipeline:** An operator must explicitly request control of a resource via the UI. The request flows to `OwnershipManager`, which queries `PermissionManager`. If approved and available, control is granted, and an `OwnershipTransferEvent` is broadcast to all connected clients, locking the UI buttons for others.

## Safety & Constraints
- **Mutual Exclusion:** `OwnershipManager` maintains a strict 1:1 mapping of Resource-to-Operator. Conflicting requests are instantly rejected on the backend.
- **Admin Override:** Operators with the "Administrator" role can forcibly seize control of a resource from a lower-tier operator to resolve emergencies.
- **Dangling Locks:** Network drops immediately strip an operator of their locks, preventing a scenario where a disconnected pilot permanently locks out the drive controls.
