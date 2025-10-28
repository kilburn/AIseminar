# Guideline: Adopting Spec Kit in an Existing Repo

1. Create a safe workspace
   Make a feature branch (e.g., `speckit-bootstrap`) and commit/stash all changes. This lets you trial Spec Kit without disrupting main.

2. Verify prerequisites
   Run `specify check` (after installing the CLI) to confirm Git, Python/uv, and AI agent availability. Prevents setup churn later.

3. Initialize in place
   From repo root: `specify init --here` (use `--force` only after committing). This adds Spec Kit scaffolding without moving files.

4. Establish your “Constitution”
   Run `/speckit.constitution` in your editor/agent to capture coding standards, testing minimums, security/privacy rules, performance SLOs, UX principles, and “never do” policies. This aligns future changes.

5. Baseline the current system
   Document what exists: domains, modules, external deps, data flows, build/test pipelines, and known constraints. Keep it factual—no solutions yet.

6. Specify the desired change
   Use `/speckit.specify` to write requirements: user stories, non-functional constraints, acceptance criteria, out-of-scope items, and migration needs. This becomes your source of truth.

7. Plan against the real codebase
   Run `/speckit.plan` to propose architecture changes, integration points, data contracts, and rollout/migration steps. Call out risks and mitigations.

8. Decompose into tasks
   Use `/speckit.tasks` to create small, testable work items with owners and dependencies. Map each task back to spec sections for traceability.

9. Pre-implementation checks
   Run `/speckit.analyze` and `/speckit.checklist` to catch ambiguities, missing test plans, security/privacy gaps, and operational concerns before coding.

10. Implement iteratively
    Run `/speckit.implement`. Keep commits small; each PR should reference the spec clause it satisfies. Maintain backward compatibility or include a migration plan.

11. Test with intent
    Add/extend unit, integration, and contract tests anchored to acceptance criteria. Include negative tests and performance/regression checks when relevant.

12. Document and link artifacts
    Update README/ADR/wiki minimally; centralize decisions in Spec Kit files (constitution/spec/plan/tasks). Ensure PRs link to spec sections and checklists.

13. Review and sign-off
    Use the constitution and acceptance criteria as the review lens. Require at least one domain reviewer and one QA/ops reviewer for production-facing changes.

14. Release and observe
    Roll out behind a flag if possible. Add monitoring/alerts aligned with SLOs from the constitution. Define rollback triggers and steps.

15. Maintain and iterate
    After release, fold learnings back into the constitution/specs. Close tasks with outcomes and metrics; retire temporary flags/migrations promptly.

---

## Quick command recap (minimal)

```bash
# install & check
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
git checkout -b speckit-bootstrap
specify check

# init in existing repo
specify init --here       # add --force only after you’ve committed

# in your AI editor/agent
/speckit.constitution
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
```

## Do/Don’t (at a glance)

* Do: commit first, keep tasks small, tie PRs to spec clauses, test per acceptance criteria, observe SLOs.
* Don’t: skip the constitution, overuse `--force`, or implement without a migration/rollback plan.

## Bonus:
Claude code gather information prompt:

