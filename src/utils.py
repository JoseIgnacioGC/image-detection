from datetime import datetime, timedelta
from pathlib import Path


def set_timer_in_seconds(seconds: int):
    def x_seconds_has_passed(given_date: datetime) -> bool:
        return datetime.now() - given_date > timedelta(seconds=seconds)

    return x_seconds_has_passed


ROOT_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = ROOT_DIR / "resources"
