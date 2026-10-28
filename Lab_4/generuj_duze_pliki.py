import os

KATALOG = "wyniki/teksty/duze_pliki"
ROZMIARY = {"1MB": 1_000_000, "2MB": 2_000_000, "5MB": 5_000_000}

os.makedirs(KATALOG, exist_ok=True)

for nazwa, rozmiar in ROZMIARY.items():
    sciezka = os.path.join(KATALOG, f"plik_{nazwa}.bin")
    with open(sciezka, "wb") as f:
        f.write(os.urandom(rozmiar))
    print(f"zapisano {sciezka}: {os.path.getsize(sciezka)} B")