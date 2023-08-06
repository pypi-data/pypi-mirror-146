# import os
import json
import pandas as pd


def txt2list(filename, enter=False, mode="r"):
    """
    filename: str
    enter: keep right "\n", False, bool
    mode: "r"
    """
    fopen = open(filename, mode)
    lines = fopen.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip('\n') 
    fopen.close()
    return lines


def table2list(filename, column, sep="\t", **kwargs):
    """
    filename: txt filename, str
    column: key of the column, str
    sep: delimiter to use, "," for .csv only , "\t"
    others: ...
    """
    data = pd.read_table(filename, sep, **kwargs)[column]
    out = []
    for i in range(len(data)):
        out.append(json.loads(data[i]))
    return out
