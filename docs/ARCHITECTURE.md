# Dotmac ISP architecture

## Current authority state

Legacy `dotmac_sub` is production-authoritative for every ISP cohort. This
repository is a candidate target and owns no production decision, writer, or
customer consequence yet.

The repository contains two sharply separated regions:

| Region | Status | Canonical owner | Consumer |
| --- | --- | --- | --- |
| `src/dotmac_isp` | candidate target runtime | `src/dotmac_isp/assembly.py` | wheel, container, CI |
| `src/dotmac/isp` | frozen inherited prototype | legacy baseline control | none in target runtime |
| legacy `tests/` and `frontend/` | frozen inherited evidence/debt | legacy baseline control | no merge credit |

`scripts/check_legacy_baseline.py` owns the exact tracked inventory and
`docs/legacy-baseline.json` is its reviewable ratchet. The target package cannot
import `dotmac`, `dotmac_sub`, `dotmac_erp`, `dotmac_crm`, `vendor_cp`, or the
Starter reference assembly `app`.

## Product composition

`src/dotmac_isp/assembly.py` is the single declaration of product composition.
`src/dotmac_isp/main.py` delegates directly to kernel `create_app`; it owns no
middleware or route decisions.

The walking skeleton composes:

| Surface | Exact release | Immutable source revision | State |
| --- | --- | --- | --- |
| `dotmac-kernel` | `0.1.0a83` | `4cfdcd76739c9ad6c6dc249c1093849db7c3b752` | composed |
| `dotmac-ui` | `0.1.0a7` | `042532d2c80ee7a56b14b71269d15459288312c2` | composed |
| Party | none released | — | cohort 1 blocked |
| Brand Profiles | none released | — | cohort 1 blocked |
| Customers | not built/released | — | cohort 1 blocked |

The module tuple is deliberately empty. A package appearing on Starter main is
not a release and is not composable evidence.

## Runtime and data boundary

- Product name: `dotmac-isp`.
- First topology: dedicated ISP (`tenancy="single"`) while retaining the
  kernel Tenant/RLS model.
- Online platform surface: disabled; external control-plane concerns remain
  outside this data plane.
- Database: one independent Dotmac ISP PostgreSQL database. The online runtime
  holds only its online DSN. Migration authority is a separate deploy process.
- Cross-application integration: versioned APIs/webhooks and durable messages,
  never a foreign DSN or ORM import.
- Deployment: none approved or performed by this bootstrap.

The candidate container runs `dotmac_isp.main:app` as a non-root user and never
runs migrations at boot. `compose.yaml` is the default candidate launch surface
and requires the independent online DSN. The old `docker-compose.yml`,
entrypoint, and service/frontend assets remain frozen legacy material; they are
not evidence of the target runtime and will be retired in a separately reviewed
ratchet change.

## Cohort-1 join

The target-build and Sub-cutover tracks proceed concurrently, but meet only at
one cohort proof:

1. release and exact-pin Party, Brand Profiles, and Customers;
2. define the Sub Party/Customer versioned export contract;
3. classify every source row as accepted, quarantined, or evidenced retirement;
4. replay idempotently into a disposable target database;
5. compare the complete cohort at an immutable watermark; and
6. perform no authority switch until the Governance controls are verified.
