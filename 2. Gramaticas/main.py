import sys

from file.fileManager import FileManager
from gramatic.gramatic import Gramatic

def main():
    argv = len(sys.argv)
    fileRoute = str(sys.argv[-1])

    if argv != 2:
        print('You have to add only one argument.')
    else:
        print('File route:', fileRoute)
        fileManager = FileManager(fileRoute)

        gramatic = Gramatic(fileManager.fileData())

        print('Gramatic type:', gramatic.gramaticType())
