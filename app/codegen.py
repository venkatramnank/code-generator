"""Code Generator base module.
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class CodeGenerator:
    def __init__(self, templates_dir=None):
        templates_dir = templates_dir or "./templates"
        self.template_list = [p.stem for p in Path(templates_dir).iterdir() if p.is_dir()]
        self.env = Environment(
            loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True
        )

    def render_templates(self, template_name: str, config: dict):
        """Renders all the templates from template folder for the given config.
        """
        file_template_list = (
            template
            for template in self.env.list_templates(".jinja")
            if template.startswith(template_name)
        )
        for fname in file_template_list:
            # Get template
            template = self.env.get_template(fname)
            # Render template
            code = template.render(**config)
            # Write python file
            fname = fname.strip(f"{template_name}/").strip(".jinja")
            self.generate(template_name, fname, code)
            yield fname, code

    def generate(self, template_name: str, fname: str, code: str) -> None:
        """Generates `fname` with content `code` in `path`.
        """
        path = Path(f"dist/{template_name}")
        path.mkdir(parents=True, exist_ok=True)
        (path / fname).write_text(code)

    def make_archive(self):
        raise NotImplementedError
