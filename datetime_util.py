import datetime


def get_timestamp_str() -> str:
    """Returns a str based on the current datetime.
    Example: if current datetime is 2022-04-14 17:52:08.969016
    then it will return 2022_04_14__17_52_08
    """
    curr_dt_str = str(datetime.datetime.now())
    curr_dt_str = curr_dt_str.split(".")[0] # strip the miliseconds
    curr_dt_str = curr_dt_str.replace(" ", "__")
    # replace with underscores
    for char in ['-', ':']:
        curr_dt_str = curr_dt_str.replace(char, '_')

    return curr_dt_str
