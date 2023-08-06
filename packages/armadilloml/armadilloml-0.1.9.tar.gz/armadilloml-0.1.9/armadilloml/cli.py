import os
import time
import uuid
import shutil
import requests
import rich_click as click
from git import Repo
from rich.console import Console
from typing import Optional
from .github import create_github_repository
from .utils import validate_id, get_armadillo_url
from .templating import render_template_directory

console = Console()


@click.command()
@click.option(
    "--environment",
    default="PRODUCTION",
    help="The environment to deploy to.",
)
def login(environment: str):
    """
    Login to Armadillo. Under the hood, this creates a session ID in Armadillo
    that is sent to allow follow-up requests. The session ID is saved locally,
    and if the login is successful then we will store it in Firebase
    as a valid session ID. That way, when you use it in follow-up requests,
    we will know that the requests are coming from a trusted source.
    """
    TIME_BETWEEN_REQUESTS = 0.5
    random_id = str(uuid.uuid4())
    armadillo_url = get_armadillo_url(environment)
    click.launch(
        f"{armadillo_url}/signin?sessionId={random_id}",
    )
    validating = True
    with console.status("Waiting for you to log in...") as status:
        while validating:
            time.sleep(TIME_BETWEEN_REQUESTS)
            try:
                session_response = requests.get(
                    f"{armadillo_url}/api/sessions/{random_id}"
                )
                session_response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                console.print(
                    f"There was an error while trying to validate the session: {e}",
                    style="red",
                )
                return
            session_status = session_response.json()["sessionStatus"]
            if session_status == "EXISTS":
                user = session_response.json()["user"]
                console.print(
                    f"Successfully logged in as [bold]{user['email']}[/bold]! :thumbs_up:.",
                    style="blue",
                )
                return
            elif session_status == "NOT_EXISTS":
                continue
            else:
                raise ValueError(f"Unknown session status: {session_status}")
        click.echo(f"Something went wrong. Please try again.")
    return


@click.command()
@click.argument("path", type=click.Path(), default=None)
@click.option(
    "--id",
    type=str,
    help="The ID of the model to create.",
    prompt="Model ID",
)
@click.option(
    "--name",
    type=str,
    help="The name of the model to create.",
    prompt="Model Name",
)
@click.option(
    "--delete",
    "-d",
    type=bool,
    default=False,
    flag_value=True,
    help="Delete the directory if it already exists.",
)
def init(path: Optional[str], id: str, name: str, delete: bool):
    """
    Initializes the directory structure for a new model.
    """
    remote_repo = create_github_repository(id, name, delete)
    path = os.path.join(os.getcwd(), path)
    validate_id(id)
    if os.path.exists(path):
        if delete:
            console.print(
                f":rotating_light: Deleting local directory [bold]{path}[/bold]",
                style="red",
            )
            shutil.rmtree(path)
        else:
            raise click.BadParameter("Path already exists")
    repo = Repo.clone_from(remote_repo.clone_url, path)
    render_template_directory(
        "templates/project-template/",
        path,
        {
            "model_id": id,
            "model_name": name,
            "name": "Max Davish",  # TODO Get Armadillo username for real
            "email": "davish9@gmail.com",  # TODO Get Armadillo email for real
        },
    )
    console.print(
        f":white_check_mark: Successfully created [bold]{path}[/bold]",
        style="green",
    )
    open_in_vscode = click.confirm("Open in VS Code?", abort=False)
    if open_in_vscode:
        os.system(f"code {path}")


@click.group(help="The CLI for managing your ML models.")
def cli():
    """
    Reference for the command line interface. (This is referenced in poetry.toml)
    """
    pass


cli.add_command(login)
cli.add_command(init)
