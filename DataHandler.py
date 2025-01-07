#!/usr/bin/env python

""" Data Handler Class

Defines a simple data file handler that can store data and output it cleanly.

"""

import os, os.path

class DataHandler:
    def __init__(self, filename, output_type="csv"):
        self.filename = filename
        self.data = {}
        if output_type == "csv":
            self.sep = ','
        else:
            raise ValueError("data file output type not recognized")

    def AddData(self, name, value):
        self.data[name] = str(value)

    def InitializeDataDirectory(self):
        # check if the data directory exists, and if not create it
        dirname = os.path.dirname(self.filename)
        if os.path.exists(dirname) and os.path.isdir(dirname):
            return
        elif os.path.exists(dirname) and not os.path.isdir(dirname):
            s = "data directory '%s' is an existing file" % dirname
            raise NotADirectoryError(s)
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
            for k, v in self.data.items():
                header.append(k)
            if len(header) > 0:
                with open(self.filename, 'w') as f:
                    f.write(self.sep.join(header) + '\n')

    def OutputLine(self):
        self.InitializeDataDirectory()
        self.InitializeDataFile()
        line = list()
        for k, v in self.data.items():
            line.append(v)
        if len(line) > 0:
            with open(self.filename, 'a') as f:
                f.write(self.sep.join(line) + '\n')

import time

if __name__=="__main__":
    datafile = DataHandler("testdata/test.csv", 'csv')
    datafile.AddData("name", "TestData")
    datafile.AddData("runtime", time.strftime("%Y%m%d-%H%M%S"))
    for b in ['prac', 'exp']:
        datafile.AddData('blocktype', b)
        for t in range(4):
            datafile.AddData("trial", t + 1)
            datafile.AddData("rt", .56939567238954560934572)
            datafile.OutputLine()
