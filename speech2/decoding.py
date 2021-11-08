#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *


seqs = {1 : "seq1digit_200_files", 3 : "seq3digit_100_files", 5: "seq5digit_100_files"}
#These steps are the same whether we use ngram or jsgf language model
def set_hmm_dic(folder="ps_data", hmm="en-us",dic="cmudict-en-us"):
    config = Decoder.default_config()
    hmm = "/".join([folder, "model", hmm])
    dic = "/".join([folder, "lex", dic + ".dic"])
    config.set_string('-hmm',  hmm)
    config.set_string('-dict', dic)
    return config
    
# Create a decoder with acoustic model, language model (ngram), and pronunciation dict
def get_ngram_decoder(folder="ps_data", hmm="en-us",lm="en-us", dic="cmudict-en-us"):
    config = set_hmm_dic(folder=folder, hmm=hmm, dic=dic)
    lm = "/".join([folder, "lm", lm + ".lm.bin"])
    config.set_string('-lm',   lm)
    return Decoder(config)

#Use the previously configured decoder on a raw file
def decode(decoder, raw_file, ln="digits"):
    decoder.start_utt()
    stream = open(raw_file, 'rb')
    uttbuf = stream.read(-1)
    if uttbuf:
        decoder.process_raw(uttbuf, False, True)
    else:
        print ("Error reading speech data")
        exit ()
        decoder.end_utt()
    hyp = "<NULL>"
    if decoder.hyp():
        hyp = decoder.hyp().hypstr
    print (" ".join(["Decoding with", ln, "language:", hyp]))

    print ('')
    print ('--------------')
    print ('')
    decoder.end_utt()
    return hyp

#Create a decoder with acoustic model, pronunciation dictionary, grammar, and specific rule
def get_rule_decoder(folder="ps_data", hmm="en-us", dic="cmudict-en-us",
                     g_fold = "jsgf", grammar="digits",rule="5digits"):
    config = set_hmm_dic(folder=folder, hmm=hmm, dic=dic)
    decoder = Decoder(config)
    g_file = "/".join([folder, g_fold, grammar]) + ".gram"
    jsgf = Jsgf(g_file)
    jrule = jsgf.get_rule(grammar + "." + rule)
    fsg = jsgf.build_fsg(jrule, decoder.get_logmath(), 7.5)
    fsg.writefile("/".join([folder, g_fold, rule]) +".fsg")
    decoder.set_fsg(rule, fsg)
    decoder.set_search(rule)
    return decoder

def main(folder="./td_corpus_digits/SNR05dB/man/seq5digits_100_files/SNR05dB_man_seq5digits_010.raw"):
    decoder = get_rule_decoder()
    decode(decoder, folder)
    
if __name__ == "__main__":
    main()
    

