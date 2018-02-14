from collections import Counter
import matplotlib.pyplot as plt


class PositionDistribution:
    def __init__(self, position: str, aa_array: list, maxlen: int):
        self.position = position
        self.aa_array = aa_array
        self.parts_dict = {}
        self.maxlen = maxlen

    # count the number of aminoacids in the array
    def aa_part_counter(self):
        sum = 0

        counter = Counter(self.aa_array)
        # we recieve an array of tuples and need to refactor it to dict parallel with that we need to normalize the data
        positions_with_aa_count = counter.most_common(21)
        for position in positions_with_aa_count:
            sum += position[1]

        for position in positions_with_aa_count:
            self.parts_dict[position[0]] = position[1]/sum

    # generate picture of the distribution
    def generate_pict(self):
        fig = plt

class AADistribution:
    def __init__(self):
        self.positions = {}
