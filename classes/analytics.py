from collections import Counter


class PositionDistribution:
    def __init__(self, position: str, aa_array: list):
        self.position = position
        self.aa_array = aa_array
        self.parts_dict = {}

    # count the number of aminoacids in the array
    def aa_part_counter(self):
        counter = Counter(self.aa_array)
        self.parts_dict = counter.most_common(21)
        print(self.position)
        print(self.parts_dict)
        print('-' * 20)

    # define the destribution and find the outlayers
    #def calculate_distribution(self):


class AADistribution:
    def __init__(self):
        self.positions = {}
