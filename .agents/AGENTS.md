# Recon Rover V2 - Global Agent Rules

## GLOBAL DOCUMENTATION POLICY
Every engineering phase must have its own dedicated documentation.
Never reuse documentation from previous phases.
Never overwrite documentation from previous phases.
Every phase must be completely self-contained.

## DEPRECATED DOCUMENTS
The following files are permanently forbidden. Never create them. Never edit them. Never suggest them.
`implementation_plan.md`
`verification_plan.md`
`walkthrough.md`
`task.md`
`summary.md`
`report.md`
`design.md`
`notes.md`

## PHASE DOCUMENTATION STRUCTURE
For every phase X.Y automatically create:
`docs/Phase-X/PHASE-X.Y-IMPLEMENTATION-PLAN.md`
`docs/Phase-X/PHASE-X.Y.md`
`docs/Phase-X/PHASE-X.Y-VERIFICATION-PLAN.md`
`docs/Phase-X/PHASE-X.Y-VERIFICATION.md`
Each file must be created as a completely NEW document. Never overwrite previous phase files.

## IMPLEMENTATION PLAN
`PHASE-X.Y-IMPLEMENTATION-PLAN.md` must contain: Executive Summary, Objectives, Repository Analysis, Current Architecture, Technical Debt, Proposed Architecture, Folder Structure, Public APIs, EventBus Integration, Dependencies, Runtime Design, Memory Strategy, CPU Strategy, Risks, Migration Strategy, Deliverables, Engineering Recommendation.

## IMPLEMENTATION REPORT
`PHASE-X.Y.md` must contain: Executive Summary, Files Created, Files Modified, Architecture, Runtime Pipeline, EventBus Integration, Internal Tests, Memory Analysis, CPU Analysis, Production Readiness.

## VERIFICATION PLAN
Before starting ANY verification automatically create `PHASE-X.Y-VERIFICATION-PLAN.md` containing: Executive Summary, Verification Objectives, Verification Scope, Audit Strategy, Architecture Audit, Runtime Audit, Memory Audit, CPU Audit, Thread Safety Audit, Async Safety Audit, EventBus Audit, Internal Test Matrix, PASS / FAIL Criteria, Risks, Expected Deliverables.
Verification must NEVER begin before this document exists.

## VERIFICATION REPORT
After verification automatically create `PHASE-X.Y-VERIFICATION.md` containing ONLY: Executive Summary, Engineering Score, Final Verdict, Repository Ready, Known Risks, Engineering Recommendations limited ONLY to the completed phase.
Do NOT include "Recommended Next Phase", "Proceed to...", "Approved For Next Phase", or any similar roadmap recommendations.

## CHANGELOG
Every phase must append its completion into `docs/ENGINEERING-CHANGELOG.md`. Never overwrite previous entries.

## FINAL RESPONSE POLICY
After EVERY implementation or verification, explicitly list every generated document in the repository AND attach the documentation files as user-facing artifacts so they are available for download.

Example:
Generated Files:
- docs/Phase-X/PHASE-X.Y-VERIFICATION-PLAN.md
- docs/Phase-X/PHASE-X.Y-VERIFICATION.md
- docs/ENGINEERING-CHANGELOG.md

Attached Files:
📎 PHASE-X.Y-VERIFICATION-PLAN.md
📎 PHASE-X.Y-VERIFICATION.md

If any document could not be created, explicitly state FAILED TO CREATE followed by the filename and reason.

Finally end with:
Phase Completed.
Documentation Verified.
Awaiting next implementation prompt.

## PROJECT GOVERNANCE POLICY
I am NOT the project owner or architect. The roadmap and architecture are controlled exclusively by the Project Architect (ChatGPT).
- DO NOT recommend the next phase.
- DO NOT generate future architecture.
- Stop immediately after completing the requested phase.
- Only implement exactly what is described in the Implementation Prompt.
- Never expand scope, skip phases, merge phases, or redesign completed systems.
- Document any extra necessary work under "Future Improvements" without changing the roadmap.
