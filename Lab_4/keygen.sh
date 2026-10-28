#!/bin/bash
set -e

OUT="wyniki/klucze_openssl"
MSG="wiadomosc.txt"
mkdir -p "$OUT"
echo "Lab 4 - test podpisu cyfrowego" > "$MSG"

echo "Wersja OpenSSL: $(openssl version)"
echo

for b in 512 1024 2048; do
  PRIV="$OUT/rsa_${b}_private.pem"
  PUB="$OUT/rsa_${b}_public.pem"

  echo "=== RSA-$b ==="

# Generowanie klucza prywatnego
  echo "Czas generowania:"
  time openssl genrsa -out "$PRIV" "$b" 2>/dev/null

  # Wyprowadzenie klucza publicznego
  openssl rsa -in "$PRIV" -pubout -out "$PUB" 2>/dev/null

  # Import: wczytanie klucza i sprawdzenie spójności
  openssl rsa -in "$PRIV" -check -noout 2>&1
  echo "Długość modułu: $(openssl rsa -in "$PRIV" -noout -text 2>/dev/null | head -1)"

  # Porównanie modułu klucza publicznego i prywatnego
  M_PRIV=$(openssl rsa -in "$PRIV" -noout -modulus)
  M_PUB=$(openssl rsa -pubin -in "$PUB" -noout -modulus)
  [ "$M_PRIV" = "$M_PUB" ] && echo "Import zgodny: True" || echo "Import zgodny: False"

  # Podpis cyfrowy: podpis kluczem prywatnym, weryfikacja publicznym
  SIG="$OUT/podpis_${b}.bin"
  openssl dgst -sha256 -sign "$PRIV" -out "$SIG" "$MSG"
  echo "Podpis: $(wc -c < "$SIG" | tr -d ' ') bajtów"
  openssl dgst -sha256 -verify "$PUB" -signature "$SIG" "$MSG"
  echo
done