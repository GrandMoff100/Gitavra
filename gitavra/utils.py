import git
import os


def recursively_find_files(directory: str):
    for path in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, path)):
            yield from recursively_find_files(os.path.join(directory, path))
        else:
            yield os.path.join(directory, path)


def reshape_2d_array(array: list):
    return [[x[i] for x in array] for i in range(len(array[0]))]
