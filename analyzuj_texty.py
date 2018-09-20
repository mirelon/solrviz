#!/usr/bin/python3.6
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_top(n):
    print("Calculating top " + str(n))
    topn = [row[np.argsort(row)[-n:]].values.sum() for i,row in train.iterrows()]
    print("Plotting top " + str(n))
    plt.clf()
    plt.scatter(avgwls, topn, s=0.5)
    plt.xlabel('Average word length')
    plt.ylabel('Top ' + str(n) + ' characters')
    plt.title('OCR quality')
    plt.savefig('top' + str(n) + '.png')

    plt.clf()
    plt.scatter(avgwls[:100], topn[:100], s=0.5)
    plt.xlabel('Average word length')
    plt.ylabel('Top ' + str(n) + ' characters')
    plt.title('OCR quality')
    
    for i in range(100):
        plt.text(avgwls[i], topn[i], str(i))
    plt.savefig('top' + str(n) + '_first_100.png', dpi=600)

def plot_samohlasky():
    plt.clf()
    plt.scatter(avgwls, samohlasky, s=0.5)
    plt.xlabel('Average word length')
    plt.ylabel('Samohlasky')
    plt.title('OCR quality')
    plt.savefig('samohlasky.png')
    plt.show()

def awgwls_colors():
  return [(1 if a>12 else a/12, a/8 if a<8 else 1 if a < 12 else (18-a)/6 if a<18 else 0, (8-a)/8 if a<8 else 0) for a in avgwls]

def plot_samo_topn(n):
    print("Calculating top " + str(n))
    topn = [row[np.argsort(row)[-n:]].values.sum() for i,row in train.iterrows()]
    print("Plotting top " + str(n))
    plt.clf()
    plt.scatter(samohlasky, topn, s=0.5, c=awgwls_colors())
    plt.xlabel('Samohlasky')
    plt.ylabel('Top ' + str(n) + ' characters')
    plt.title('OCR quality')
    plt.savefig('samohlasky_top' + str(n) + '.png', figsize=(6,4), dpi=300)


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

def plot_samo_skdists():
    plt.clf()
    plt.scatter(samohlasky, skdists, s=0.5, c=awgwls_colors())
    plt.xlabel('Samohlasky')
    plt.ylabel('SK distance')
    plt.title('OCR quality')
    plt.savefig('samohlasky_sk_dist.png', figsize=(6,4), dpi=300)
    plt.show()

print("Reading avgwls")
avgwls = [float(line) for line in open("current_avgwls").read().split('\n') if line]
print("Reading freqs")
train=pd.read_csv("current_freqs", dtype=np.float)
print("Calculating skdist")
skdists = [sk_dist(row) for i,row in train.iterrows()]
print("Calculating samohlasky")
samohlasky = [row[list('AEIOUYÁÉÍÓÚÝaeiouyáäéíóôúý')].values.sum() for i,row in train.iterrows()]

plot_samo_skdists()
