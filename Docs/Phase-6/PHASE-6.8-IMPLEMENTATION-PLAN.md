# Phase 6.8: Security & Access Control - Implementation Plan

## Executive Summary
Phase 6.8 hardens the Recon Rover V2 Ground Station by implementing a robust Security & Access Control Framework. This phase transitions the system from open access to a secure, authenticated, and audited environment using JSON Web Tokens (JWT) and Role-Based Access Control (RBAC), without disrupting the underlying real-time robotics logic.

## Objectives
- Implement `AuthenticationManager` to handle user login, password verification (bcrypt-ready), and account lockouts after excessive failed attempts.
- Build `TokenManager` to generate, validate, and refresh JWTs for session management.
- Develop `AuthorizationManager` to strictly enforce RBAC constraints before any critical action is executed on the EventBus.
- Create `AuditManager` to durably log all security-relevant events to disk (logins, authorization checks, configuration changes).
- Construct the `security.html` dashboard allowing Administrators to view active sessions, manage user roles, and search audit logs.

## Architecture
- **Authentication Pipeline:** User submits credentials -> `AuthenticationManager` checks lock status -> hashes input via `PasswordManager` -> compares to DB -> on success, calls `TokenManager` to issue a JWT.
- **Authorization Pipeline:** Before any API route executes an action, `SecurityManager.authorize_action()` validates the provided JWT and queries the `AuthorizationManager` to confirm the role has the necessary permission.
- **Audit Pipeline:** Every authentication attempt and authorization check automatically generates an `AuditEvent`, which is asynchronously serialized to a daily rotation log via `AuditManager`.

## Safety & Constraints
- **Fail Closed:** If a token is expired, missing, or malformed, the system defaults to DENY.
- **Lockout Policy:** 5 failed logins within a rolling window triggers a 5-minute hard lockout for the targeted account to mitigate brute-force attacks.
- **Token Expiration:** JWTs expire after 1 hour (configurable via `SecurityPolicy`), requiring active sessions to securely refresh their tokens.
