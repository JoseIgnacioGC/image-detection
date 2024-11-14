from src.utils import ROOT_DIR

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

    with open(credentials_path, "r") as f:
        config = yaml.safe_load(f)

    for key in Credentials.__annotations__:
        value = config.get(key)
        if isinstance(value, bool):
            continue
        if not value:
            raise KeyError(f"{key} not found in the {__FILE_NAME} file or is empty")

    return Credentials(**config)

credentials = __get_credentials()
