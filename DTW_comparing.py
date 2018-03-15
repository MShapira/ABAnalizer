from dtw import dtw
import numpy as np
import time
from numpy.linalg import norm
import gc
from os import makedirs, path
import multiprocessing as m
import json
import threading


class WorkerThread(m.Process):
    def __init__(self, queue, size):
        m.Process.__init__(self)
        self.queue = queue
        self.size = size

    def run(self):
        self.queue.put(range(self.size))


start_time = time.time()


# run one dtw calculation
def dtw_pare_comparing(pare):
    if not path.exists('results'):
        makedirs('results')

    data = json.loads(pare)

    with open('results/' + data['key']['name'] + '-' + data['aa']['name'], 'w') as file:
        print('Begin with ' + data['key']['name'] + ' and ' + data['aa']['name'])
        x = np.array([int(round(float(v), 4) * 10000) for v in data['key']['value']]).reshape(-1, 1)
        print(data['key']['name'] + ' array is done')
        y = np.array([int(round(float(v), 4) * 10000) for v in data['aa']['value']]).reshape(-1, 1)
        print(data['aa  ']['name'] + ' array is done')
        dist = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))[0]
        gc.collect()

        file.write(str(dist/10000))
        file.close()

        print('Data was wroten down for ' + data['key']['name'] + '-' + data['aa']['name'])
        print('-' * 50)


with open('real_rmsd.txt', 'r') as file:
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
    queue = m.Queue()

    for key in rmsd.keys():
        final_table[key] = {}
        for aa in rmsd.keys():
            if aa not in final_table[key].keys() and aa not in final_table.keys():
                pare = {"key": {"name": key, "value": rmsd[key]}, "aa": {"name": aa, "value": rmsd[aa]}}
                pare = json.dumps(pare, sort_keys=True, indent=4)

                queue.put(m.Process(target=dtw_pare_comparing, args=(pare, )))

    worker_p = WorkerThread(queue, 30)
    worker_p.start()
    worker_p.join()

    print("--- %s seconds ---" % (time.time() - start_time))