```markdown
# Prompt: Generate a Tailored Spec Kit Guideline (single Markdown, no intermediates)

**Role:** You are a principal engineer working inside Claude Code on an existing repository.
**Objective:** Produce a single, project-specific **Spec Kit Guideline** in Markdown that tells this team exactly how to adopt and use Spec Kit in this repo. The file must be self-contained, accurate to the repo, and production-quality.
**Key constraints:**

* **Output exactly one file:** `SPECKIT_GUIDE.md` in the repo root.
* **Do not commit or change source files.**
* **No leftover temp files or folders.** If you need scratch files, keep them under a temporary directory you create and delete (e.g., `.speckit-tmp/`).
* Prefer facts derived from manifests/configs over guesses; if unknown, list them as **Open Questions**.

---

## What to detect (scan the repo)

1. **Stack & Tooling**

   * Languages; frameworks; package/dependency managers; build tools; test frameworks; linters/formatters; container/infra tooling; dev server tooling.
   * App type(s): CLI, service/API, web app, mobile, library, mono/multi-repo; primary entrypoints.
2. **Build/Test/Run**

   * Exact commands to install, build, test, lint/format, run locally; typical environment variables.
   * CI/CD: where defined, required checks, environments, artifact publishing, versioning/release strategy (tags/semver/changelog).
3. **Architecture & Dependencies**

   * High-level textual architecture diagram; core modules/boundaries.
   * Critical first-party modules; critical third-party deps and why they’re used.
4. **Data & Integrations**

   * Datastores (DB, cache, queue), schema/migrations location; seed/process scripts.
   * External services/APIs, auth flows, secrets mgmt method.
5. **Operations**

   * Environments (dev/stage/prod), config strategy (.env/vault/flags).
   * Observability (logs, metrics, traces, dashboards, alerts, SLIs/SLOs).
   * Perf hotspots or large bundles; reliability patterns (retries, idempotency, CB).
6. **Quality & Risk**

   * Test coverage status/shape; hardest-to-test areas; security posture (SCA/SAST/DAST, secret scanning).
   * Compliance constraints (e.g., PII/GDPR/HIPAA) and where relevant code lives.
7. **Team Workflow**

   * Trunk vs PR-driven; CODEOWNERS; review rules; commit/PR conventions; release cadence; hotfix/rollback; feature flags/migrations.
8. **UX/Product**

   * Primary user journeys; A11y/i18n/l10n footprints; acceptance criteria patterns.

**Look for these files/paths automatically (if present):**

* Deps: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock`, `pyproject.toml`, `requirements*.txt`, `Pipfile`, `go.mod`, `Gemfile`, `Cargo.toml`, `composer.json`
* Build/Test: `Makefile`, `justfile`, `tox.ini`, `noxfile.py`, `vite.config.*`, `webpack.config.*`, `rollup.config.*`, `tsconfig.json`
* Lint/Format: `.eslintrc*`, `.prettierrc*`, `ruff.toml`, `.flake8`, `pylintrc`, `.editorconfig`
* CI/CD: `.github/workflows/*.yml`, `gitlab-ci.yml`, `.circleci/config.yml`, `azure-pipelines.yml`, `Jenkinsfile`
* Runtime/Infra: `Dockerfile*`, `docker-compose*.yml`, `Procfile`, `helm/`, `terraform/`, `pulumi/`
* Observability: `otel*`, `prometheus*`, `grafana/`, `datadog/`, `newrelic*`, logging/tracing utils
* Security: `CODEOWNERS`, `SECURITY.md`, `dependabot.yml`, `renovate.json*`, `.gitleaks*`
* Docs/Tests/Entrypoints: `README*`, `CONTRIBUTING*`, `ADR*`, `docs/`, `tests/`, `__tests__/`, `src/server.*`, `main.*`, `cmd/`

---

## Required output (write to `SPECKIT_GUIDE.md`)

Produce a polished Markdown with these **sections in this exact order** (generate tailored content, not placeholders, except where info is truly unknown):

````markdown
# Spec Kit Guideline for <repo-name>

## 1. Purpose
Concise explanation of why Spec Kit is being adopted here and what outcomes we expect in THIS repo.

## 2. Prerequisites (Repo-Specific)
- Tools and minimum versions (pin based on repo findings).
- Verified commands to check readiness (e.g., `uv --version`, `node --version`, `python -V`, `docker --version`).
- Where to configure the preferred AI agent for this team.

