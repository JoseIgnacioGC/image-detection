from src.utils import ROOT_DIR

from typing import Any
from dataclasses import dataclass
import yaml

__FILE_NAME = "credentials.yml"


@dataclass
class Credentials:
    email_server_email: str
    email_server_password: str


def __get_credentials() -> Credentials:
    credentials_path = ROOT_DIR / __FILE_NAME
    if not credentials_path.exists():
        raise FileNotFoundError(
            f"{credentials_path}: file not found\n you should create a {__FILE_NAME}"
        )

    credentials = Credentials.__annotations__
    credentials_keys = tuple(credentials.keys())
    with open(credentials_path, "r") as f:
        config: dict[Any, Any] = yaml.safe_load(f)

    if len(config) != len(credentials_keys):
        raise ValueError(
            f"Error in {__FILE_NAME}: the file should only have {credentials_keys} keys"
        )

    for key, value in config.items():
        if key not in credentials_keys:
            raise ValueError(f"Error in {__FILE_NAME}: {key} is not a valid")
        if not isinstance(value, credentials[key]):
            raise ValueError(
                f"Error in {__FILE_NAME}: {key} should be of type {credentials[key]}"
            )

    return Credentials(**config)


credentials = __get_credentials()
