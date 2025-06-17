import pygame
import random
import os
from player import Player
from monster import Monster
from coin import Coin

class Game:
    def __init__(self):
        # Stałe gry
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # Inicjalizacja ekranu
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("EscapeHero")
        self.clock = pygame.time.Clock()
        
        # Stan gry
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER, LEVEL_TRANSITION
        self.score = 0
        self.lives = 3
        self.level = 1
        
        # Timer dla przejścia między poziomami
        self.transition_timer = 0
        self.transition_duration = 4000  # 4 sekundy (w milisekundach)
        
        # Inicjalizacja obiektów
        self.init_game_objects()
        
        # Dźwięki
        self.load_sounds()
        
        # Font dla UI
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
    
    def init_game_objects(self):
        """Inicjalizuje obiekty gry"""
        # Gracz
        self.player = Player(100, 100)
        
        # Potwory
        self.monsters = pygame.sprite.Group()
        self.spawn_monsters()
        
        # Monety
        self.coins = pygame.sprite.Group()
        self.spawn_coins()
        
        # Grupy sprite'ów
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.monsters)
        self.all_sprites.add(self.coins)
    
    def spawn_monsters(self):
        """Tworzy potwory na planszy"""
        monster_count = 3 + self.level
        for i in range(monster_count):
            x = random.randint(50, self.SCREEN_WIDTH - 50)
            y = random.randint(50, self.SCREEN_HEIGHT - 50)
            monster = Monster(x, y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.monsters.add(monster)
    
    def spawn_coins(self):
        """Tworzy monety na planszy"""
        coin_count = 5 + self.level * 2
        for i in range(coin_count):
            x = random.randint(50, self.SCREEN_WIDTH - 30)
            y = random.randint(100, self.SCREEN_HEIGHT - 150)
            coin = Coin(x, y)
            self.coins.add(coin)
    
    def load_sounds(self):
        """Ładuje dźwięki gry"""
        try:
            # Generuj proste dźwięki programowo
            self.coin_sound = self.create_coin_sound()
            self.damage_sound = self.create_damage_sound()
        except Exception as e:
            print(f"Nie można załadować dźwięków: {e}")
            self.coin_sound = None
            self.damage_sound = None
    
    def create_coin_sound(self):
        """Tworzy dźwięk zbierania monety"""
        try:
            import numpy as np
            
            # Parametry dźwięku
            sample_rate = 22050
            duration = 0.2  # 0.2 sekundy
            
            # Generuj dźwięk dzwonka (wysokie tony)
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Mieszanka kilku częstotliwości dla efektu dzwonka
            frequency1 = 800  # Hz
            frequency2 = 1000  # Hz
            frequency3 = 1200  # Hz
            
            wave1 = np.sin(frequency1 * 2 * np.pi * t)
            wave2 = np.sin(frequency2 * 2 * np.pi * t) * 0.5
            wave3 = np.sin(frequency3 * 2 * np.pi * t) * 0.3
            
            # Dodaj envelope (zanikanie)
            envelope = np.exp(-t * 8)
            
            # Połącz wszystko
            wave = (wave1 + wave2 + wave3) * envelope
            
            # Normalizuj i konwertuj do 16-bit
            wave = (wave * 32767).astype(np.int16)
            
            # Stwórz stereo (duplikuj kanał) i upewnij się że jest C-contiguous
            stereo_wave = np.column_stack((wave, wave))
            stereo_wave = np.ascontiguousarray(stereo_wave)
            
            # Stwórz pygame sound object
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(0.3)  # Ustaw głośność na 30%
            
            return sound
            
        except ImportError:
            # Fallback - prosty beep bez numpy
            return self.create_simple_beep(800, 0.2, 0.3)
        except Exception as e:
            print(f"Błąd przy tworzeniu dźwięku monety: {e}")
            return None
    
    def create_damage_sound(self):
        """Tworzy dźwięk otrzymania obrażeń"""
        try:
            import numpy as np
            
            # Parametry dźwięku
            sample_rate = 22050
            duration = 0.3  # 0.3 sekundy
            
            # Generuj niski, ostry dźwięk
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Niskie częstotliwości dla efektu "aua"
            frequency1 = 150  # Hz - bardzo niski
            frequency2 = 200  # Hz
            
            wave1 = np.sin(frequency1 * 2 * np.pi * t)
            wave2 = np.sin(frequency2 * 2 * np.pi * t) * 0.7
            
            # Dodaj noise dla ostrzejszego efektu
            noise = np.random.random(len(t)) * 0.1
            
            # Envelope - szybkie zanikanie
            envelope = np.exp(-t * 6)
            
            # Połącz wszystko
            wave = (wave1 + wave2 + noise) * envelope
            
            # Normalizuj i konwertuj do 16-bit
            wave = (wave * 32767).astype(np.int16)
            
            # Stwórz stereo i upewnij się że jest C-contiguous
            stereo_wave = np.column_stack((wave, wave))
            stereo_wave = np.ascontiguousarray(stereo_wave)
            
            # Stwórz pygame sound object
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(0.4)  # Ustaw głośność na 40%
            
            return sound
            
        except ImportError:
            # Fallback - prosty beep bez numpy
            return self.create_simple_beep(150, 0.3, 0.4)
        except Exception as e:
            print(f"Błąd przy tworzeniu dźwięku obrażeń: {e}")
            return None
    
    def create_simple_beep(self, frequency, duration, volume):
        """Tworzy prosty beep bez numpy (fallback)"""
        try:
            import math
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Generuj prostą falę sinusoidalną
            arr = []
            for i in range(frames):
                time_val = float(i) / sample_rate
                wave_val = int(32767 * volume * math.sin(frequency * time_val * 2 * math.pi))
                arr.append([wave_val, wave_val])  # Stereo
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
            
        except Exception as e:
            print(f"Błąd przy tworzeniu prostego dźwięku: {e}")
            return None
    
    def handle_events(self):
        """Obsługuje zdarzenia"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
                
                elif self.game_state == "PLAYING":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
        
        return True
    
    def update(self):
        """Aktualizuje stan gry"""
        if self.game_state == "LEVEL_TRANSITION":
            self.update_level_transition()
            return
        elif self.game_state != "PLAYING":
            return
        
        # Aktualizuj gracza
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Aktualizuj potwory
        self.monsters.update()
        
        # Aktualizuj monety (animacja)
        self.coins.update()
        
        # Sprawdź kolizje z potworami
        if pygame.sprite.spritecollide(self.player, self.monsters, False):
            self.player_hit()
        
        # Sprawdź kolizje z monetami
        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collected_coins:
            self.score += 10
            if self.coin_sound:
                self.coin_sound.play()
        
        # Sprawdź czy wszystkie monety zostały zebrane
        if len(self.coins) == 0:
            self.start_level_transition()
    
    def player_hit(self):
        """Obsługuje uderzenie gracza"""
        self.lives -= 1
        if self.damage_sound:
            self.damage_sound.play()
        
        if self.lives <= 0:
            self.game_state = "GAME_OVER"
        else:
            # Zresetuj pozycję gracza
            self.player.rect.x = 100
            self.player.rect.y = 100
    
    def start_level_transition(self):
        """Rozpoczyna przejście do następnego poziomu"""
        self.level += 1
        self.score += 50  # Bonus za ukończenie poziomu
        self.game_state = "LEVEL_TRANSITION"
        self.transition_timer = pygame.time.get_ticks()
    
    def update_level_transition(self):
        """Aktualizuje stan przejścia między poziomami"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.transition_timer
        
        if elapsed >= self.transition_duration:
            # Czas minął, przejdź do następnego poziomu
            self.complete_level_transition()
    
    def complete_level_transition(self):
        """Kończy przejście i rozpoczyna nowy poziom"""
        # Usuń stare obiekty z all_sprites
        for monster in self.monsters:
            self.all_sprites.remove(monster)
        for coin in self.coins:
            self.all_sprites.remove(coin)
        
        # Usuń stare obiekty z grup
        self.monsters.empty()
        self.coins.empty()
        
        # Stwórz nowe
        self.spawn_monsters()
        self.spawn_coins()
        
        # Dodaj nowe obiekty do all_sprites
        self.all_sprites.add(self.monsters)
        self.all_sprites.add(self.coins)
        
        # Zresetuj pozycję gracza
        self.player.rect.x = 100
        self.player.rect.y = 100
        
        # Wróć do gry
        self.game_state = "PLAYING"
    
    def start_game(self):
        """Rozpoczyna nową grę"""
        self.game_state = "PLAYING"
        self.score = 0
        self.lives = 3
        self.level = 1
        self.init_game_objects()
    
    def restart_game(self):
        """Restartuje grę"""
        self.start_game()
    
    def draw_menu(self):
        """Rysuje menu główne"""
        self.screen.fill(self.BLACK)
        
        title = self.big_font.render("ESCAPEHERO", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "SPACJA - Rozpocznij grę",
            "ESC - Wyjście",
            "",
            "Sterowanie:",
            "Strzałki lub WASD - Ruch w 4 kierunkach",
            "",
            "Zbieraj monety, omijaj potwory!"
        ]
        
        y = 300
        for instruction in instructions:
            text = self.font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH//2, y))
            self.screen.blit(text, text_rect)
            y += 30
    
    def draw_game_over(self):
        """Rysuje ekran końca gry"""
        self.screen.fill(self.BLACK)
        
        game_over = self.big_font.render("KONIEC GRY", True, self.RED)
        game_over_rect = game_over.get_rect(center=(self.SCREEN_WIDTH//2, 200))
        self.screen.blit(game_over, game_over_rect)
        
        score_text = self.font.render(f"Wynik: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH//2, 300))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font.render(f"Poziom: {self.level}", True, self.WHITE)
        level_rect = level_text.get_rect(center=(self.SCREEN_WIDTH//2, 340))
        self.screen.blit(level_text, level_rect)
        
        instructions = [
            "R - Zagraj ponownie",
            "ESC - Menu główne"
        ]
        
        y = 400
        for instruction in instructions:
            text = self.font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH//2, y))
            self.screen.blit(text, text_rect)
            y += 40
    
    def draw_hud(self):
        """Rysuje interfejs użytkownika"""
        # Wynik
        score_text = self.font.render(f"Wynik: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Życia
        lives_text = self.font.render(f"Życia: {self.lives}", True, self.WHITE)
        self.screen.blit(lives_text, (10, 50))
        
        # Poziom
        level_text = self.font.render(f"Poziom: {self.level}", True, self.WHITE)
        self.screen.blit(level_text, (10, 90))
    
    def draw_level_transition(self):
        """Rysuje ekran przejścia między poziomami"""
        # Najpierw narysuj grę w tle
        self.screen.fill(self.BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        
        # Stwórz półprzezroczysty overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(180)  # Półprzezroczystość
        overlay.fill((0, 0, 0))  # Czarny
        self.screen.blit(overlay, (0, 0))
        
        # Oblicz ile czasu minęło
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.transition_timer
        
        # Informacja o poziomie
        level_text = self.big_font.render(f"POZIOM {self.level}", True, self.YELLOW)
        level_rect = level_text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - 100))
        self.screen.blit(level_text, level_rect)
        
        # Oblicz odliczanie
        if elapsed < 1000:  # Pierwsza sekunda - pokazuj tylko poziom
            pass
        elif elapsed < 2000:  # 1-2 sekunda
            countdown_text = self.big_font.render("3", True, self.WHITE)
            countdown_rect = countdown_text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
            self.screen.blit(countdown_text, countdown_rect)
        elif elapsed < 3000:  # 2-3 sekunda
            countdown_text = self.big_font.render("2", True, self.WHITE)
            countdown_rect = countdown_text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
            self.screen.blit(countdown_text, countdown_rect)
        elif elapsed < 4000:  # 3-4 sekunda
            countdown_text = self.big_font.render("1", True, self.WHITE)
            countdown_rect = countdown_text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
            self.screen.blit(countdown_text, countdown_rect)
        
        # Dodatkowe informacje
        if elapsed < 1000:
            info_text = self.font.render("Przygotuj się!", True, self.WHITE)
            info_rect = info_text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 + 50))
            self.screen.blit(info_text, info_rect)
        elif elapsed >= 3500:  # Pod koniec pokazuj START
            start_text = self.big_font.render("START!", True, self.GREEN)
            start_rect = start_text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
            self.screen.blit(start_text, start_rect)
    
    def draw(self):
        """Rysuje wszystko na ekranie"""
        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
        elif self.game_state == "LEVEL_TRANSITION":
            self.draw_level_transition()
        elif self.game_state == "PLAYING":
            # Tło
            self.screen.fill(self.BLUE)
            
            # Narysuj wszystkie sprite'y
            self.all_sprites.draw(self.screen)
            
            # HUD
            self.draw_hud()
        
        pygame.display.flip()
    
    def run(self):
        """Główna pętla gry"""
        running = True
        
        while running:
            # Ogranicz do 60 FPS
            self.clock.tick(60)
            
            # Obsłuż zdarzenia
            running = self.handle_events()
            
            # Aktualizuj stan gry
            self.update()
            
            # Narysuj wszystko
            self.draw() 