## 3. Quickstart (Copy-Paste)
```bash
# safe bootstrap
git checkout -b speckit-bootstrap
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify check
specify init --here   # use --force ONLY after committing a clean state
````

Notes that are SPECIFIC to this repo (mono vs poly, workspaces, virtualenv/poetry/pnpm, etc.).

## 4. Our Constitution (Tailored)

Concrete, enforceable rules for THIS repo:

* Coding standards (formatter/linter as source of truth, naming, architectural boundaries).
* Testing minimums (levels required per PR, coverage floors by package, contract tests where needed).
* Security & privacy (secrets handling, auth patterns, allowed crypto, dep policy).
* Performance & reliability SLOs (numbers and how we measure them).
* Observability requirements (logs/metrics/traces for endpoints/jobs; dashboards/alerts we maintain).
* UX principles (A11y baseline, design tokens, i18n rules).
* Never Do (outlawed libs/patterns for this codebase).

## 5. How We Specify Changes

* When to write a spec; linking to user stories/issues.
* Template tuned to this stack (include Gherkin examples that fit our testing style).
* Required acceptance criteria and data/compat constraints we commonly face.

## 6. Planning Against This Codebase

* Recommended module boundaries for new work; integration seams.
* Data contracts (HTTP/GRPC/GraphQL/DB) and validation strategy used here.
* Migration/feature-flag approach used here; rollback triggers and steps.

## 7. Tasks & Execution

* How we decompose into ≤1-day tasks; ownership & dependencies.
* Branching model for this team (trunk vs PR-driven), CODEOWNERS, required checks.
* Commit/PR conventions with examples that reference spec clauses.

## 8. Implementation Workflow (Commands)

Exact commands for build/test/lint/format/run in THIS repo, plus:

```bash
/speckit.constitution
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
```

And any repo-specific env vars or docker compose steps.

## 9. Testing Strategy (Repo-Tuned)

* Unit/integration/contract/e2e locations, fixtures, and how we run them in CI.
* Minimal smoke tests required for new modules.
* Performance & regression tests, load/gen tooling if present.

## 10. Security & Compliance

* How dependency and secret scanning run here (tools, schedule, PR gates).
* AuthN/Z patterns, data handling (PII/GDPR/etc.) with repo paths to relevant code.
* Threat model notes and common footguns in this repo.

## 11. Observability Playbook

* What to log/measure/trace for new endpoints/jobs.
* Where dashboards/alerts live; SLI/SLOs with thresholds.
* Runbooks/rollback docs locations.

## 12. Release & Rollout

* Versioning strategy, changelog, release branches/tags.
* Canary/feature flags and dark-launch steps for this stack.
* Post-release checks and metrics to watch.

## 13. Checklists

* Author PR checklist (tailored).
* Reviewer checklist (domain + QA/ops).
* Pre-merge CI checklist (required jobs).
* Release checklist (flags, migrations, dashboards).

## 14. Slash-Command Cookbook (For Our Stack)

Short, high-signal examples of the most common Spec Kit flows we will use here.

## 15. Appendix

* Repo Snapshot (stack/tooling/architecture/data/integrations/operations) discovered from files.
* File Map: where our Constitution/Spec/Plan/Tasks live in this repo once initialized.
* Open Questions (explicit unknowns with suggested owners).

```

**Important:** everything above must be **tailored** to detected tooling and patterns. Only use placeholders under **Open Questions**.

---

## Workflow to follow (inside Claude Code)
1) **Scan files** listed above (read-only).  
2) Build an in-memory snapshot (no files yet).  
3) If you must write scratch content, do it under `.speckit-tmp/`.  
4) Render the final Markdown to `SPECKIT_GUIDE.md` at repo root.  
5) **Delete `.speckit-tmp/`** entirely so no intermediate files remain.  
6) **Final console output**: print only this line if successful:  
```

WROTE: SPECKIT_GUIDE.md

```
If you couldn’t determine something, list it in **Open Questions**.

**House rules**
- Do not run or modify the project. Read files only.  
- Prefer concrete commands/code over prose.  
- Keep it concise but complete; assume senior engineers are the readers.

---

## Optional inputs (if the user provides them)
If available, incorporate:
- **Workflow**: trunk-based or PR-driven; required reviewers.  
- **SLO targets**: e.g., p95 latency, error budget, uptime.  
- **Coverage floors** per package.  
- **Flag/migration** tooling standards.

If any of these are not provided and not derivable, add them to **Open Questions** with sane recommendations.

```