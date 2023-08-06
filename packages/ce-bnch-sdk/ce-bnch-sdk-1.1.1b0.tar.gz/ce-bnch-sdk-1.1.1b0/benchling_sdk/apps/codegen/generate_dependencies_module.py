from jinja2 import Environment, PackageLoader

from benchling_sdk.apps.codegen.helpers import reformat_code_str
from benchling_sdk.apps.types.manifest import Manifest


def generate_dependencies_module(manifest: Manifest) -> str:
    env = Environment(
        loader=PackageLoader("benchling_sdk.apps.codegen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("dependencies.py.jinja2")
    return reformat_code_str(template.render(manifest=manifest))
