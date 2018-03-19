from os import listdir
from pprint import pprint


aminoacids = {}
aa_list = []

for file in listdir('distances'):
    aminoacids_pair = file.split('.')[0]

    for i in aminoacids_pair.split('-'):
        aa_list.append(i)

aa_list = (sorted(list(set(aa_list))))

indexes = {}
for aa in aa_list:
    indexes[aa] = aa_list.index(aa)

with open('distances/final_matrix.csv', '+') as f:
    first_line = [' ']
    for aa in aa_list:
        first_line.append(aa)
    first_line.append('\n')
    f.write(','.join(first_line))

    for aa in aa_list:
        line = [aa]
        for i in range(0, len(aa_list)):
            line.append('0')
        line.append('\n')
        f.write(','.join(line))

    for file in listdir('distances'):
        aminoacids_pair = file.split('.')[0]

        with open('distances/' + file, 'r') as d:
            distance = float(d.readline())

        for line in f.readlines()[1:]:
            for aminoacid in aminoacids_pair:
                if line[0] == aminoacid:
                    line[indexes[aminoacids_pair]]