import hashlib

def hash_function(word: str):
    return hashlib.sha256(word.encode('utf-8')).hexdigest()

print(hash_function('gideon'))