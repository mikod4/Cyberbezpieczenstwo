# entropia_tabela.py
import os
import numpy as np
from scipy.stats import entropy as scipy_entropy

PLAIN = "wyniki/teksty/plaintext"
ZASZYFR = "wyniki/teksty/zaszyfrowane"
PLIKI = ["jednorodny.txt", "srednio_zroznicowany.txt", "wysoce_zroznicowany.txt"]
KLUCZE = [512, 1024, 2048]


def entropy_scipy(data: bytes) -> float:
    counts = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
    return scipy_entropy(counts, base=2)


def read(path):
    with open(path, "rb") as f:
        return f.read()


naglowki = ["tekst", "TJ", "512 bit", "1024 bit", "2048 bit"]
print(f"{naglowki[0]:<28}" + "".join(f"{h:>12}" for h in naglowki[1:]))
print("-" * (28 + 12 * 4))

for plik in PLIKI:
    tj = read(os.path.join(PLAIN, plik))
    wartosci = [entropy_scipy(tj)]
    for bits in KLUCZE:
        tt = read(os.path.join(ZASZYFR, f"rsa_{bits}", plik))
        wartosci.append(entropy_scipy(tt))
    nazwa = plik.replace(".txt", "")
    print(f"{nazwa:<28}" + "".join(f"{v:>12.4f}" for v in wartosci))