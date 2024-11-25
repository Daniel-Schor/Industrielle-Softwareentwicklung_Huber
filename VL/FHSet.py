class FHSet(set):
    def __init__(self, *args):
        super().__init__(*args)

    def __add__(self, other):
        return FHSet(self.union(other))

new_set = FHSet({1, 2, 3})

print(new_set)  

new_set = new_set + {3, 4, 9}

print(new_set)
