from base64_encoder import encode_base64_str as encode
from base64_decoder import decode_base64_str as decode


def verify_encoding_decoding(string):
    encoded_string = encode(string)
    decoded_string = decode(encoded_string)
    return True if string == decoded_string else False


if __name__ == '__main__':
    # verify_encoding_decoding should return True
    assert verify_encoding_decoding("Try out any test string here!")
