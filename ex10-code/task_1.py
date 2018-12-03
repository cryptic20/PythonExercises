from base64_encoder import encode_base64_str as encoder
from base64_decoder import decode_base64_str as decoder


def verify_encoding_decoding(string):
    encode = encoder(string)
    decode = decoder(encode)
    return True if string == decode else False


if __name__ == '__main__':
    # verify_encoding_decoding should return True
    assert verify_encoding_decoding("Try out any test string here!")
