#!/usr/bin/env python

""" Data Handler Class

The idea is to create a hierarchical data file handler that can store data
at different levels, e.g., experiment, block, and trial. You can add data
at different levels, reset at each iteration (clearing out that level and
all lower levels), and output a line when requested.
"""

import os, os.path

class DataHandler:
    def __init__(self, filename, levels, output_type="csv"):
        self.levels = levels
        self.filename = filename
        self.data = {}
        for level in self.levels:
            self.data[level] = {}
        if output_type == "csv":
            self.sep = ','
        else:
            raise ValueError("data file output type not recognized")

    def AddData(self, level, name, value):
        self.data[level][name] = str(value)

    def InitializeDataDirectory(self):
        # check if the data directory exists, and if not create it
        dirname = os.path.dirname(self.filename)
        if os.path.exists(dirname) and os.path.isdir(dirname):
            return
        elif os.path.exists(dirname) and not os.path.isdir(dirname):
            raise NotADirectoryError("data directory is an existing file")
        else:
            os.makedirs(dirname)
            return

    def InitializeDataFile(self):
        # check if the data file exists, and if not create it with its header
        if os.path.exists(self.filename) and os.path.isfile(self.filename):
            return
        elif os.path.exists(self.filename) and not os.path.isfile(self.filename):
            raise
        else:
            header = list()
            for level in self.data:
                for k, v in self.data[level].items():
                    header.append(k)
            if len(header) > 0:
                with open(self.filename, 'w') as f:
                    f.write(self.sep.join(header) + '\n')

    def OutputLine(self):
        self.InitializeDataDirectory()
        self.InitializeDataFile()
        line = list()
        for level in self.data:
            for k, v in self.data[level].items():
                line.append(v)
        if len(line) > 0:
            with open(self.filename, 'a') as f:
                f.write(self.sep.join(line) + '\n')

import time

if __name__=="__main__":
    datafile = DataHandler("testdata/test.csv", ["exp", "block", "trial"], 'csv')
    datafile.AddData("exp", "name", "TestData")
    datafile.AddData("exp", "runtime", time.strftime("%Y%m%d-%H%M%S"))
    for b in ['prac', 'exp']:
        datafile.AddData('block', 'blocktype', b)
        for t in range(4):
            datafile.AddData("trial", "trial", t + 1)
            datafile.OutputLine()
