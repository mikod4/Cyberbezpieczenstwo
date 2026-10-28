# punkt_1_6.py
import os
from Crypto.PublicKey import RSA

PLAIN_DIR = "wyniki/teksty/plaintext"
SZYFR_DIR = "wyniki/teksty/zaszyfrowane_hex"
PLIK = "test.txt"
KLUCZE = [512, 2048]
PODGLAD_BLOKOW = 12
POZYCJA_BLOKU = 6   # numer bloku szyfrogramu, w którym wykonujemy zmianę/usunięcie


def load_priv(bits):
    with open(f"wyniki/klucze/rsa_{bits}_private.pem", "rb") as f:
        return RSA.import_key(f.read())


def load_szyfr(bits):
    with open(os.path.join(SZYFR_DIR, f"rsa_{bits}", PLIK), "r", encoding="ascii") as f:
        return bytes.fromhex(f.read().strip())


def odszyfruj_bloki(szyfr, key):
    k = key.size_in_bytes()
    chunk = (key.n.bit_length() - 1) // 8
    wynik = []
    for i in range(0, len(szyfr), k):
        c = int.from_bytes(szyfr[i:i + k], "big")
        m = pow(c, key.d, key.n).to_bytes(k, "big")
        wynik.append(m[-chunk:])
    return wynik


def raport(nazwa, szyfr, key):
    odsz = odszyfruj_bloki(szyfr, key)
    print(f"\n{nazwa}")
    print(f"  pierwsze {PODGLAD_BLOKOW} bloków:")
    for i in range(min(PODGLAD_BLOKOW, len(odsz))):
        tekst = odsz[i].decode("utf-8", errors="replace")
        print(f"    [{i:3d}] {tekst}")


def main():
    for bits in KLUCZE:
        key = load_priv(bits)
        k = key.size_in_bytes()
        szyfr = load_szyfr(bits)

        poz_bajt = POZYCJA_BLOKU * k + 10   # zmiana/usunięcie 1 i 50 bajtów: w środku bloku
        poz_blok = POZYCJA_BLOKU * k        # usunięcie k bajtów: na granicy bloku

        print(f"\n===== RSA-{bits} (blok szyfrogramu {k} B) =====")

        raport("0. bez zmian", szyfr, key)

        b = bytearray(szyfr)
        b[poz_bajt] ^= 0xFF
        raport("1. zmiana 1 bajtu", bytes(b), key)

        raport("2. usunięcie 1 bajtu",
               szyfr[:poz_bajt] + szyfr[poz_bajt + 1:], key)

        raport("3. usunięcie 50 bajtów",
               szyfr[:poz_bajt] + szyfr[poz_bajt + 50:], key)

        raport(f"4. usunięcie {k} bajtów (długość modułu, granica bloku)",
               szyfr[:poz_blok] + szyfr[poz_blok + k:], key)


if __name__ == "__main__":
    main()