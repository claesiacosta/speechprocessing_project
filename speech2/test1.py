# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', 'ps_data/model/en-us')
config.set_string('-lm', 'ps_data/lm/en-us.lm.bin')
config.set_string('-dict', 'ps_data/lex/cmudict-en-us.dict')
# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open('ps_data/exemple/goforward.raw', 'rb')
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break
    decoder.end_utt()
hypothesis = decoder.hyp()
print ('Best hypothesis: ', hypothesis.hypstr)
