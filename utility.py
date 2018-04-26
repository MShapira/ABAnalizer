from classes.sequence import ProteinSequence
from classes.antiboby import Antibody
from sys import stdout
from datetime import datetime
from os import makedirs, path
import matplotlib.pyplot as plt
from pandas import read_csv
from matplotlib.ticker import FuncFormatter
import numpy as np


# parsing of data file with sequences
def sequences_parser(filename: str)->list:

    antibodies = []
    dictionaries = []
    str = ''

    with open(filename) as file:
        lines = file.readlines()

        # smart bar for getting the time remaining
        progress_label = 'Parsing the input data'
        show_progress(progress_label, 0.0)
        index = 0

        for line in lines:

            # for appropriate work of smart bar
            index += 1
            show_progress(progress_label, float(index) / float(len(lines)))

            line = line.rstrip()
            # the way to find new seq and initiate new object
            if line[0] == '>':

                # add the sequence to its antibody object as to a previous object in antibodies list
                if len(antibodies) != 0 and str != '':
                    protein_sequence = ProteinSequence(seq=str)
                    # construct the sequence dictionary for each Sequence object
                    protein_sequence.construct_seq_dict()
                    # if there is no such dictionary (from Sequence object) in dictionaries list add it to the list and
                    # add this Sequence object to the Antibody object in the final list
                    if protein_sequence.seq_dict not in dictionaries:
                        dictionaries.append(protein_sequence.seq_dict)
                        antibodies[-1].protein_sequence = protein_sequence
                    # if there is such dictionary - remove the Antibody object from the final list
                    else:
                        antibodies.remove(antibodies[-1])
                    str=''

                # generate hot points in class initiating
                laa = line.split('|')
                name = laa[0][1:]
                host = laa[2]
                res = laa[3]
                # initiate an object of class Antibody
                # todo: write a filter to rid out of the sequence duplicates
                antibody = Antibody(name=name, host=host, resource_of_origin=res)

                # define what kind of seq do we have
                if laa[5] == 'protein':
                    antibody.protein_sequence = True
                    antibody.nucleotide_sequence = False
                elif laa[5] == 'nucleotide':
                    antibody.protein_sequence = False
                    antibody.nucleotide_sequence = True
                antibodies.append(antibody)

            else:
                str += line
                # to fill the last line
                if line == lines[-1].rstrip():
                    protein_sequence = ProteinSequence(seq=str)
                    protein_sequence.construct_seq_dict()
                    if protein_sequence.seq_dict not in dictionaries:
                        dictionaries.append(protein_sequence.seq_dict)
                        antibodies[-1].protein_sequence = protein_sequence
                    else:
                        antibodies.remove(antibodies[-1])
                    str=''

    return antibodies


# smart progress bar
def show_progress(label: str, percentage: float, width: int = 50):
    progress = '['
    for i in range(0, width):
        if i / width < percentage:
            progress += '#'
        else:
            progress += ' '
    progress += '] {0:.1%}'.format(percentage)
    print('\r' + label + progress + '\n', end='')
    stdout.flush()


# create session folder to divide the program firing
def create_session_folder() -> str:

    # create a folder with the date and the time as a name
    session_root_folder = 'sessions'
    time = datetime.now()
    session_name = '{0}-{1}-{2}_{3}-{4}-{5}'.format(time.year, time.month, time.day, time.hour, time.minute, time.second)
    session_folder_name = path.join(session_root_folder, session_name)
    makedirs(session_folder_name)

    # это ебаный костыль, но я не придумал, как это изменить -
    # мне нужно место, куда я могу обращаться и брать имя сессии
    # с любой точки скрипта
    with open(session_root_folder + '/folder_name.txt', 'w') as file:
        file.write(session_folder_name + '\n')
        file.close()

    return session_folder_name


# print data to log file instead of terminal output
def print_to_log(string: str):
    with open('sessions/folder_name.txt', 'r') as file:
        file_name = file.readline().rstrip() + '/session.log'
        file.close()

    with open (file_name, 'a') as log:
        log.write(string + '\n')
        log.close()


# read data from csv file
def read_from_csv(csv_file_name: str, ref_column: str)-> dict:
    # generate dictionary with column names as a keys
    primary_dict = read_csv(csv_file_name, header=0).to_dict()

    # refactor primary dictionary to 20 dicts
    lines_names = {}
    for index in primary_dict[ref_column]:
        name = primary_dict[ref_column][index]
        lines_names[name] = {}
        for key in primary_dict.keys():
            if key != ref_column:
                lines_names[name][key] = primary_dict.get(key)[index]

    return lines_names


# building the bar graph
def generate_bar_chart(xlabels: list, percents: list, position: str, fld_name: str, x_coordinate = 20):

    # generate labels on Y axis
    def generate_y_axis_labels(x_coordinate, pos):
        return '{0:2.2f}%'.format(x_coordinate * 100)

    formatter = FuncFormatter(generate_y_axis_labels)

    # build the plot
    fig, ax = plt.subplots()
    ax.set_title('Aminoacids')
    ax.yaxis.set_major_formatter(formatter)
    plt.bar(np.arange(1, x_coordinate + 1), percents)
    plt.xticks(np.arange(1, x_coordinate + 1), xlabels)

    file_name = '{0}.png'.format(position)
    with open('sessions/folder_name.txt', 'r') as file:
        folder_name = file.readline().rstrip() + '/pictures/' + fld_name + '/'
        if not path.exists(folder_name):
            makedirs(folder_name)
        file.close()
        # saving the file to the folder inside the session
        plt.savefig(folder_name + file_name)
        plt.close()


# build the linear graph
def generate_linear_chart(x: list, y: list, xlabel: str, ylabel: str, fld_name: str):
    plt.figure(num=None, figsize=(30, 20), dpi=100)
    plt.plot(np.arange(1, len(x)+1), y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(np.arange(1, len(x)+1), x, rotation='vertical')

    file_name = '{0}.png'.format(ylabel)
    with open('sessions/folder_name.txt', 'r') as file:
        folder_name = file.readline().rstrip() + '/pictures/' + fld_name + '/'
        if not path.exists(folder_name):
            makedirs(folder_name)
        file.close()
        # saving the file to the folder inside the session
        plt.savefig(folder_name + file_name)
        plt.close()