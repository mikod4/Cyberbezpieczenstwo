import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

WEJSCIE = "wyniki/teksty/plaintext"
WYJSCIE = "wyniki/teksty/zaszyfrowane"
KLUCZE = [512, 1024, 2048]


def load_pub(bits):
    with open(f"wyniki/klucze/rsa_{bits}_public.pem", "rb") as f:
        return RSA.import_key(f.read())


def encrypt_blocks(data, pub):
    chunk = pub.size_in_bytes() - 11  # limit danych dla PKCS#1 v1.5
    cipher = PKCS1_v1_5.new(pub)
    return b"".join(cipher.encrypt(data[i:i + chunk]) for i in range(0, len(data), chunk))


pubs = {bits: load_pub(bits) for bits in KLUCZE}

for bits in KLUCZE:
    os.makedirs(os.path.join(WYJSCIE, f"rsa_{bits}"), exist_ok=True)

for nazwa in sorted(os.listdir(WEJSCIE)):
    sciezka = os.path.join(WEJSCIE, nazwa)
    if not os.path.isfile(sciezka):
        continue
    with open(sciezka, "rb") as f:
        dane = f.read()
    for bits in KLUCZE:
        szyfr = encrypt_blocks(dane, pubs[bits])
        out = os.path.join(WYJSCIE, f"rsa_{bits}", nazwa)
        with open(out, "wb") as f:
            f.write(szyfr)
        print(f"{nazwa} RSA-{bits}: {len(dane)} B -> {len(szyfr)} B")