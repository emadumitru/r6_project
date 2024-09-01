import os

def get_relative_path(target_file, directory='data', curent_file=__file__):
    curent_dir = os.path.dirname(curent_file)
    one_dir_up = os.path.join(curent_dir, os.pardir)
    data_dir = os.path.join(one_dir_up, directory)
    path = os.path.join(data_dir, target_file)
    return path