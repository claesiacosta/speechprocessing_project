# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 22:11:01 2021

@author: rasul
"""

from experiment import get_files, get_folders
import os
corpus = "td_corpus_digits"
SNR = ["SNR05db", "SNR15db", "SNR25db", "SNR35db"]
seqs =["seq1digit_200_files", "seq3digits_100_files", "seq5digits_100_files"]
speakers = ["man", "woman", "boy", "girl"]
files = []

data = []

def confidence(wer, n):
    #percent to decimal
    wer = wer/100
    return 1.96 * ((wer * (1-wer) / n) ** (1/2)) * 100
def compile_data(corpus, SNR,speakers, seqs):
    data = []
    for db in SNR:
        for speaker in speakers:
            for seq in seqs:
                try:
                    folder = os.path.join(corpus, db, speaker, seq)
                    for file in os.listdir(folder):
                        full = os.path.join(folder, file)
                        if full.endswith(".txt"):
                            with open(full, encoding="utf8") as f:
                                lines = f.readlines()
                                summary = lines[-3]
                                for x in "()/\n%":
                                    summary = summary.replace(x, "")
                                    
                                summary = summary.split()
                                print(summary)
                                wer = summary[1]
                                n = summary[3]
                                ci = confidence(float(wer), int(n))
                                data.append("\t".join([db, speaker, seq, file[7:-4], wer, str(ci), n]))
                except(FileNotFoundError):
                    print(folder, "not found")
    return data
data = compile_data(corpus, SNR, speakers, seqs)
with open("summary.txt", mode="w", encoding="utf8") as f:
    header = "\t".join(["SNR", "SPKR", "DIGITS_SEQ", "RULE", "WER", "CONF_INT", "NUMS"])
    f.write(header +"\n")
    for line in data:
        f.write(line +"\n")
