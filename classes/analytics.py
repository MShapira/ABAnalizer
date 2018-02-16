from collections import Counter
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
from os import makedirs, path


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

        # normalize to 1
        for position in positions_with_aa_count:
            self.parts_dict[position[0]] = position[1]/sum

    # generate picture of the distribution
    def generate_pict(self):
        x_coordinate = np.arange(len(self.parts_dict))

        aminoacids = []
        percents = []
        for key in self.parts_dict.keys():
            aminoacids.append(key)
            percents.append(self.parts_dict[key])

        # generate labels on Y axis
        def generate_y_axis_labels(x_coordinate, pos):
            return '{0:2.2f}%'.format(x_coordinate*100)

        formatter = FuncFormatter(generate_y_axis_labels)

        # building the graph
        fig, ax = plt.subplots()
        ax.set_title('Aminoacids')
        ax.yaxis.set_major_formatter(formatter)
        plt.bar(x_coordinate, percents)
        plt.xticks(x_coordinate, aminoacids)

        file_name = '{0}.png'.format(self.position)
        with open('sessions/folder_name.txt', 'r') as file:
            folder_name = file.readline().rstrip() + '/pictures/aa_distribution/'
            if not path.exists(folder_name):
                makedirs(folder_name)
            file.close()
            # saving the file to the folder inside the session
            plt.savefig(folder_name + file_name)
            plt.close()


class AADistribution:
    def __init__(self):
        self.positions = {}
