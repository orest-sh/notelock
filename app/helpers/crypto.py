import zlib
from hashlib import sha256

from cryptography.hazmat.primitives import padding

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)


def encrypt_and_compress(plaintext: str, password: str) -> bytes:
    hashed_pass = sha256(password.encode()).hexdigest()[:32]
    cipher = Cipher(algorithms.AES(hashed_pass.encode()), modes.ECB())

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    result = zlib.compress(ct)

    return result


def decrypt_and_decompress(ciphertext: bytes, password: str) -> str:
    hashed_pass = sha256(password.encode()).hexdigest()[:32]
    cipher = Cipher(algorithms.AES(hashed_pass.encode()), modes.ECB())

    decryptor = cipher.decryptor()

    decompressed = zlib.decompress(ciphertext)

    pt = decryptor.update(decompressed) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(pt) + unpadder.finalize()

    return unpadded_data.decode()
