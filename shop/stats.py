"""Order statistics used by the shop's reports."""


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean() of an empty list")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("median() of an empty list")
    s = sorted(values)
    mid = len(s) // 2
    if len(s) % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2
