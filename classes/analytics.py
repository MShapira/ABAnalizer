from collections import Counter
from utility import generate_bar_chart


class PositionDistribution:
    def __init__(self, position: str, aa_array: list, maxlen: int):
        self.position = position
        self.aa_array = aa_array
        self.parts_dict = {}
        self.maxlen = maxlen

    # count the number of amino acids in the array
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
    def __init__(self, antibodies: list):
        self.antibodies = antibodies
        self.frameworks = {
            'fr_1': [],
            'fr_2': [],
            'fr_3': [],
            'fr_4': []
        }
        self.cdrs = {
            'cdr_1': [],
            'cdr_2': [],
            'cdr_3': []
        }
        self.positions = {}

    # get longest CDRs and Frameworks numbers via dictionary numbering
    def get_longest_cdrs_and_frameworks(self):
        # find the longest framework and cdr in each position
        # for frameworks
        for antibody in self.antibodies:
            for key in self.frameworks:
                if len(self.frameworks[key]) < len(antibody.protein_sequence.frameworks[key]):
                    self.frameworks[key] = antibody.protein_sequence.frameworks[key]

            # for cdrs
            for key in self.cdrs:
                if len(self.cdrs[key]) < len(antibody.protein_sequence.CDRs[key]):
                    self.cdrs[key] = antibody.protein_sequence.CDRs[key]