from bedrockz._imports import *
import typer
import questionary
from bedrockz import core as cr
from bedrockz import files as flz
from bedrockz import config as cfg
from anyio import run
app = typer.Typer()
items_app = typer.Typer()
app.add_typer(items_app, name="items")


linker = typer.Typer()
app.add_typer(linker, name="linker")




@linker.command("list")
def list_projects_pm():
    typer.echo(f"Selling item:")

async def _link_project(path: Path):
    async with cfg.get_config(path) as box:
        packages = flz.BrowniePM()
        bcopy = box.copy()
        prior_remappings = bcopy.get("solidity", {}).get("remappings", [])
        box.solidity.remappings = list(set(packages.remappings + prior_remappings))
        # merged = cr.automerge(box.copy(), bcopy)
        # logger.info(merged)
        # box.update(merged)
        
        logger.warning(box)
        

@linker.command("attach")
def link_project():
    is_curr: bool = questionary.confirm("Would you like to link the current project?").ask()
    if not is_curr:
        typer.secho("Not Linking the current working directory.", fg="red", bold=True)
        return 
    
    root = cfg.vscode_config()
    run(_link_project, root)


@linker.command("detach")
def unlink_project(user_name: str):
    typer.echo(f"Deleting user: {user_name}")


if __name__ == "__main__":
    app()
