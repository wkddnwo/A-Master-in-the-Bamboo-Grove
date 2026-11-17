import pygame

pygame.init()


class COLOR:
    def __init__(self):
        self.SILVER = "#c0c0c0"
        self.GRAY = "#808080"
        self.WHITE = (255, 255, 255)

class FONT:
    def __init__(self):
        self.malgunbd = pygame.font.SysFont("malgungothic", 40, bold=True)

color = COLOR()
font = FONT()

class Screen_State:
    def update(self):
        pass

class main_menu(Screen_State):
    def __init__(self):
        self.font = pygame.font.SysFont("malgungothic", 40, bold=True)
        self.title = self.font.render("모드를 선택하세요", True, color.WHITE)
        self.aroww_mode_btn = Button("무한모드", (200, 200), (200, 60))
    def update(self, screen):
        screen.screen.fill((20, 20, 20))
        screen.screen.blit(self.title, (screen.WIDTH // 2 - self.title.get_width() // 2, 100))
        self.aroww_mode_btn.update(screen)
        
        pygame.display.flip()
        
class Button:
    def __init__(self, text, pos, size):
        self.text = font.malgunbd.render(text, True, color.WHITE)
        self.rect = pygame.Rect(pos, size)
        self.color = color.GRAY
    def update(self, screen):
        pygame.draw.rect(screen.screen, self.color, self.rect)
        screen.screen.blit(self.text, (self.rect.centerx- self.text.get_width() // 2, self.rect.centery - self.text.get_height()//2))
        if self.isHovered():
            self.color = color.SILVER
        else:
            self.color = color.GRAY
        for event in pygame.event.get():
            self.isClicked(event)
    def isHovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def isClicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
# class Button:
#     def __init__(self, text, pos, size):
#         self.text = text
#         self.rect = pygame.Rect(pos, size)
#         self.color = HOVER

#     def draw(self, surface):
#         mouse_pos = pygame.mouse.get_pos()
#         self.color = HOVER if self.rect.collidepoint(mouse_pos) else GRAY
#         pygame.draw.rect(surface, self.color, self.rect)
#         txt = font.render(self.text, True, WHITE)
#         surface.blit(txt, (self.rect.centerx - txt.get_width() // 2,
#                            self.rect.centery - txt.get_height() // 2))

#     def is_clicked(self, event):
#         return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)




class arrow_mode(Screen_State):
    def update(self):
        pass

class boom_mode(Screen_State):
    def uptade(self):
        pass

class Screen:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("죽림고수 - 모드 선택")

        self.state = main_menu()

    def update(self):
        self.state.update(self)


screen = Screen()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.update()

pygame.quit()

# import pygame
# import sys
# import math
# import random

# import bomb_mode
# import arrow_mde

# pygame.init()

# WIDTH, HEIGHT = 600, 600
# CENTER = (WIDTH // 2, HEIGHT // 2)
# RADIUS = 250
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("죽림고수 - 모드 선택")
# clock = pygame.time.Clock()
# font = pygame.font.Font("C:/Windows/Fonts/malgunbd.ttf", 40)
# small_font = pygame.font.Font("C:/Windows/Fonts/malgunbd.ttf",20)

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (100, 100, 100)
# HOVER = (160, 160, 160)
# MAP_COLOR = (30, 30, 30)
# PLAYER_COLOR = (50, 200, 255)
# ARROW_COLOR = (255, 60, 60)
# BOMB_COLOR = (255, 100, 0)
# EXPLOSION_COLOR = (255, 180, 100)
# BUTTON_COLOR = (80, 80, 80)
# BUTTON_HOVER = (120, 120, 120)

# player_radius = 5
# best_time = 0

# class Button:
#     def __init__(self, text, pos, size):
#         self.text = text
#         self.rect = pygame.Rect(pos, size)
#         self.color = HOVER

#     def draw(self, surface):
#         mouse_pos = pygame.mouse.get_pos()
#         self.color = HOVER if self.rect.collidepoint(mouse_pos) else GRAY
#         pygame.draw.rect(surface, self.color, self.rect)
#         txt = font.render(self.text, True, WHITE)
#         surface.blit(txt, (self.rect.centerx - txt.get_width() // 2,
#                            self.rect.centery - txt.get_height() // 2))

#     def is_clicked(self, event):
#         return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# # Main UI loop
# aroww_mode_btn = Button("무한모드", (200, 200), (200, 60))

# bomb_mode_btn = Button("폭탄모드",(200, 300),(200, 60))

# while True:
#     screen.fill((20, 20, 20))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if aroww_mode_btn.is_clicked(event):
#             best_time = arrow_mde.run_arrow_mode(best_time)
#         elif bomb_mode_btn.is_clicked(event):
#             bomb_mode.run_bomb_mode()

#     title = font.render("모드를 선택하세요", True, WHITE)
#     screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

#     aroww_mode_btn.draw(screen)
#     bomb_mode_btn.draw(screen)
#     pygame.display.flip()
#     clock.tick(60)