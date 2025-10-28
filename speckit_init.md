Generation process: https://chatgpt.com/share/68fff583-a7e4-800e-a271-d0ea2b79d6d4

# SPEC_INIT — Seminar Initialization Guide

> TweetEval Interactive NLP Dashboard — End‑to‑end, docker‑first, MCP‑enabled stack

---

## 1. Objective

Establish a repeatable, reviewable initialization flow for a Spec‑Kit–driven project. The outcome is a clean repository with enforceable governance, branch discipline, MCP configuration, containerized services, and step‑gated delivery across database, API, vector search, datasets, and web UI.

## 2. Audience & Scope

* Audience: engineering teams, leads, and reviewers attending a professional seminar; AI coding assistants (Claude Code, Copilot) operating under explicit guardrails.
* Scope: initialization and the first delivery milestones (DB → API → Qdrant → Data ingestion → WebUI). CI/CD specifics and production SRE hardening are out of scope for this document but linked through placeholders.

## 3. Governance & Ground Rules

* **Single‑source documentation**: no duplication; canonical docs live under `docs/*`; link to sources instead of copying.
* **Branch discipline**: exactly one feature branch per task; three long‑lived branches:

  * `main` — last finished and tested task set (manual promotion only).
  * `develop` — current completed and tested subtasks.
  * `current` — work‑in‑progress branch for the active subtask.
* **Merge policy**:

  * Feature branches → `develop` via PR after green tests.
  * `develop` → `main` **manual** Release PR with summary and verification checklist.
* **Containers**: all services dockerized; tests run in containers; no host‑only assumptions.
* **MCP**: servers added at **project scope** in Claude Code (PostgreSQL, Qdrant, GitHub, Docker).

## 4. Repository Layout (clean root)

```
tweet_app/
├─ backend/                  # FastAPI service, SQLAlchemy models, Alembic
├─ frontend/                 # Vue 3 + Vite + Tailwind
├─ infra/
│  └─ docker/
│     ├─ dev/
│     ├─ test/
│     └─ prod/
├─ docs/
│  ├─ architecture/
│  ├─ api/
│  ├─ ops/
│  ├─ runbooks/
│  ├─ decisions/            # ADR-XXXX-title.md
│  └─ datasets/
├─ scripts/
├─ .github/
│  └─ pull_request_template.md
├─ docker-compose.yml        # thin root entrypoint or symlink to infra/docker/dev
└─ README.md
```

## 5. Initialization Flow (Spec‑Kit + Git)

### 5.0. Install the CLI

#### Prerequisites: uv

**macOS / Linux**

```bash
/bin/bash -c "$(curl -L micro.mamba.pm/install.sh)"
```

```bash
source ~/.bashrc
```

```bash
micromamba --version
```

```bash
micromamba create -n aiSeminar python=3.12
```

```bash
micromamba activate aiSeminar
```

```bash
micromamba install uv
```

---

**Windows (PowerShell)**

```powershell
Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1 -UseBasicParsing | Invoke-Expression
```

```powershell
micromamba --version
```

```powershell
micromamba create -n aiSeminar python=3.12
```

```powershell
micromamba activate aiSeminar
```

```powershell
micromamba install uv
```

#### specify-cli installation

Run this command (persistent installation):

```
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Or for a one-time usage:

```
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

### 5.1 Bootstrap

```bash
specify init tweet_app
cd tweet_app

git checkout -b develop
git checkout -b current/bootstrap
mkdir -p infra/docker/{dev,test,prod} docs/{architecture,api,ops,runbooks,decisions,datasets} scripts .github
claude
/sandbox
```

Commit: `chore: repo skeleton and hygiene rules` → PR into `develop` with the template in §10.

### 5.2 Constitution (project principles)

```
/speckit.constitution
- One feature branch per task; containers for everything; tests are containerized.
- No auto‑merge to main; manual Release PR with explicit verification.
- Documentation lives in docs/*; single source of truth; ADRs required for key decisions.
- MCP servers configured at project scope only.
```

