"""The single declaration of what the candidate Dotmac ISP application is."""

from __future__ import annotations

import dotmac_ui
from dotmac_kernel.assembly import ProductAssemblySpec

from dotmac_isp.config import configuration_errors

ASSEMBLY_NAME = "dotmac-isp"


def build_spec() -> ProductAssemblySpec:
    """Compose the zero-domain walking skeleton.

    The first supported profile is a dedicated ISP: exactly one operator tenant
    in an otherwise unchanged tenant/RLS model. No code branches on that value.
    Domain manifests join only with their governed cohort and a real release.
    """
    return ProductAssemblySpec(
        name=ASSEMBLY_NAME,
        modules=(),
        module_planes=(),
        tenancy="single",
        platform_surface_enabled=False,
        web_enabled=True,
        packaged_static_dirs=(dotmac_ui.static_dir(),),
        packaged_template_dirs=(dotmac_ui.template_dir(),),
        stylesheets=(dotmac_ui.stylesheet_url(),),
        startup_checks=(configuration_errors,),
    )


__all__ = ["ASSEMBLY_NAME", "build_spec"]
