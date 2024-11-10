from datetime import datetime, timedelta


def set_timer_in_seconds(seconds: int):
    def x_seconds_has_passed(given_date: datetime) -> bool:
        return datetime.now() - given_date > timedelta(seconds=seconds)

    return x_seconds_has_passed
