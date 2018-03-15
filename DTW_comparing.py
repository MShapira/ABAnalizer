from dtw import dtw
import numpy as np
from numpy.linalg import norm
import gc
import pprint
from os import makedirs, path


def construct_dict(final_table: dict) -> dict:
    d = {}
    names = []

    for key in final_table.keys():
        for aa in final_table[key]:
            name = tuple(sorted([key, aa]))

            if name not in names:
                d[name] = []
                d[name].append(final_table[key][aa])
            else:
                d[name].append(final_table[key][aa])

            names.append(name)

    return d


# run one dtw calculation
def dtw_pare_comparing(pare: dict):
    if not path.exists('results/'):
        makedirs('results/')

    with open('results/' + pare['key']['name'] + '-' + pare['aa']['name'], 'w') as file:
        print('Begin with ', pare['key']['name'], ' and ', pare['aa']['name'])
        x = np.array([int(round(float(v), 4) * 10000) for v in pare['key']['value']]).reshape(-1, 1)
        print(pare['key']['name'], ' array is done')
        y = np.array([int(round(float(v), 4) * 10000) for v in pare['aa']['value']]).reshape(-1, 1)
        print(pare['aa']['name'],' array is done')
        dist = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))[0]
        gc.collect()
        print('Distance between ', pare['key']['name'], ' and ', pare['aa']['name'], ' is: ', dist / 10000)
        print('-' * 50)

        file.write(str(dist/10000))
        file.close()


with open('real_rmsd.txt', 'r') as file:
    pp = pprint.PrettyPrinter(indent=4)
    lines = file.readlines()
    rmsd = {}

    # construct the dictionary
    names = lines[0].strip().split('\t')
    for name in names:
        rmsd[name] = []

    # fill the dictionary
    # todo: refactor for more universal using
    for line in lines[1:20]:
        rmsd['Ala'].append(line.strip().split('\t')[0])
        rmsd['Arg'].append(line.strip().split('\t')[1])
        rmsd['Asn'].append(line.strip().split('\t')[2])
        rmsd['Asp'].append(line.strip().split('\t')[3])
        rmsd['Cys'].append(line.strip().split('\t')[4])
        rmsd['Gln'].append(line.strip().split('\t')[5])
        rmsd['Glu'].append(line.strip().split('\t')[6])
        rmsd['Gly'].append(line.strip().split('\t')[7])
        rmsd['His'].append(line.strip().split('\t')[8])
        rmsd['Ile'].append(line.strip().split('\t')[9])
        rmsd['Leu'].append(line.strip().split('\t')[10])
        rmsd['Lys'].append(line.strip().split('\t')[11])
        rmsd['Met'].append(line.strip().split('\t')[12])
        rmsd['Phe'].append(line.strip().split('\t')[13])
        rmsd['Pro'].append(line.strip().split('\t')[14])
        rmsd['Ser'].append(line.strip().split('\t')[15])
        rmsd['Thr'].append(line.strip().split('\t')[16])
        rmsd['Trp'].append(line.strip().split('\t')[17])
        rmsd['Tyr'].append(line.strip().split('\t')[18])
        rmsd['Val'].append(line.strip().split('\t')[19])

    # calculate and collect the data using dtw lib
    final_table = {}
    for key in rmsd.keys():
        final_table[key] = {}
        for aa in rmsd.keys():
            if aa not in final_table[key].keys() and aa not in final_table.keys():
                pare = {'key': {'name': key, 'value': rmsd[key]}, 'aa': {'name': aa, 'value': rmsd[aa]}}
                dtw_pare_comparing(pare)







