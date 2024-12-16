def functools_test():
    from functools import reduce

    reduce_list = [1, 2, 3, 4, 5]

    reduced = reduce(lambda x, y: x + y, reduce_list)

    print(reduced)

def country_len():

    countries = [ "GER", "FR", "BRZ", "CZ", "SWE"]
    indexes = range(len(countries))

    zipped = zip(indexes, countries)

    print(list(zipped))

def filter_names():
    from functools import reduce

    names = ["Torsten", "Tobias", "Tamian", "Gabriel", "Lisa", "Luisa", "Tim"]

    filtered = list(filter(lambda x: not x.startswith("T"), names))

    reduced = reduce(lambda x, y: f"{x} {y}", filtered)

    print(reduced)


if __name__ == "__main__":

    functools_test()
    
    country_len()
    
    filter_names()
