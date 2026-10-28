# odszyfruj_rsa_raw.py
import os
import sys
from Crypto.PublicKey import RSA

PLAIN = "wyniki/teksty/plaintext"
WYJSCIE = "wyniki/teksty/odszyfrowane"


def load_priv(bits):
    with open(f"wyniki/klucze/rsa_{bits}_private.pem", "rb") as f:
        return RSA.import_key(f.read())


def decrypt_raw(szyfr: bytes, key, dlugosc_oryginalu: int) -> bytes:
    n, d = key.n, key.d
    k = key.size_in_bytes()
    chunk = (n.bit_length() - 1) // 8

    bloki = []
    for i in range(0, len(szyfr), k):
        c = int.from_bytes(szyfr[i:i + k], "big")
        bloki.append(pow(c, d, n).to_bytes(chunk, "big"))

    # Pełne bloki mają chunk bajtów. Ostatni blok był dopełniony zerami z lewej,
    # więc z niego bierzemy tylko r ostatnich bajtów.
    q, r = divmod(dlugosc_oryginalu, chunk)
    return b"".join(bloki[:q]) + (bloki[q][-r:] if r else b"")


if len(sys.argv) != 2:
    sys.exit("Użycie: python odszyfruj_rsa_raw.py <plik_hex>")

sciezka = sys.argv[1]
nazwa = os.path.basename(sciezka)

katalog = os.path.basename(os.path.dirname(os.path.abspath(sciezka)))
if not katalog.startswith("rsa_"):
    sys.exit("Plik musi leżeć w katalogu rsa_512, rsa_1024 lub rsa_2048.")
bits = int(katalog.split("_")[1])

oryginal = os.path.join(PLAIN, nazwa)
if not os.path.exists(oryginal):
    sys.exit(f"Brak oryginału do określenia długości: {oryginal}")
dlugosc = os.path.getsize(oryginal)

with open(sciezka, "r", encoding="ascii") as f:
    szyfr = bytes.fromhex(f.read().strip())

odszyfr = decrypt_raw(szyfr, load_priv(bits), dlugosc)

os.makedirs(WYJSCIE, exist_ok=True)
wyjscie = os.path.join(WYJSCIE, nazwa)
with open(wyjscie, "wb") as f:
    f.write(odszyfr)

ok = odszyfr == open(oryginal, "rb").read()
print(f"{nazwa} RSA-{bits}: odszyfrowano {len(odszyfr)} B, zgodne z oryginałem: {ok} -> {wyjscie}")