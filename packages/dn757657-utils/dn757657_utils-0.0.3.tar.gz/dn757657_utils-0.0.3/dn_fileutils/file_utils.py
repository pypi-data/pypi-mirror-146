import os


def move_all_files(source, destination):
    """ move all files from Dir to new source """
    all_files = os.listdir(source)

    for f in all_files:
        os.rename(source.joinpath(f), destination.joinpath(f))