### 5.3 Specification (what & why)

```
/speckit.specify
Build a FastAPI + Vue stack backed by PostgreSQL and Qdrant to power TweetEval‑based interactive NLP analysis with semantic search and visualizations.
```

### 5.4 Plan (how)

```
/speckit.plan
Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, sentence‑transformers.
Frontend: Vue 3, Vite, Tailwind, Pinia, Playwright.
Infra: Docker Compose profiles (dev/test/prod). MCP: Postgres, Qdrant, GitHub, Docker.
```

### 5.5 Task Breakdown (first milestones)

```
/speckit.tasks
1) PostgreSQL + seed + dockerized unit tests + Claude MCP Postgres check.
2) API ↔ PostgreSQL with tests (success, failure, edge).
3) Qdrant service + MCP + smoke tests.
4) API + Qdrant integration with tests.
5) Ingest TweetEval stance dataset with full metadata preservation.
6) WebUI homepage in Docker with unit + e2e smoke tests.
7+) Remaining pages, each with tests. Each page a different task/milestone
```

## 6. Branching Protocol (per milestone)

* Create `feature/<slug>` then derive `current/<slug>` for WIP.
* Push `current/*` early; open PR from `current/*` → `develop` when tests pass.
* After merge, delete `current/*`; keep `feature/*` closed.
* Promote `develop` → `main` only via Release PR after manual verification (§9).

## 7. MCP Configuration (Claude Code, project scope)

```bash
# GitHub MCP (requires PAT with repo scope)
claude mcp add --scope project github npx -- @modelcontextprotocol/server-github

# PostgreSQL MCP (read‑only recommended)
claude mcp add --scope project postgres npx -- @modelcontextprotocol/server-postgres
POSTGRES_URL=postgresql://app:app@localhost:5432/tweeteval

# Qdrant MCP
claude mcp add --scope project qdrant npx -- @qdrant/mcp-server-qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=<if configured>

# Docker MCP via Docker Desktop Toolkit (enable in Docker Desktop; approve in Claude Code)
```

## 8. Step‑Gated Milestones (commands & checks)

### M1 — PostgreSQL foundation

Branches:

```bash
git checkout -b feature/db-postgres
git checkout -b current/db-postgres
```

Infra (dev excerpt):

```yaml
# infra/docker/dev/docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: tweeteval
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports: ["5432:5432"]
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./sql/init:/docker-entrypoint-initdb.d
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports: ["5050:80"]
volumes:
  pgdata:
```

Tests (containerized): ensure at least 1 success, 1 deliberate failure, 1 edge.
Gate checks:

* DB up; Alembic `upgrade head` succeeds.
* Seed script populates non‑empty tables.
* Claude MCP Postgres server visible and can run a read‑only `SELECT`.

### M2 — API ↔ PostgreSQL

* Endpoints: `/health`, `GET /tweets/{id}`, `POST /tweets`, `GET /stance?target=...`.
* Tests: success (found), failure (404), edge (422 invalid payload).
* Containerized pytest via `infra/docker/test/docker-compose.test.yml`.
  Gate checks:
* All three API tests green.
* Error mapping conforms to spec.

### M3 — Qdrant service + MCP

* Add Qdrant container (port 6333) to dev/test compose.
* Init script to create collection and schema.
* Tests: success (insert + query), failure (wrong collection), edge (zero‑vector).
  Gate checks:
* MCP Qdrant server visible; basic similarity query works.

### M4 — API + Qdrant integration

* Endpoints: `POST /embeddings/index`, `GET /search?q=...`.
* Strategy: transactional write (Postgres first, then Qdrant) with retry/compensation.
* Tests: success (returns similar), failure (missing collection), edge (empty query).
  Gate checks:
* End‑to‑end search returns non‑empty results for seeded data.

### M5 — TweetEval stance dataset ingestion

