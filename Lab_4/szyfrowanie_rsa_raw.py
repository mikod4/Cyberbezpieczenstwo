# szyfrowanie_raw_hex.py
import os
from Crypto.PublicKey import RSA

WEJSCIE = "wyniki/teksty/plaintext"
WYJSCIE = "wyniki/teksty/zaszyfrowane_hex"
KLUCZE = [512, 1024, 2048]


def load_pub(bits):
    with open(f"wyniki/klucze/rsa_{bits}_public.pem", "rb") as f:
        return RSA.import_key(f.read())


def encrypt_raw_blocks(data: bytes, key) -> list[str]:
    """Zwraca listę bloków szyfrogramu w hex, jeden blok = jedna linia."""
    n, e = key.n, key.e
    chunk = (n.bit_length() - 1) // 8   # m < n gwarantowane
    out_len = key.size_in_bytes()
    linie = []
    for i in range(0, len(data), chunk):
        blok = data[i:i + chunk].rjust(chunk, b"\x00")
        c = pow(int.from_bytes(blok, "big"), e, n)
        linie.append(c.to_bytes(out_len, "big").hex())
    return linie


for bits in KLUCZE:
    key = load_pub(bits)
    katalog = os.path.join(WYJSCIE, f"rsa_{bits}")
    os.makedirs(katalog, exist_ok=True)
    for nazwa in sorted(os.listdir(WEJSCIE)):
        sciezka = os.path.join(WEJSCIE, nazwa)
        if not os.path.isfile(sciezka):
            continue
        with open(sciezka, "rb") as f:
            dane = f.read()
        linie = encrypt_raw_blocks(dane, key)
        with open(os.path.join(katalog, nazwa), "w", encoding="ascii") as f:
            f.write("\n".join(linie) + "\n")
        print(f"{nazwa} RSA-{bits}: {len(dane)} B -> {len(linie)} bloków")