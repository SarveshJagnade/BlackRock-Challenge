import typer
from BR_app.management.commands import runserver_command


app = typer.Typer(help="FastAPI management Commands")

app.add_typer(runserver_command.app)

if __name__ == "__main__":
    app()