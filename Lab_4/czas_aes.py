# czas_aes.py
import os
import time
from Crypto.Cipher import AES
from Crypto.Util import Counter

KATALOG = "wyniki/teksty/duze_pliki"
KLUCZE_BITS = [128, 192, 256]


def make_cipher(key, nonce):
    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    return AES.new(key, AES.MODE_CTR, counter=ctr)


pliki = sorted(f for f in os.listdir(KATALOG) if os.path.isfile(os.path.join(KATALOG, f)))

wyniki = []
for plik in pliki:
    with open(os.path.join(KATALOG, plik), "rb") as f:
        dane = f.read()
    for bits in KLUCZE_BITS:
        key = os.urandom(bits // 8)
        nonce = os.urandom(8)

        t0 = time.perf_counter()
        szyfr = make_cipher(key, nonce).encrypt(dane)
        t_enc = time.perf_counter() - t0

        t0 = time.perf_counter()
        odszyfr = make_cipher(key, nonce).decrypt(szyfr)
        t_dec = time.perf_counter() - t0

        ok = odszyfr == dane
        wyniki.append((plik, bits, t_enc, t_dec))
        print(f"{plik} AES-{bits}: szyfrowanie {t_enc:.4f} s, "
              f"deszyfrowanie {t_dec:.4f} s, poprawnie: {ok}")

print("\nTabela")
print(f"{'plik':<18}{'klucz':>8}{'szyfr [s]':>12}{'deszyfr [s]':>14}")
for plik, bits, te, td in wyniki:
    print(f"{plik:<18}{bits:>8}{te:>12.4f}{td:>14.4f}")