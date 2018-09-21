#!/usr/bin/python3.6
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Plot the OCR quality of documents in 2D canvas.')
parser.add_argument('-l', help='Label to show next to each marker', dest='labels', choices=['id', 'wl'])
parser.add_argument('-x', help='Variable for X-axis', dest='xaxis', choices=['samohlasky', 'avgwl', 'topn', 'skdist'], default='samohlasky')
parser.add_argument('-y', help='Variable for Y-axis', dest='yaxis', choices=['samohlasky', 'avgwl', 'topn', 'skdist'], default='skdist')
parser.add_argument('-n', help='Number of top character to use for topn metric', dest='topnchars', type=int, default=5)
args = parser.parse_args()
# todo zoom

def awgwls_colors():
  return [(1 if a>12 else a/12, a/8 if a<8 else 1 if a < 12 else (18-a)/6 if a<18 else 0, (8-a)/8 if a<8 else 0) for a in avgwls]

def sk_dist(row):
    return sum([d(char,row[char] + (row.to_dict()[char.upper()] if char.upper()!=char else 0)) for char in row.to_dict() if char.lower()==char])

# char is lowercase
def d(char, freq):
    sk_freq = {'o': 0.095, 'a': 0.090, 'ä': 0.001, 'e': 0.078, 'i': 0.061, 'v': 0.051, 'r': 0.050, 's': 0.047, 't': 0.045, 'k': 0.038, 'n': 0.038, 'p': 0.033, 'm': 0.032,
    'l': 0.037, 'u': 0.026, 'í': 0.012, 'ň': 0.002, 'd': 0.032,'á': 0.019, 'ľ': 0.004, 'z': 0.020, 'b': 0.017, 'c': 0.014, 'ť': 0.005, 'x': 0.001, 'h': 0.012,
    'č': 0.011, 'f': 0.003, 'j': 0.019, 'š': 0.009, 'ú': 0.009, 'ď': 0.001, 'é': 0.008, 'ž': 0.008, 'g': 0.003, 'ó': 0.001, 'y': 0.015, 'ý': 0.011, 'ô': 0.002, 'ŕ': 0.000,
    'w': 0.000, 'q': 0.000, 'ř': 0.000, 'ĺ': 0.000}.get(char, -1)
    if sk_freq == -1:
        print(char, sk_freq)
    return abs(freq - sk_freq)

def label(i):
    if args.labels == 'id':
        return str(i+1)
    else:
        if args.labels == 'wl':
            return str(avgwls[i])

def calculate_topn(n):
    print("Calculating top " + str(n))
    return [row[np.argsort(row)[-n:]].values.sum() for i,row in train.iterrows()]

def calculate_samohlasky():
    print("Calculating samohlasky")
    return [row[list('AEIOUYÁÉÍÓÚÝaeiouyáäéíóôúý')].values.sum() for i,row in train.iterrows()]

def calculate_skdist():
    print("Calculating skdist")
    return [sk_dist(row) for i,row in train.iterrows()]

def series(series_name):
    if series_name == 'samohlasky':
        return calculate_samohlasky()
    elif series_name == 'avgwl':
        return avgwls
    elif series_name == 'topn':
        return calculate_topn(args.topnchars)
    elif series_name == 'skdist':
        return calculate_skdist()
    else:
        return []    

def xseries():
    return series(args.xaxis)

def yseries():
    return series(args.yaxis)

def plot_scatter():
    plt.clf()
    plt.scatter(xseries(), yseries(), s=0.5, c=awgwls_colors())
    plt.xlabel(args.xaxis)
    plt.ylabel(args.yaxis)
    plt.title('OCR quality')
    if args.labels:
        for i in range(len(samohlasky)):
            plt.text(samohlasky[i], skdists[i], label(i))
    plt.savefig('scatter.png', figsize=(6,4), dpi=300)
    plt.show()

print(args)
print("Reading avgwls")
avgwls = [float(line) for line in open("current_avgwls").read().split('\n') if line]
print("Reading freqs")
train=pd.read_csv("current_freqs", dtype=np.float)

plot_scatter()
