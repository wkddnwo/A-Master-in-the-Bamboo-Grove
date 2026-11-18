import pygame
import math




pygame.init()


class COLOR:
    def __init__(self):
        self.SILVER = "#c0c0c0"
        self.GRAY = "#808080"
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

class FONT:
    def __init__(self):
        self.malgunbd = pygame.font.SysFont("malgungothic", 40, bold=True)

color = COLOR()
font = FONT()


class Screen_State:
    def update(self, screen):
        pass
    def event_update(self, event):
        pass




class main_menu(Screen_State):
    def __init__(self, screen):
        pygame.display.set_caption("죽림고수 - 모드 선택")
        def change_aroww_mode():
            screen.state = arrow_mode(screen)
        def change_boom_mode():
            screen.state = boom_mode(screen)
        
        self.title = font.malgunbd.render("모드를 선택하세요", True, color.WHITE)
        
        #버튼선언
        self.aroww_mode_btn = Button("무한모드", (200, 200), (200, 60), change_aroww_mode)
        self.bomb_mode_btn = Button("폭탄모드",(200, 300),(200, 60), change_boom_mode)
    
    def update(self, screen):
        screen.screen.fill((20, 20, 20))
        screen.screen.blit(self.title, (screen.WIDTH // 2 - self.title.get_width() // 2, 100))
        
        #버튼 그리기
        self.aroww_mode_btn.update(screen)
        self.bomb_mode_btn.update(screen)
        # pygame.display.flip()

    def event_update(self, event):
        self.aroww_mode_btn.isClicked(event)
        self.bomb_mode_btn.isClicked(event)



class Button:
    def __init__(self, text, pos, size, callback):
        self.text = font.malgunbd.render(text, True, color.WHITE)
        self.rect = pygame.Rect(pos, size)
        self.color = color.GRAY
        self.callback = callback
    def update(self, screen):
        pygame.draw.rect(screen.screen, self.color, self.rect)
        screen.screen.blit(self.text, (self.rect.centerx- self.text.get_width() // 2, self.rect.centery - self.text.get_height()//2))
        if self.isHovered():
            self.color = color.SILVER
        else:
            self.color = color.GRAY
    def isHovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()






class arrow_mode(Screen_State):
    def __init__(self, screen):
        pygame.display.set_caption("죽림고수 - 무한모드")
        
        self.state = Playeralive(screen)

    def update(self, screen):
        #맵 그리기
        screen.screen.fill(color.BLACK)
        pygame.draw.circle(screen.screen, (30, 30, 30), (screen.WIDTH // 2, screen.HEIGHT // 2), 250)
        
        
        self.state.update(screen, self)
        
    
    def event_update(self, event):
        self.state.event_update(event)

    def change_state(self, state):
        self.state = state

class Arrow:
    def __init__(self, pos, target_pos):
        self.posx = pos[0]
        self.posy = pos[1]
        target_posx = target_pos[0]
        target_posy = target_pos[1]
        dist = math.hypot(target_posx-self.posx, target_posy - self.posy)
        self.speed = 3.5
        self.dx = (target_posx - self.posx) / dist
        self.dy = (target_posy - self.posy) / dist

        #화살 이미지 생성
        self.size = (4, 12)
        angle = math.atan2(self.dy, self.dx)
        surf = pygame.Surface(self.size)
        surf.fill((255, 60, 60))
        surf.set_colorkey(color.BLACK)
        self.rot_image = pygame.transform.rotate(surf, -math.degrees(angle))
        self.rect = self.rot_image.get_rect(center=(self.posx, self.posy))

        
    def update(self, screen):
        #위치 업데이트
        self.posx += (self.dx * self.speed)
        self.posy += (self.dy * self.speed)
        #이미지 그리기
        self.rect = self.rot_image.get_rect(center=(self.posx, self.posy))
        screen.screen.blit(self.rot_image, self.rect)

class ArrowGenerator:
    def __init__(self, game_start_time):
        self.arrows = []
        self.last_time = game_start_time
        self.last_time_special = game_start_time
        self.firing_cooldown = 500
        self.special_firing_cooldown = 5000
    def update(self, screen, player):
        if pygame.time.get_ticks() - self.last_time >= self.firing_cooldown :
            angle = math.atan2(player.posy - screen.HEIGHT // 2, player.posx - screen.WIDTH // 2)
            pos_x = screen.WIDTH // 2 + math.cos(angle + (math.pi)) * (250 + 40) #맵 지름에 40을 더함
            pos_y = screen.HEIGHT // 2 + math.sin(angle + (math.pi)) * (250 + 40)
            self.arrows.append(Arrow((pos_x, pos_y), (player.posx, player.posy)))
            self.last_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_time_special >= self.special_firing_cooldown:
            for i in range(10):
                angle = i * (2 * math.pi / 10)
                x = screen.WIDTH // 2 + math.cos(angle) * (250 + 40)#맵 지름에 40을 더함
                y = screen.HEIGHT // 2 + math.sin(angle) * (250 + 40)
                self.arrows.append(Arrow((x, y), (player.posx, player.posy)))
            self.last_time_special = pygame.time.get_ticks()
            self.special_firing_cooldown = 3000
        



class ArrowManager:
    def __init__(self, game_start_time):
        self.arrow_generator = ArrowGenerator(game_start_time)
    def update(self, screen, player):
        self.arrow_generator.update(screen, player)
        for arrow in self.arrow_generator.arrows:
            arrow.update(screen)
        self.del_arrow(screen)

    def del_arrow(self, screen):
        self.arrow_generator.arrows = [arrow for arrow in self.arrow_generator.arrows if(arrow.posx > 0 and arrow.posx < screen.WIDTH and arrow.posy > 0 and arrow.posy < screen.HEIGHT)]




class boom_mode(Screen_State):
    def __init__(self, screen):
        pygame.display.set_caption("죽림고수 - 폭탄모드")
    def update(self, screen):
        screen.screen.fill(color.BLACK)
        pygame.display.flip()

    def event_update(self, event):
        pass

class Player:
    def __init__(self, hp, screen):
        self.player_color = (50, 200, 255)
        self.player_radius = 5
        self.posx = screen.WIDTH // 2
        self.posy = screen.HEIGHT // 2
        self.speed = 4
        self.hp = hp
    def update(self, screen):
        pygame.draw.circle(screen.screen, self.player_color, (int(self.posx), int(self.posy)), self.player_radius)
                
                
        #플레이어 이동
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.speed
        new_x = self.posx + dx
        new_y = self.posy + dy
                
        #맵 경계선충돌 판정
        if math.hypot(new_x - screen.WIDTH // 2, new_y - screen.HEIGHT // 2) <= 250 - self.player_radius:
            self.posx = new_x
            self.posy = new_y

        

class GameState:
    def update(self, screen):
        pass
    def event_update(self, event):
        pass

class Playeralive(GameState):
    def __init__(self, screen):
        self.player = Player(1, screen)
        self.arrow_manager = ArrowManager(pygame.time.get_ticks())
    def update(self, screen, arrow_mode):
        self.player.update(screen)
        self.arrow_manager.update(screen, self.player)
        for arrow in self.arrow_manager.arrow_generator.arrows:
            if self.IsArrow_collision(self.player.posx, self.player.posy, self.player.player_radius, arrow.rect):
                arrow_mode.state = PlayerDie(screen)
    def IsArrow_collision(self, player_posx, player_posy,radius, rect):
        closest_x = max(rect.left, min(player_posx, rect.right))
        closest_y = max(rect.top, min(player_posy, rect.bottom))

        distance = math.hypot(
            player_posx - closest_x,
            player_posy - closest_y
        )

        return distance <= radius
     
    def event_update(self, event):
        pass




class PlayerDie(GameState):
    def __init__(self, screen):
        self.game_over_txt = font.malgunbd.render("Game Over", True, (255, 80, 80))
        def go_main():
            screen.state = main_menu(screen)
        self.go_main_btn = Button("Go main", (screen.WIDTH / 2 - self.game_over_txt.get_width()/2, screen.HEIGHT/2 +25), (self.game_over_txt.get_width(), 50), go_main)
    def update(self, screen, arrow_mode):
        screen.screen.blit(self.game_over_txt, (screen.WIDTH // 2 - self.game_over_txt.get_width()/ 2, screen.HEIGHT // 2 - self.game_over_txt.get_height()/2))
        self.go_main_btn.update(screen)

    def event_update(self, event):
        self.go_main_btn.isClicked(event)

class Screen:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("죽림고수 - 모드 선택")

        self.state = main_menu(self)

    def update(self):
        self.state.update(self)

    def event_update(self, event):
        self.state.event_update(event)




screen = Screen()


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.event_update(event)
    screen.update()
    pygame.display.flip()
    clock.tick(60)
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