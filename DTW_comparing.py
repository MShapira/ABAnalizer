from dtw import dtw
import numpy as np
from numpy.linalg import norm
import gc
import pprint


# def construct_dict(dict_name: str, final_table: dict) -> dict:
#     d = {}
#     names = []
#
#     for key in final_table.keys():
#         for aa in final_table[key]:
#             name = tuple([key, aa].sort())
#
#             if name not in names:
#                 d[name] = []
#                 d[name].append(final_table[key][aa][str(dict_name)])
#             else:
#                 d[name].append(final_table[key][aa][str(dict_name)])
#
#             names.append(name)
#
#     return d
#
#
# def print_to_file(name: str, data: dict):
#     with open(name + '.csv', 'w', newline='') as file:
#         first_line = [';']
#
#         for key in tuple(sorted(data.keys())):
#             if key[0] not in first_line:
#                 first_line.append(key[0])
#                 first_line.append(';')
#                 first_line.append('')
#         file.write(first_line)
#
#         line = []
#         for key in tuple(sorted(data.keys())):
#             if key[0] not in line:
#                 line.append('')
#                 line.append(key[0])
#                 line.append(';')
#             else:
#                 line.append(data[key])


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
    for line in lines[1:]:
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
                print('Begin with ', key, ' and ', aa)
                x = np.array([int(round(float(v), 4) * 10000) for v in rmsd[key]]).reshape(-1, 1)
                print(key, ' array is done')
                y = np.array([int(round(float(v), 4) * 10000) for v in rmsd[aa]]).reshape(-1, 1)
                print(aa, ' array is done')
                dist, cost, acc, path = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
                final_table[key][aa] = {'dist': dist/10000, 'cost': cost/10000, 'acc': acc/10000, 'path': path/10000}
                gc.collect()
                print('Distance between ', key, ' and ', aa, ' is: ', dist / 10000)
                print('-' * 50)

    pp.pprint(final_table)

    # dist = construct_dict('dist', final_table)
    # cost = construct_dict('cost', final_table)
    # acc = construct_dict('acc', final_table)
    # path = construct_dict('path', final_table)







