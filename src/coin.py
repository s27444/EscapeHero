import pygame
import math

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Sprite monety (żółte kółko)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 8)  # Złoty środek
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animacja
        self.angle = 0
        self.bob_speed = 0.1
        self.bob_range = 5
        self.original_y = y
    
    def update(self):
        """Aktualizuje animację monety"""
        # Animacja unoszenia się w górę i w dół
        self.angle += self.bob_speed
        self.rect.y = self.original_y + math.sin(self.angle) * self.bob_range 