* Fetch `https://github.com/cardiffnlp/tweeteval/tree/main/datasets`.
* Ingest stance splits, preserve all metadata (target, label, ids, file provenance).
* Emit `docs/datasets/stance_manifest.json` with file list, checksums, counts.
* Tests: success (sample ingest), failure (missing files), edge (malformed line).
  Gate checks:
* Row counts align with manifest; metadata columns non‑null as specified.

### M6 — WebUI homepage

* Vue 3 + Vite + Tailwind; health widget; simple search box hitting API.
* Tests: Vitest unit (render), failing case (missing prop), edge (empty input); Playwright smoke.
  Gate checks:
* Frontend container serves homepage; e2e smoke green.

### M7+ — Remaining pages

* One page per feature branch; each includes unit + e2e tests and API contracts updated in `docs/api/*`.

## 9. Promotion to `main` (manual)

Create a **Release PR** from `develop` to `main` including:

* Feature list (linked PRs), schema changes (Alembic revisions), dataset manifest link, API routes added, UI pages added.
* Verification checklist:

  * `docker compose -f infra/docker/prod/docker-compose.yml up -d --build`
  * API `/health` OK; migrations applied; Qdrant healthy.
  * Search returns non‑empty results.
  * WebUI loads and interacts with API.
  * Test suite: `infra/docker/test/docker-compose.test.yml` green.
* Rollback: revert migration; restore previous image tags; clear Qdrant collection if needed.

## 10. PR Template (`.github/pull_request_template.md`)

```markdown
## Summary
Concise description of what changed and why.

## Changes
- Bullet points of key changes

## Tests
- [ ] Unit (ok/fail/edge)
- [ ] Integration (db/api)
- [ ] E2E (if applicable)

## Risks & Rollback
Risk level and clear rollback steps.

## Docs
- [ ] Updated canonical doc(s) and linked references
```

## 11. Testing Matrix (per milestone)

| Milestone | Unit     | Integration | E2E | Notes                |
| --------- | -------- | ----------- | --- | -------------------- |
| M1 DB     | ✅/❌/Edge | —           | —   | Seed + constraints   |
| M2 API    | ✅/❌/Edge | DB‑backed   | —   | httpx/pytest         |
| M3 Qdrant | ✅/❌/Edge | —           | —   | Upsert/search        |
| M4 API+Q  | ✅/❌/Edge | API⇄DB⇄Q    | —   | Transactional writes |
| M5 Ingest | ✅/❌/Edge | DB          | —   | Manifest checks      |
| M6 WebUI  | ✅/❌/Edge | API         | ✅   | Playwright smoke     |

## 12. Documentation Policy

* Canonical diagrams: `docs/architecture/diagram.md`.
* API contracts: `docs/api/*` generated from FastAPI and refined manually where needed.
* Datasets: `docs/datasets/*` maintain provenance and manifests.
* Decisions: `docs/decisions/ADR-XXXX-title.md` for significant choices.

## 13. Risk Considerations

* Supply‑chain for MCP servers: pin versions; update regularly.
* Data migrations: forward‑only with tested downgrade scripts where feasible.
* Vector drift: record embedding model version and collection schema in metadata.

## 14. Ready‑to‑Copy Command Appendix

```bash
# Branches
git checkout -b develop
git checkout -b current/bootstrap

# Speckit core
specify init tweet_app --ai copilot
/speckit.constitution
/speckit.specify
/speckit.plan
/speckit.tasks

# MCP (project scope)
claude mcp add --scope project github npx -- @modelcontextprotocol/server-github
claude mcp add --scope project postgres npx -- @modelcontextprotocol/server-postgres
claude mcp add --scope project qdrant npx -- @qdrant/mcp-server-qdrant
```

---

**Outcome**: a reproducible initialization playbook that enforces branch discipline, documentation quality, MCP readiness, and step‑gated delivery across the core components of the TweetEval Interactive NLP Dashboard.
