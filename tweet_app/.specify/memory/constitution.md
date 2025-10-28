<!-- Sync Impact Report:
Version change: 0.0.0 → 1.0.0
Modified principles: N/A (initial creation)
Added sections: All sections (initial creation)
Removed sections: N/A (initial creation)
Templates requiring updates: ✅ plan-template.md (validated), ✅ spec-template.md (validated), ⚠ tasks-template.md (pending validation)
Follow-up TODOs: N/A
-->

# Tweet App Constitution

## Core Principles

### I. Feature Branch Workflow
One feature branch per task to ensure isolation, clear change tracking, and independent testing. Each feature MUST be developed in a dedicated branch that gets merged only after explicit verification and approval.

### II. Container-Only Development
Containers for everything - NO direct code execution allowed. All development, testing, and application execution MUST happen within containers. This ensures consistent environments and eliminates "it works on my machine" issues. Direct Python/npm execution is prohibited.

### III. Containerized Testing
Tests are containerized to guarantee consistent test execution and isolation. All test suites MUST run in containers with the same configuration as production environments.

### IV. Manual Release Process
No auto-merge to main; manual Release PR with explicit verification required. All releases MUST be manually reviewed, tested, and approved through a dedicated release pull request process. Create a detailed description of all changes, including rationales, in each PR.

### V. Documentation-Driven Development
Documentation lives in docs/*; single source of truth for all project knowledge. All architectural decisions, API specifications, and development guidelines MUST be documented in the docs directory. Avoid creating endless markdown files, be clear, concise, non-redundant and informative.

### VI. Architecture Decision Records
ADRs required for key decisions to maintain transparent decision-making process. All significant technical decisions MUST be documented with rationale, alternatives considered, and consequences.

### VII. Project-Scoped MCP Configuration
MCP servers configured at project scope only to ensure consistency and avoid configuration drift. All MCP server configurations MUST be project-level, never user-level or environment-specific.

## Development Standards

### Code Quality
- All code MUST follow established style guides
- All features MUST include comprehensive tests
- All changes MUST pass automated checks before PRs
- All documentation MUST be updated with code changes
- All code execution MUST happen within containers only

### Testing Requirements
- Unit tests MUST cover all business logic
- Integration tests MUST cover all service interactions
- End-to-end tests MUST cover critical user journeys
- All tests MUST run in containerized environments

## Release Management

### Version Control
- Semantic versioning MUST be followed (MAJOR.MINOR.PATCH)
- Main branch MUST always be stable and deployable
- Feature branches MUST be deleted after merge
- Release tags MUST be created for all releases

### Deployment Process
- All deployments MUST go through the release PR process
- Rollback plans MUST be documented for each release
- Deployment verification MUST be automated
- Monitoring MUST be in place for all deployed services

## Governance

This constitution supersedes all other development practices and guidelines. Amendments require:

1. Documentation of the proposed change with rationale
2. Team review and discussion
3. Formal approval through a governance PR
4. Migration plan for existing work
5. Version update following semantic versioning

All PRs and reviews must verify compliance with this constitution. Complexity must be explicitly justified in design documents. Use docs/development/guidelines.md for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-10-27 | **Last Amended**: 2025-10-27