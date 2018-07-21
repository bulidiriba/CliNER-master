import os
import sys
import glob
import argparse
import itertools
import pickle

def main():
    function()


def function():

    txt = []
    line = input('First line: ')
    while line:
        txt.append(line)
        line = input()

    filepath = "F:/Programming Documnets/AI/Telehealth/CliNER-master/data/examples/ex_1.txt"
    file = open(filepath, 'w')
    for i in txt:
        file.write(i+"\n")
    file.close()


if __name__ == '__main__':
    main()

