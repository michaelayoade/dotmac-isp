# 0001. Dotmac ISP is a thin replacement assembly

- Status: Proposed
- Date: 2026-08-20
- Owner: Michael Ayoade
- Approver: Michael Ayoade (intended while Proposed)
- Scope: `michaelayoade/dotmac-isp`, legacy `dotmac_sub`, and Starter package composition
- Classification: Internal

## Context

The existing repository is a large 2025 split from `dotmac-ftth-ops`. Its
runtime hand-builds FastAPI, depends on a sibling `dotmac-shared` checkout,
duplicates domain owners now assigned to Starter modules, tracks generated
dependency trees, and has no green GitHub CI baseline. Treating it as the new
authority would recreate the parallel writers the replacement programme exists
to retire.

Governance PR #20 proposes the coordinated programme: build this independent
target while Sub completes source-readiness, bounded shadow, sealed cohort
switches, and displaced-writer retirement. Michael approved that direction and
named `michaelayoade/dotmac-isp` in the 2026-08-20 working session. The global
record remains non-normative until the approval event and accepted revision are
recorded and merged in Governance.

## Decision

If accepted, `src/dotmac_isp` is the sole target runtime package. It composes
kernel `ProductAssemblySpec` and `create_app`; it never imports the inherited
`src/dotmac/isp` tree or another product data plane.

The first slice is a zero-domain walking skeleton on exact immutable revisions
of released `dotmac-kernel 0.1.0a83` and `dotmac-ui 0.1.0a7`. Party, Brand
Profiles, and Customers remain cohort-1 blockers until real releases exist.
Declared-but-unreleased packages are not substituted with paths, editables, or
copied code.

The existing application remains frozen and excluded from the product wheel.
Its backend, tests, frontend, tracked dependency tree, and runtime-environment
debt are held by a two-directional inventory/digest ratchet. A bounded legacy
change updates that ratchet in the same reviewed change and explains which
transition purpose it serves.

Dotmac ISP owns an independent database and never receives a Sub/ERP/CRM/vendor
control-plane DSN. The dedicated first profile declares one operator tenant but
retains tenant context and RLS. Migrations never run at container boot.

## Consequences

- Building and deploying the skeleton moves no production authority.
- The inherited application's previously failing tests are not reclassified as
  passing. They are frozen evidence; the target has its own fail-closed CI.
- The candidate VCS pins are immutable and correspond to annotated release
  tags, but private-index wheel installation remains a required pre-cutover
  artifact proof.
- The tracked `node_modules` estate is explicit debt and must be retired in a
  focused baseline-lowering change; it cannot grow or disappear invisibly.
- Two inherited billing-extension files received syntax-only repairs so the
  accepted Governance engine can parse and measure the frozen region. The
  legacy backend digest records those exact repairs; the files remain outside
  the target wheel and runtime.
- The removed runtime `.env.local` path may have exposed material in public Git
  history. It is marked non-diffable so the removal does not reproduce its
  contents in review. Any non-placeholder credential from that file requires
  rotation; deleting the current-tree copy does not erase history.

## Drift prevention

- Architecture tests reject foreign/legacy imports and direct FastAPI
  construction, and include sensitivity proofs for both detectors.
- Build tests require the exact Starter revisions, the new package-only wheel,
  the new container entrypoint, pinned Actions, and no ignored CI failure.
- `scripts/check_legacy_baseline.py` compares exact Git blob identities and
  counts in both directions; sensitivity tests change a digest and lower a
  count to prove the detector fails.
- The Governance standards workflow is pinned to an exact accepted Governance
  revision and validates the assembly and legacy-containment authorities.
- This ADR remains Proposed until the named human approval event is recorded in
  the repository review process.
