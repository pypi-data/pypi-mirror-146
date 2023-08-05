import re

# time units on seconds 
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24
week = day * 7
mounth = week * 4
year = mounth * 12

def ms(query: str) -> int:
    """Convert a query to seconds"""

    temp = re.findall(
        pattern=r"^(-?(?:\d+)?.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|month?|mon|years?|yrs?|y)?$", 
        string=query, 
        flags=re.I
    )
    if temp == []:
        return None
    
    number = int(temp[0][0])

    if number <= 0:
        return 0

    elif temp[0][1] in ("m", "min", "minute"):
        return number * minute

    elif temp[0][1] in ("h", "ho", "hour"):
        return number * hour
    
    elif temp[0][1] in ("d", "day"):
        return number * day

    elif temp[0][1] in ("w", "week"):
        return number * week

    elif temp[0][1] in ("mon", "month"):
        return number * mounth

    elif temp[0][1] in ("y", "year"):
        return number * year

    else:
        raise Exception(
            r"The entered time unit was not found."
        )


def check(query: str) -> bool:
    """Check a writed query"""

    temp = re.findall(
        pattern=r"^(-?(?:\d+)?.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|month?|mon|years?|yrs?|y)?$",
        string=query,
        flags=re.I
    )

    if temp == []:
        return False

    number = int(temp[0][0])
    
    units = [
        "m", "min", "minute",
        "h", "ho", "hour",
        "d", "day",
        "w", "week",
        "mon", "month",
        "y", "year"
    ]

    if temp[0][1] not in units:
        return False

    elif number < 0:
        return False
    
    else:
        return True