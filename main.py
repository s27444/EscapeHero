#!/usr/bin/env python3
"""
EscapeHero - Główny plik gry
Platformówka 2D napisana w Pygame
"""

import pygame
import sys
import os

# Dodaj katalog src do ścieżki
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import Game

def main():
    # Inicjalizacja Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Utwórz grę
    game = Game()
    
    # Uruchom grę
    game.run()
    
    # Zamknij Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 