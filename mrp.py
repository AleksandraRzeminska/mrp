import math

def oblicz_mrp(nazwa, poziom, lead_time, zapotrzebowanie_brutto, stan_poczatkowy, partia, mnoznik):
    print(f"\n--- OBLICZENIA DLA: {nazwa} (Poziom {poziom}) ---")
    
    # Przygotowanie tabeli wyników
    tygodnie = len(zapotrzebowanie_brutto)
    planowany_stan = [0] * tygodnie
    zamowienia = [0] * tygodnie
    
    obecny_magazyn = stan_poczatkowy
    
    # Nagłówek tabeli
    print("Tydzień:     | " + " | ".join(f"{i:2}" for i in range(tygodnie)))
    print("-" * (15 + tygodnie * 5))
    print(f"Brutto:      | " + " | ".join(f"{x:2}" for x in zapotrzebowanie_brutto))

    for t in range(tygodnie):
        # Sprawdzamy, czy brakuje towaru
        if obecny_magazyn < zapotrzebowanie_brutto[t]:
            brak = zapotrzebowanie_brutto[t] - obecny_magazyn
            # Obliczamy ile partii musimy zamówić
            ile_zamowic = math.ceil(brak / partia) * partia
            
            # Sprawdzamy kiedy trzeba było złożyć zamówienie (Lead Time)
            tydzien_zamowienia = t - lead_time
            if tydzien_zamowienia >= 0:
                zamowienia[tydzien_zamowienia] = ile_zamowic
                obecny_magazyn += ile_zamowic
            else:
                print(f"UWAGA: Spóźnienie! Brakuje {brak} szt. {nazwa} w tygodniu {t}")

        obecny_magazyn -= zapotrzebowanie_brutto[t]
        planowany_stan[t] = obecny_magazyn

    print(f"Stan magaz.: | " + " | ".join(f"{x:2}" for x in planowany_stan))
    print(f"Zamówienia:  | " + " | ".join(f"{x:2}" for x in zamowienia))
    
    return zamowienia

# --- PROGRAM GŁÓWNY (Przykład - rower) ---

horyzont = 6  # 6 tygodni
# Puste listy na zapotrzebowanie (początkowo wszędzie zero)
zap_p0 = [0] * horyzont
zap_p1 = [0] * horyzont
zap_p2 = [0] * horyzont

# 1. Poziom 0: Rower
# Chcemy 20 rowerów w 5. tygodniu (indeks 5)
zap_p0[5] = 20
zamowienia_p0 = oblicz_mrp("Rower", 0, 1, zap_p0, 0, 10, 1)

# 2. Poziom 1: Rama (potrzeba 1 na rower)
# Zapotrzebowanie na ramy to zamówienia złożone na rowery
for i in range(horyzont):
    zap_p1[i] = zamowienia_p0[i] * 1
zamowienia_p1 = oblicz_mrp("Rama", 1, 2, zap_p1, 5, 1, 1)

# 3. Poziom 2: Rury (potrzeba 2 na ramę)
for i in range(horyzont):
    zap_p2[i] = zamowienia_p1[i] * 2
oblicz_mrp("Rury", 2, 1, zap_p2, 0, 1, 1)