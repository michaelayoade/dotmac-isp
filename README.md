> # ⛔ FROZEN — 2026-08-22
>
> **This repository holds no programme control and receives no further
> construction.**
>
> Its premise was that legacy `dotmac_sub` would be replaced by an independent
> assembly running on its own host and database. That is no longer the accepted
> direction. **Dotmac Sub is not being retired**: it remains the ISP product,
> runtime, API identity, hostname and customer-facing application, and becomes
> the thin assembly *in place* — pinning kernel, UI and released domain modules,
> with each domain switching authority internally from legacy code to its
> module. Customers and mobile clients keep the same endpoints.
>
> The operative phrase is **"retire legacy Sub implementations, not Dotmac
> Sub."**
>
> Consequently there is no separate ISP production host, no second production
> database, no mobile API-base repoint, no cross-database sealing protocol and
> no external synchronisation layer. `dec-isp-002`, which asked which host would
> run this assembly, is **superseded rather than answered**.
>
> This repository is kept, not deleted: it is the record of a direction that was
> accepted and then corrected. Read the conversion amendment in Governance
> ADR-0012 (`docs/adr/0012-dotmac-isp-replacement-programme.md`, § "Conversion
> amendment — 2026-08-22") before doing anything here.

# Dotmac ISP

The candidate thin product assembly that will replace legacy `dotmac_sub` one
sealed cohort at a time.

This repository already contained a large `dotmac-ftth-ops` split. That code is
now a frozen extraction/reference region under `src/dotmac/isp`, `tests/`, and
`frontend/`; it is not packaged or imported by the new runtime. Its exact
tracked inventory is held by [`docs/legacy-baseline.json`](docs/legacy-baseline.json).

The authoritative candidate boot path is deliberately small:

```text
src/dotmac_isp/assembly.py  ProductAssemblySpec
src/dotmac_isp/main.py      app = create_app(build_spec())
```

It composes the released `dotmac-kernel 0.1.0a83` and `dotmac-ui 0.1.0a7` at
immutable source revisions. It composes zero domain modules because Party,
Customers, and Brand Profiles are not yet all released. A green skeleton earns
no adoption or cutover credit.

## Commands

```bash
make check   # exact toolchain, lock, lint, format, types, legacy ratchet
make test    # thin-assembly and architecture canaries
make build   # wheel
make image   # candidate container
make dev     # local candidate runtime
```

Copy `.env.example` for the online runtime. The deploy/migration process uses
the separate `.env.migration.example`; never load both into one process.

Tests run in GitHub CI. No production deployment or data authority is assigned
by this bootstrap.

See [`AGENTS.md`](AGENTS.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md),
and [`docs/adr/0001-thin-assembly-replacement.md`](docs/adr/0001-thin-assembly-replacement.md).
