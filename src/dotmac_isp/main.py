"""ASGI adapter: all product composition lives in ``assembly.build_spec``."""

from __future__ import annotations

from dotmac_kernel import create_app

from dotmac_isp.assembly import build_spec

app = create_app(build_spec())

__all__ = ["app"]
