from hashlib import sha256

def sha256_encode(data):
    return sha256(data.encode('utf-8')).hexdigest()