# autokorelacja_wykresy.py
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PLAIN = "wyniki/teksty/plaintext"
ZASZYFR = "wyniki/teksty/zaszyfrowane"
OUT = "wyniki/wykresy"
TEKSTY = {
    "jednorodny": "jednorodny.txt",
    "srednio_zroznicowany": "srednio_zroznicowany.txt",
    "wysoce_zroznicowany": "wysoce_zroznicowany.txt",
}
KLUCZE = [512, 1024, 2048]
MAX_LAG = 1200


def read(path):
    with open(path, "rb") as f:
        return f.read()


def zgodne_znaki(data, max_lag=MAX_LAG):
    """Liczba znaków zgodnych dla odstępu k: ile x[i] == x[i+k]. Jak w CrypTool."""
    x = np.frombuffer(data, dtype=np.uint8)
    max_lag = min(max_lag, len(x) - 1)
    return np.array([int(np.sum(x[:-k] == x[k:])) for k in range(1, max_lag + 1)])


def rysuj(wartosci, tytul, sciezka):
    lags = np.arange(1, len(wartosci) + 1)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(lags, wartosci, color="black", lw=0.8)
    ax.set_title(tytul, fontsize=11)
    ax.set_xlabel("Odstęp")
    ax.set_ylabel("Liczba znaków, które się zgadzają")
    ax.set_xlim(1, len(wartosci))
    ymin, ymax = wartosci.min(), wartosci.max()
    margin = max((ymax - ymin) * 0.1, 1)  # oś dopasowana do danych, jak w CrypTool
    ax.set_ylim(ymin - margin, ymax + margin)
    ax.grid(False)
    fig.tight_layout()
    fig.savefig(sciezka, dpi=150)
    plt.close(fig)


for nazwa, plik in TEKSTY.items():
    katalog = os.path.join(OUT, nazwa)
    os.makedirs(katalog, exist_ok=True)

    tj = read(os.path.join(PLAIN, plik))
    rysuj(zgodne_znaki(tj), f"Autokorelacja <tekst jawny: {nazwa}>",
          os.path.join(katalog, "TJ.png"))

    for bits in KLUCZE:
        tt = read(os.path.join(ZASZYFR, f"rsa_{bits}", plik))
        rysuj(zgodne_znaki(tt), f"Autokorelacja <zaszyfrowany RSA-{bits}: {nazwa}>",
              os.path.join(katalog, f"TT_{bits}.png"))

    print(f"{nazwa}: zapisano 4 wykresy w {katalog}")