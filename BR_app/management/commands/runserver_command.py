import typer
import uvicorn

app = typer.Typer(help="Runserver command")

@app.command()
def runserver(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
    workers: int = 1,
    log_level: str = "info",
):
    print(f"Running server on {host}:{port} with {workers} workers, reload={reload}, log_level={log_level}")
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers,
            log_level=log_level
        )
    except Exception as e:
        print(f"Error starting server: {e}")