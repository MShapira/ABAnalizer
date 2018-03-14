from collections import Counter
from utility import generate_bar_chart
import numpy as np


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
        # we receive an array of tuples and need to refactor it to dict parallel with that we need to normalize the data
        positions_with_aa_count = counter.most_common(21)
        for position in positions_with_aa_count:
            sum += position[1]

        # normalize to 1
        for position in positions_with_aa_count:
            self.parts_dict[position[0]] = position[1]/sum

    # generate picture of the distribution
    def generate_aa_distribution_pict(self):
        with open('sessions/folder_name.txt', 'r') as file:
            file_lines = file.readlines()
            file.close()
        # get all aa from folder_name.txt
        aminoacids =list(file_lines[1].strip())
        # get percents
        percents = []
        for aa in aminoacids:
            try:
                percents.append(self.parts_dict[aa])
            except KeyError:
                percents.append(0.0)
                continue

        generate_bar_chart(xlabels=aminoacids, percents=percents, position=self.position, fld_name='aa_distribution')

    def __str__(self):
        return 'Position: {0}\n'.format(self.position) + \
               'Amino acid parts: {0}\n'.format(self.parts_dict) + \
               'Maximal length: {0}\n'.format(self.maxlen) + \
               '\n'


class AADistribution:
    def __init__(self):
        self.positions = {}
