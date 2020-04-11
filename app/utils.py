import datetime


def parse_date(date: str) -> datetime.date:
    """
    Parse string in the form dd/mm/yyyy into a datetime.
    """
    return datetime.date(*map(int, date.split("/")[::-1]))
