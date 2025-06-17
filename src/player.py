import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Sprite gracza (prostokąt)
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # Zielony prostokąt
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Ruch w 4 kierunkach
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4
        
        # Pozycja startowa (do respawnu)
        self.start_x = x
        self.start_y = y
    
    def update(self, keys, screen_width, screen_height):
        """Aktualizuje pozycję i stan gracza"""
        # Ruch poziomy
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        
        # Ruch pionowy
        self.vel_y = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = self.speed
        
        # Aktualizuj pozycję
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Kolizje z krawędziami ekranu
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    
    def reset_position(self):
        """Resetuje gracza do pozycji startowej"""
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vel_x = 0
        self.vel_y = 0 