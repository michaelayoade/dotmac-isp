# dotmac-isp — hard rules

This file is canonical for this repository. `docs/ARCHITECTURE.md` records the
as-built boundary and `docs/adr/` records decisions. Reconcile drift toward
reality; never cite a plan as evidence of current behavior.

## 0. Containment and authority

`dotmac_sub` remains the production source authority until a cohort-specific
sealed switch. The new `src/dotmac_isp` package is the target assembly; it moves
no authority merely by building or deploying.

The inherited `src/dotmac/isp`, legacy `tests/`, and `frontend/` tree came from
`dotmac-ftth-ops`. They are frozen forensic/extraction material, not the future
runtime. They are excluded from the product wheel and the new runtime may never
import them. `docs/legacy-baseline.json` plus
`scripts/check_legacy_baseline.py` is a two-directional ratchet: any rise,
reduction, or byte change requires the baseline to move in the same reviewed
change. Never hide a legacy change by weakening the detector.

Bounded legacy changes are limited to security containment, evidence repair,
migration/shadow adapters, or retiring one local writer. They never count as
target adoption or cutover.

## 1. One thin assembly

`src/dotmac_isp/assembly.py` is the single product composition writer.
`src/dotmac_isp/main.py` is only `create_app(build_spec())`. Never instantiate
FastAPI, recreate kernel middleware, or copy a Starter surface locally.

Compose only exact released `dotmac-*` packages. Cross-repository path and
editable dependencies are forbidden. An unreleased declared version is a
blocker, not permission to pin it. A module joins only in the cohort that needs
it, with its plane selection, composed migrations, source disposition contract,
shadow proof, and retirement gate in the same programme slice.

## 2. Independent application boundary

This application owns its runtime, database, migrations, sessions,
authorization, and domain decisions. It never imports or reads another product's
tables, ORM, filesystem, session, or database—not during backfill or shadow.
Cross-application data arrives through versioned APIs/webhooks as typed,
deduplicated observations. Outbound synchronization uses a durable outbox.

For each cohort there is exactly one production writer. Shadow compares facts;
it does not decide state or cause consequences.

## 3. Database and tenancy

The dedicated first profile still keeps a real Tenant, tenant context,
composite tenant constraints, and PostgreSQL RLS. `tenancy="single"` is a
topology assertion, never a separate schema or code path.

Every future tenant table ships `tenant_id UUID NOT NULL`, composite uniques
and tenant FKs, and ENABLE + FORCE RLS with its policy and grants in the same
creation migration. `dotmac_kernel.db` is the transaction authority; services
flush and never commit or roll back. Migrations run as the migration role from
the deploy process, never at container boot.

## 4. Adapters and configuration

Routes, web handlers, tasks, workers, webhooks, CLI commands, and delivery
integrations validate, authorize, delegate, and render. Decisions live in one
named service.

Everything environment-specific is configuration with a documented safe
default or a required value. No secret value may appear in Git, synchronized
files, logs, prompts, reports, or memory. Keep only an OpenBao path or approved
runtime pointer. A runtime `.env*` file is never tracked; example files contain
names and non-secret local pointers only.

## 5. Governance and delivery

The coordinated target-build/Sub-cutover programme is owned by Governance PR
#20 until its accepted revision reaches `dotmac_governance/main`. This
repository's ADR 0001 stays Proposed until the named human review event. A
green build is structural evidence only; it does not approve a cutover.

- Branch before committing; never commit directly to `main`.
- Stage, commit, push, create/update a PR, mark ready, and merge only with the
  user's explicit authorization for that action.
- Merge only when every required GitHub check for the exact head is green and
  the required human approval is present.
- Production or SSH work requires Michael to name the target host explicitly.

## Validation

```sh
make check
make test
make image
```

Tests run in GitHub CI as the merge acceptance evidence. Local work is limited
to inspection, editing, formatting, lock generation, and static validation;
do not install or execute test suites locally unless Michael changes that
direction.
