import pygame
import random

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        
        # Sprite potwora (czerwony prostokąt)
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Czerwony prostokąt
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Ruch w 4 kierunkach
        self.speed = random.uniform(1, 2.5)
        self.direction_x = random.choice([-1, 1])  # -1 lewo, 1 prawo
        self.direction_y = random.choice([-1, 1])  # -1 góra, 1 dół
        
        # Granice ruchu (prostokąt obszaru poruszania się)
        boundary_size = random.randint(80, 200)
        self.left_boundary = max(0, x - boundary_size//2)
        self.right_boundary = min(screen_width - 30, x + boundary_size//2)
        self.top_boundary = max(0, y - boundary_size//2)
        self.bottom_boundary = min(screen_height - 30, y + boundary_size//2)
        
        # Zapewnij że granice są w porządku
        if self.left_boundary >= self.right_boundary:
            self.left_boundary = max(0, x - 100)
            self.right_boundary = min(screen_width - 30, x + 100)
        if self.top_boundary >= self.bottom_boundary:
            self.top_boundary = max(0, y - 100)
            self.bottom_boundary = min(screen_height - 30, y + 100)
    
    def update(self):
        """Aktualizuje pozycję potwora"""
        # Porusz się w poziomie
        self.rect.x += self.speed * self.direction_x
        
        # Porusz się w pionie
        self.rect.y += self.speed * self.direction_y
        
        # Sprawdź kolizje z granicami poziomymi
        if self.rect.left <= self.left_boundary or self.rect.right >= self.right_boundary:
            self.direction_x *= -1  # Zmień kierunek poziomy
        
        # Sprawdź kolizje z granicami pionowymi
        if self.rect.top <= self.top_boundary or self.rect.bottom >= self.bottom_boundary:
            self.direction_y *= -1  # Zmień kierunek pionowy
        
        # Upewnij się że potwór jest w granicach
        if self.rect.left < self.left_boundary:
            self.rect.left = self.left_boundary
        if self.rect.right > self.right_boundary:
            self.rect.right = self.right_boundary
        if self.rect.top < self.top_boundary:
            self.rect.top = self.top_boundary
        if self.rect.bottom > self.bottom_boundary:
            self.rect.bottom = self.bottom_boundary 