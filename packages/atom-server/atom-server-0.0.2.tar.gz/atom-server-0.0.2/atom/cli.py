import subprocess
import multiprocessing
import click
import gunicorn

cli = click.Group()


@cli.command()
@click.option("--host", type=str, default='localhost', help="Enter server host.")
@click.option("--port", type=int, default=9000, help="Enter server port.")
@click.option("--workers", type=int, default=(multiprocessing.cpu_count() * 2), help="Enter thread count.")
@click.option("--daemon", type=bool, default=False, required=False, help="Start as daemon.")
def runserver(host, port, workers, daemon):
    gunicorn.SERVER_SOFTWARE = 'atom/0.0.1'
    host = f"{host}:{port}"
    cmd = ["gunicorn", "manage:handle_app", "--reload", "-b", host, f"--workers={workers}"]
    if daemon:
        cmd.append("--daemon")
    subprocess.run(cmd)


@cli.command()
def version():
    click.secho("Atom CLI 0.0.1", fg='green')
