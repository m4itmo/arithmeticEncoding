from arithmeticEncoding import ae

encoder = ae()

enc = encoder.encode_dec('abacaba')
print(enc)
print(encoder.decode_dec(enc['encoded'], enc['aplh']))
