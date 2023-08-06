import os
import json
import rich_click as click
from typing import Union

APP_NAME = "ArmadilloML"


def get_armadillo_url(environment: str) -> str:
    """
    Get the armadillo url for the given environment.
    """
    if environment == "PRODUCTION":
        return "https://www.witharmadillo.com/"
    elif environment == "STAGING":
        # TODO: Make this URL work for real.
        return "https://staging.armadillo.ml"
    elif environment == "DEVELOPMENT":
        return "http://localhost:3000"
    else:
        raise ValueError(f"Unknown environment: {environment}")


def get_armadillo_config() -> dict:
    """
    Load the Armadillo Config JSON File. This is a global application file
    that stores data about the Armadillo CLI. Right now it just stores a
    Session ID and some user data and stuff like that. You can read more about
    application files here:
    https://click.palletsprojects.com/en/7.x/utils/#finding-application-folders
    """
    app_dir = click.get_app_dir(APP_NAME)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    config_file = os.path.join(app_dir, "armadillo-config.json")
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("{}")
        return {}
    else:
        with open(config_file, "r") as f:
            return json.load(f)


def get_armadillo_session() -> Union[str, None]:
    """
    Load the Armadillo Session ID, if there is one.
    """
    return get_armadillo_config().get("sessionId", None)


def validate_id(model_id: str):
    """Validates that the ID contains no spaces or special characters."""
    if not model_id:
        raise click.BadParameter("ID cannot be empty")
    if " " in model_id:
        raise click.BadParameter("ID cannot contain spaces")
    return model_id


def require_armadillo_project():
    """
    Checks that the current directory is an Armadillo project.
    """
    if not os.path.exists("armadillo.json"):
        raise click.BadParameter("Not in an Armadillo project")


def set_armadillo_value(key: str, value: str):
    """
    Saves a value to armadillo.json.
    """
    with open("armadillo.json") as f:
        data = json.load(f)
    data[key] = value
    with open("armadillo.json", "w") as f:
        json.dump(data, f, indent=4)


def get_armadillo_value(key: str):
    """
    Gets a value from armadillo.json.
    """
    with open("armadillo.json") as f:
        data = json.load(f)
    return data[key]
