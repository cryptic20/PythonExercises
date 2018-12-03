from base64 import urlsafe_b64encode


def encode_base64_str(string):
    return urlsafe_b64encode(string.encode('ascii')).decode('ascii')

