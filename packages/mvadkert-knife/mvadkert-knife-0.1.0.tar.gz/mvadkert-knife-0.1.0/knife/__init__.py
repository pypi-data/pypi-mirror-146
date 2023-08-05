import typer

import knife.containers

app = typer.Typer()
app.add_typer(knife.containers.app, name="containers")
