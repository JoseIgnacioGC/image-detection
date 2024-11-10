from dataclasses import dataclass
from pathlib import Path
import yaml

__FILE_NAME = "credentials.yml"


@dataclass
class Credentials:
    email_server_email: str
    email_server_password: str


def get_credentials() -> Credentials:
    config_path = Path(".") / __FILE_NAME
    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path}: file not found\n you should create a credentials.yml"
        )

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    for key in Credentials.__annotations__:
        value = config.get(key)
        if isinstance(value, bool):
            continue
        if not value:
            raise KeyError(f"{key} not found in the {__FILE_NAME} file or is empty")

    return Credentials(**config)
