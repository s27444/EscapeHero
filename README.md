# EscapeHero

Prosta gra 2D z ruchem w czterech kierunkach napisana w Pygame.

## Opis gry

**EscapeHero** to gra zręcznościowa, w której gracz steruje bohaterem, omija wrogów i zbiera monety, aby zdobyć jak największą liczbę punktów.

## Funkcjonalności

✅ **Sterowanie klawiaturą**: ruch w lewo/prawo, skok  
✅ **System kolizji**: bohater vs wrogowie, bohater vs monety  
✅ **Przeciwnicy**: wrogowie poruszają się w określonym zakresie  
✅ **Zbieranie monet**: monety dają punkty i animują się  
✅ **System żyć**: bohater ma 3 życia  
✅ **System punktów**: wyświetlane na interfejsie użytkownika  
✅ **Poziomy**: liczba wrogów i monet rośnie z poziomem  
✅ **Menu startowe**: opcje graj/wyjście  
✅ **Ekran przegranej**: wynik i opcje restartu  
✅ **Efekty wizualne**: kolorowe sprite'y i animacje  

## Instalacja

1. Zainstaluj wymagane zależności:
```bash
pip install -r requirements.txt
```

2. Uruchom grę:
```bash
python main.py
```

## Sterowanie

### Menu główne:
- **SPACJA** - Rozpocznij grę
- **ESC** - Wyjście z gry

### W grze:
- **Strzałki** lub **WASD** - Ruch w 4 kierunkach (góra, dół, lewo, prawo)
- **ESC** - Powrót do menu

### Ekran końca gry:
- **R** - Zagraj ponownie
- **ESC** - Powrót do menu głównego

## Mechanika gry

- **Cel**: Zbieraj żółte monety i omijaj czerwonych potworów
- **Punkty**: 
  - 10 punktów za każdą monetę
  - 50 punktów bonus za ukończenie poziomu
- **Życia**: Zaczynasz z 3 życiami, tracisz jedno gdy dotkniesz potwora
- **Poziomy**: Po zebraniu wszystkich monet przechodzisz do następnego poziomu z większą liczbą wrogów

## Struktura projektu

```
EscapeHero/
├── main.py              # Główny plik uruchamiający
├── requirements.txt     # Zależności Pythona
├── README.md           # Ta dokumentacja
└── src/                # Kod źródłowy
    ├── game.py         # Główna klasa gry
    ├── player.py       # Klasa gracza
    ├── monster.py      # Klasa potworów
    └── coin.py         # Klasa monet
```

## Grafika

Gra używa prostych kolorowych kształtów:
- **Gracz**: Zielony prostokąt (40x60 pikseli)
- **Potwory**: Czerwone prostokąty (30x40 pikseli)
- **Monety**: Żółte kółka z animacją unoszenia się
- **Tło**: Niebieskie tło z interfejsem użytkownika

Miłej zabawy! 🎮