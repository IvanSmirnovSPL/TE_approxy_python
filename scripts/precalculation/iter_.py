import itertools


def generate_variants(points, num):
    rez = list(itertools.combinations(points, num))
    return rez

