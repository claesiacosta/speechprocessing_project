# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 11:43:11 2021

@author: rasul
"""

import os
from decoding import get_rule_decoder, decode
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
        full_ref = folder + "/" + ref
        with open(full_ref, encoding="utf8") as f:
            #number = ref[-7:-4]
            labels += f.read()
    total_refs = folder + "/" + "xxx.ref"
    with open(total_refs, encoding="utf8", mode="w") as f:
       f.write(labels)

#read every file in the folder and create a hypothesis
def decode_folder(my_decoder, folder):
    raw = get_files(folder, ".raw")
    decoded = []
    for file in raw:
        full_path = folder + "/" + file
        pred = decode(my_decoder, full_path)
        decoded.append(pred)
    return decoded

def compile_pred(folder, rule, preds):
    full_path = folder + "/" + rule + ".pred"
    with open(full_path, encoding="utf8", mode="w") as f:
        f.write("\n".join(preds))
        
folder = r"td_corpus_digits/SNR05dB/man/seq5digits_100_files"
#compile_ref(folder)
my_decoder = get_rule_decoder()
decoded = decode_folder(my_decoder, folder)
compile_pred(folder, "5digits", decoded)