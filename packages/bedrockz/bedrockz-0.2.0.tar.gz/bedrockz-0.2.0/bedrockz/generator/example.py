from bedrockz._imports import *
from jinja2 import Template, Environment, FileSystemLoader
from yapf.yapflib.yapf_api import FormatCode



def get_environment(path: Path) -> Environment:
    """Get the environment for a given path."""
    loader = FileSystemLoader(path)
    return Environment(loader=loader)

class TemplateRenderer:
    def __init__(self, path: Path) -> None:
        self.env = get_environment(path)
    
    @property
    def templates(self) -> list:
        """Get all templates in a path."""
        return self.env.list_templates()
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if hasattr(self, "env"):
            logger.debug(f"Setting {__name} to {__value} inside of the environment too.")
            self.env.globals[__name] = __value    
        self.__dict__[__name] = __value
    
    
    def render(self, template_name: str, context: dict = {}) -> str:
        """Render a template with a context."""
        template = self.env.get_template(template_name)
        return template.render(context)
    
    def render_python(self, template_name: str, context: dict = {}) -> str:
        """Render a template with a context."""
        unformatted = self.render(template_name, context)
        formatted_code, _ = FormatCode(unformatted)
        return formatted_code
    


def main():
    curr = Path(__file__).parent
    local_temp_folder = curr / "templates"
    renderer = TemplateRenderer(local_temp_folder)
    # logger.success(list(Path(local_temp_folder).glob("*")))
    logger.success(renderer.templates)
    renderer.decimal_count = 18
    renderer.token_name = "Coinye Coin"
    renderer.token_symbol = "CYC"
    complete = renderer.render("brownie/token.py.jinja2")
    expandsive = f"\n\n{complete}"
    
    logger.success(expandsive)
if __name__ == "__main__":
    main()