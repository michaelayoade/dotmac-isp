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
