import gc
import json
from multiprocessing import Process
from os import makedirs
from os.path import exists
import time
from dtw import dtw
import numpy as np
from numpy.linalg import norm


def construct_global_data(file_name: str) -> list:
    # load raw data lines
    file = open(file_name)
    lines = file.readlines()
    file.close()

    # read AA names
    header = lines[0].strip()
    aa_names = header.split('\t')

    # construct dictionary skeleton
    rmsd = dict()
    for aa_name in aa_names:
        rmsd[aa_name] = []

    # load data
    lines = lines[1:]  # skip header
    for line in lines:
        components = line.strip().split('\t')

        # iterate among columns collecting data
        for aa_index in range(0, len(aa_names)):
            aa_name = aa_names[aa_index]
            rmsd[aa_name].append(components[aa_index])

    # construct global list of data for workers
    data = []
    for first_aa_index in range(0, len(aa_names)):
        first_aa_name = aa_names[first_aa_index]

        for second_aa_index in range(first_aa_index + 1, len(aa_names)):
            second_aa_name = aa_names[second_aa_index]

            # construct parenthesis dictionary
            pare = dict()
            pare['first AA'] = first_aa_name
            pare['second AA'] = second_aa_name
            pare['first RMSD'] = rmsd[first_aa_name]
            pare['second RMSD'] = rmsd[second_aa_name]

            # store it
            data.append(pare)

    return data


def worker(data_list_string: str, result_folder_name: str):
    start_time = time.time()

    # load data from JSON string
    data_list = json.loads(data_list_string)
    first_aa_name = data_list[0]['first AA']
    second_aa_name = data_list[0]['second AA']
    first_rmsd = data_list[0]['first RMSD']
    second_rmsd = data_list[0]['second RMSD']

    prefix = 'worker {0}-{1}: '.format(first_aa_name, second_aa_name)
    print(prefix + 'start')

    # prepare data for DTW
    # first AA
    first_list = [int(round(float(v), 4) * 10000) for v in first_rmsd]
    first_array = np.array(first_list).reshape(-1, 1)
    print(prefix + '{0} array is done'.format(first_aa_name))
    # second AA
    second_list = [int(round(float(v), 4) * 10000) for v in second_rmsd]
    second_array = np.array(second_list).reshape(-1, 1)
    print(prefix + '{0} array is done'.format(second_aa_name))

    # start DTW
    distance = dtw(first_array, second_array, dist=lambda x, y: norm(x - y, ord=1))[0]
    gc.collect()

    # dump results
    file_name = result_folder_name + '/{0}-{1}.distance.txt'.format(first_aa_name, second_aa_name)
    file = open(file_name, 'w')
    file.write(str(distance / 10000))
    file.close()
    print(prefix + 'result saved to {0}'.format(file_name))

    # any other data?
    worker_process = None
    if len(data_list) > 1:
        # remove first element and dump the rest to JSON
        data_list = data_list[1:]
        data_list_string = json.dumps(data_list, indent=4)

        # start new worker
        worker_process = Process(target=worker, args=(data_list_string, result_folder_name))
        worker_process.start()
        print(prefix + 'next worker started')

    # show work time
    end_time = time.time()
    print(prefix + 'finished ({0:.3f} seconds)'.format(end_time - start_time))

    # join worker process if it was created
    if worker_process is not None:
        worker_process.join()


if __name__ == '__main__':
    start_time = time.time()

    # prepare result folder
    result_folder_name = 'distances'
    if not exists(result_folder_name):
        makedirs(result_folder_name)

    # global prepare global data list for workers
    global_data = construct_global_data('real_rmsd.txt')
    print('global data constructed')

    # split data
    worker_count = 4
    worker_data = []
    for i in range(0, worker_count):
        worker_data.append(list())
    worker_index = 0
    for pare in global_data:
        worker_data[worker_index].append(pare)
        worker_index = (worker_index + 1) % worker_count
    print('data splitted for {0} workers'.format(worker_count))

    # run workers
    workers = []
    for data_list in worker_data:
        data_list_string = json.dumps(data_list, indent=4)
        worker_process = Process(target=worker, args=(data_list_string, result_folder_name))
        worker_process.start()
        workers.append(worker_process)
    print('all workers started')

    # wait for workers
    for worker_process in workers:
        worker_process.join()

    # show work time
    end_time = time.time()
    print('success ({0:.3f} seconds)'.format(end_time - start_time))
