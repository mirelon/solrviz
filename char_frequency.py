#!/usr/bin/python3.6
import csv
import re

all_keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáäčďéíľĺňóôŕřšťúýžÁÄČĎÉÍĽĹŇÓÔŔŘŠŤÚÝŽ'

def char_frequency(str1):
    dict = {}.fromkeys(all_keys, 0)
    for n in str1:
        dict[n] += 1
    return dict

def average_word_length(str):
    words = str.split()
    return sum(len(word) for word in words) / len(words)

print("Reading docs")
with open('current_docs') as f:
    content = f.readlines()

print("Calculating average word lengths")
avgwls = [average_word_length(x) for x in content]
with open('current_avgwls', 'w') as avgwlsfile:
    for item in avgwls:
        avgwlsfile.write("%s\n" % item)
print("Removing newlines")
content = [x.replace("\n", "") for x in content]
print("Removing nonword chars")
content = [re.sub('[^' + all_keys + ']', '', x) for x in content]
print("Getting lengths")
lengths = [len(x) for x in content]
print("Getting char frequencies")
freqs = [char_frequency(x) for x in content]
print("Calculating relative frequencies")
dict = [{char:(freq/l if l>0 else 0) for char,freq in f.items()} for f,l in zip(freqs,lengths)]

print("Opening file for writing")
with open('current_freqs', 'w') as csvfile:
    w = csv.DictWriter(csvfile, delimiter=',', fieldnames=all_keys)
    w.writeheader()
    print("Writing rows")
    [w.writerow(d) for d in dict]
