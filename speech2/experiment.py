# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 11:43:11 2021

@author: rasul
"""

import os
from decoding import get_rule_decoder, get_ngram_decoder, decode
#take all of the individual references and put them into one file
def get_files(folder, end):
    all_f = os.listdir(folder)
    #get all the data files except the compilation
    return sorted([f for f in all_f if f.endswith(end) and "xxx" not in f])    

#take all of the individual references and put them into one file
def compile_ref(folder):
    refs = get_files(folder, ".ref")
    labels = ""
    for ref in refs:
        full_ref = os.path.join(folder, ref)
        with open(full_ref, encoding="utf8") as f:
            #number = ref[-7:-4]
            labels += f.read()
    total_refs = os.path.join(folder, "xxx.ref")
    with open(total_refs, encoding="utf8", mode="w") as f:

        f.write(labels)

#join all of the predictions into one file
def compile_pred(folder, rule, preds):
    full_path = os.path.join(folder, rule + ".pred")
    with open(full_path, encoding="utf8", mode="w") as f:
        f.write("\n".join(preds))

#read every file in the folder and create a hypothesis
def decode_folder(my_decoder, folder):
    raw = get_files(folder, ".raw")
    decoded = []
    for f in raw:
        full_path = os.path.join(folder,f)
        pred = decode(my_decoder, full_path)
        decoded.append(pred)
    return decoded



#generate paths - only 35 db has multiple voices so the general case assumes we are accessing a male voice
def get_folders(corpus, SNR,speakers, seqs):
    folders = []
    for db in SNR:
        for speaker in speakers:
            for seq in seqs:
                folder = os.path.join(corpus, db, speaker, seq)
            folders.append(folder)
    return folders

#
def decode_folders(rule, folders):
    my_decoder = None
    if rule =="ngram":
        my_decoder = get_ngram_decoder()
    else:
        my_decoder = get_rule_decoder(rule=rule)
    for folder in folders:
        compile_ref(folder)
        decoded = decode_folder(my_decoder, folder) 
    compile_pred(folder, rule, decoded)

def main(rule):
    SNR = ["SNR05db", "SNR15db", "SNR25db", "SNR35db"]
    seqs =["seq1digit_200_files", "seq3digits_100_files", "seq5digits_100_files"]
    speakers = ["man"]
    folders = get_folders("td_corpus_digits", SNR, speakers, seqs)
    decode_folders(rule, folders)

def test_speaker(rule):
    SNR = ["SNR35db"]
    seqs =["seq1digit_200_files", "seq3digits_100_files", "seq5digits_100_files"]
    speakers = ["man", "woman", "boy", "girl"]
    folders = get_folders("td_corpus_digits", SNR, speakers, seqs)
    decode_folders(rule, folders)

if __name__ == "__main__":
    rules = ["5digits", "3digits", "ngram", "loop"]
    for rule in rules:
        #main(rule)
        test_speaker(rule)
