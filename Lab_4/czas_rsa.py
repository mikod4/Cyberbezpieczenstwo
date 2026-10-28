# czas_rsa.py
import os
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

KATALOG = "wyniki/teksty/duze_pliki"
KLUCZE = [512, 1024, 2048]
WYNIKI = "wyniki/czasy"
os.makedirs(WYNIKI, exist_ok=True)


def load_key(bits, private=False):
    nazwa = f"rsa_{bits}_{'private' if private else 'public'}.pem"
    with open(os.path.join("wyniki/klucze", nazwa), "rb") as f:
        return RSA.import_key(f.read())


def encrypt_blocks(data, pub):
    chunk = pub.size_in_bytes() - 11
    cipher = PKCS1_v1_5.new(pub)
    return b"".join(cipher.encrypt(data[i:i + chunk]) for i in range(0, len(data), chunk))


def decrypt_blocks(data, priv):
    k = priv.size_in_bytes()
    cipher = PKCS1_v1_5.new(priv)
    return b"".join(cipher.decrypt(data[i:i + k], sentinel=None) for i in range(0, len(data), k))


pliki = sorted(f for f in os.listdir(KATALOG) if os.path.isfile(os.path.join(KATALOG, f)))

wyniki = []
for plik in pliki:
    with open(os.path.join(KATALOG, plik), "rb") as f:
        dane = f.read()
    for bits in KLUCZE:
        pub = load_key(bits)
        priv = load_key(bits, private=True)

        t0 = time.perf_counter()
        szyfr = encrypt_blocks(dane, pub)
        t_enc = time.perf_counter() - t0

        t0 = time.perf_counter()
        odszyfr = decrypt_blocks(szyfr, priv)
        t_dec = time.perf_counter() - t0

        ok = odszyfr == dane
        wyniki.append((plik, bits, t_enc, t_dec))
        print(f"{plik} RSA-{bits}: szyfrowanie {t_enc:.2f} s, "
              f"deszyfrowanie {t_dec:.2f} s, poprawnie: {ok}")

print("\nTabela")
print(f"{'plik':<18}{'klucz':>8}{'szyfr [s]':>12}{'deszyfr [s]':>14}")
for plik, bits, te, td in wyniki:
    print(f"{plik:<18}{bits:>8}{te:>12.2f}{td:>14.2f}")