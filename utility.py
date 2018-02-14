from sys import stdout
import statistics


# smart progress bar
def show_progress(label, width, percentage):
    progress = '['
    for i in range(0, width):
        if i / width < percentage:
            progress += '#'
        else:
            progress += ' '
    progress += '] {0:.1%}'.format(percentage)
    print('\r' + label + progress, end='')
    stdout.flush()
