# Raport Powyjazdowy

Desktopowa aplikacja Python do tworzenia raportów powyjazdowych z pomiarów czujników na obiektach budowlanych. Generuje profesjonalne pliki PDF z logo firmy w nagłówku, obsługuje 9 modułów raportu i umożliwia import istniejących raportów PDF.

## Wymagania

- Python 3.10+
- Środowisko z dostępem do ekranu (GUI)

## Instalacja

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/kmshm/raport_powyjazdowy.git
cd raport_powyjazdowy

# 2. (Opcjonalnie) Utwórz wirtualne środowisko
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Zainstaluj zależności
pip install -r requirements.txt
```

## Uruchomienie

```bash
python3 main.py
```

## Moduły raportu

| # | Moduł | Przełączalny |
|---|-------|:---:|
| 1 | Informacje Ogólne | ✗ (zawsze aktywny) |
| 2 | Sprzęt Pomiarowy | ✓ |
| 3 | Czujniki Światłowodowe | ✓ |
| 4 | Czujniki Inne | ✓ |
| 5 | Inwentaryzacja | ✓ |
| 6 | Przebieg Pomiarów | ✓ |
| 7 | Lista Rzeczy do Zabrania | ✓ |
| 8 | Uwagi | ✓ |
| 9 | Logistyka i Organizacja | ✓ |

## Funkcje

- **Generowanie PDF** — jednolity układ z logo firmy w nagłówku każdej strony
- **Import PDF** — wczytuje wcześniej wygenerowany raport i uzupełnia formularz
- **Pola opcjonalne** — puste pola nie pojawiają się w PDF
- **Moduły przełączalne** — każdy moduł (oprócz 1) można wyłączyć
- **Automatyczna nazwa pliku** — `RRRR-MM-DD-{numer_projektu}-{inicjały}.pdf`
- **Walidacja** — wymagane: inicjały, numer projektu, data pomiarów
- **Podgląd PDF** — generuje tymczasowy plik i otwiera go w przeglądarce systemowej

## Logo firmy

Logo jest wbudowane w aplikację jako plik `assets/logo.png`. Pojawia się automatycznie w nagłówku każdego wygenerowanego PDF. Aby zmienić logo, zamień plik `assets/logo.png` na własny (zalecany rozmiar: 400×140 px, format PNG z przezroczystością lub JPEG).

## Struktura projektu

```
raport_powyjazdowy/
├── main.py                    # Punkt wejścia
├── requirements.txt
├── assets/
│   └── logo.png              # Logo firmy
└── src/
    ├── app.py                 # Główne okno aplikacji
    ├── theme.py               # Kolory, czcionki, stylesheet
    ├── modules/
    │   ├── base_module.py     # Bazowa klasa modułu
    │   ├── module1_info.py    # Informacje ogólne
    │   ├── module2_equipment.py
    │   ├── module3_fiber.py
    │   ├── module4_sensors.py
    │   ├── module5_inventory.py
    │   ├── module6_measurements.py
    │   ├── module7_packing.py
    │   ├── module8_notes.py
    │   └── module9_logistics.py
    ├── pdf/
    │   ├── generator.py       # Generowanie PDF (ReportLab)
    │   └── parser.py          # Parsowanie istniejących PDF (PyMuPDF)
    └── utils/
        └── validators.py      # Walidacja pól i generowanie nazwy pliku
```

## Zależności

| Biblioteka | Wersja | Zastosowanie |
|-----------|--------|-------------|
| PyQt6 | ≥ 6.6 | Framework GUI |
| reportlab | ≥ 4.0 | Generowanie PDF |
| PyMuPDF | ≥ 1.23 | Import/parsowanie PDF |
| Pillow | ≥ 10.0 | Przetwarzanie obrazów |

## Licencja

MIT
