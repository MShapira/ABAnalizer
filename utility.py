from sys import stdout
from datetime import datetime
from os import makedirs, path
from pandas import read_csv


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
        file.write(session_folder_name)
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


