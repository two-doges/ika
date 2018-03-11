'''user hash mod'''
from time import time
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from config import KEY, SALT


def gen_user_id(uid):
    '''gen unique id for user'''
    uuid = str(int(time()*1000)) + str(uid) + str(SALT)
    cipher = AES.new(KEY.encode('utf-8'), AES.MODE_EAX)
    nonce = cipher.nonce
    ctext, _ = cipher.encrypt_and_digest(uuid.encode('utf-8'))
    return b64encode(nonce + ctext).decode('utf-8')


def verify_user_id(bct):  # b = base64 c = crypto
    '''verify user id for spec user'''
    try:
        ccup = b64decode(bct.encode('utf-8'))
        nonce = ccup[:16]
        ctext = ccup[16:]
        cipher = AES.new(KEY.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
        uuid = cipher.decrypt(ctext)
        if not uuid.decode('utf-8').endswith(SALT):
            return None
        # generator user hash
        # hash for 3 time
        hash_f = SHA256.new()
        hash_id = uuid  # hash id should be a byte string this time
        for _ in range(3):
            hash_f.update(hash_id)
            hash_id = hash_f.digest()
        return b64encode(hash_id).decode('utf-8')[:12]
    except Exception as err:
        raise RuntimeError('Invalid user id') from err
