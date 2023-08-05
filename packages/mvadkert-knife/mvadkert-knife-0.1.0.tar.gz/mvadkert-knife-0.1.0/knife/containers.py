import typer

import knife.registry

app = typer.Typer()
app.add_typer(knife.registry.app, name="registry")

if __name__ == "__main__":
    app()
