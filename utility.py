from sys import stdout
from datetime import datetime
from os import makedirs, path


# smart progress bar
def show_progress(label: str, percentage: float, width: int = 40):
    progress = '['
    for i in range(0, width):
        if i / width < percentage:
            progress += '#'
        else:
            progress += ' '
    progress += '] {0:.1%}'.format(percentage)
    print('\r' + label + progress, end='')
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
