import pygame
import math


class DelAreaManager:
    def __init__(self, del_num, game_start_time, screen):
        self.del_num = del_num
        self.del_area = DelArea(del_num, screen)
        self.game_start_time = game_start_time
        self.state = Wait(game_start_time)
    def update(self, screen):
        self.state.update(self, screen)
    def Iscollision(self, player_radius, player_pos):
        return self.state.Iscollision(self.del_area, player_radius, player_pos)

class DelArea:
    def __init__(self, img_num, screen):
        self.danger_sin = pygame.image.load(f"죽림고수/danger_sign{img_num}.png")
        self.disappeard_area = pygame.image.load(f"죽림고수/disappeared_area{img_num}.png")
        pos_list = [
            (screen.get_width()/2-self.danger_sin.get_width(), screen.get_height()/2-self.danger_sin.get_height()),
            (screen.get_width()/2, screen.get_height()/2-self.danger_sin.get_height()),
            (screen.get_width()/2-self.danger_sin.get_width(), screen.get_height()/2),
            (screen.get_width()/2, screen.get_height()/2)
        ]
        self.posx = pos_list[img_num][0]
        self.posy = pos_list[img_num][1]
        self.rect = self.danger_sin.get_rect(topleft=(self.posx, self.posy))


class DelAreaState:
    def __init__(self):
        pass
    def update(self):
        pass
    def collision(self):
        pass

class Wait(DelAreaState):
    def __init__(self, game_start_time):
        self.game_start_time = game_start_time
    def update(self, delareamanager, screen):
        if pygame.time.get_ticks() - self.game_start_time >= 3000:
            delareamanager.state = Warning(delareamanager.del_area, pygame.time.get_ticks())
    def Iscollision(self, delarea, player_radius, player_pos):
        return False

class Warning(DelAreaState):
    def __init__(self, del_area, waring_start_time):
        self.del_area = del_area
        self.waring_start_time = waring_start_time
        self.state = Show()
    def update(self, delareamanager, screen):
        self.state.update(delareamanager, self ,screen)
        if pygame.time.get_ticks() - self.waring_start_time >= 3000:
            delareamanager.state = Disappear()
    def Iscollision(self, delarea, player_radius, player_pos):
        return False



class WaringState:
    def __init__(self):
        pass
    def update(self):
        pass

class Show(WaringState):
    def __init__(self):
        self.show_start_time = pygame.time.get_ticks()
    def update(self, delareamanager,waring, screen):
        screen.blit(delareamanager.del_area.danger_sin, delareamanager.del_area.rect)
        if pygame.time.get_ticks() - self.show_start_time >= 500:
            waring.state = Hide()
            pass
class Hide(WaringState):
    def __init__(self):
        self.hide_start_time = pygame.time.get_ticks()
    def update(self, delareamanager,waring, screen):
        if pygame.time.get_ticks() - self.hide_start_time >= 500:
            waring.state = Show()

class Disappear(DelAreaState):
    def __init__(self):
        pass
    def update(self, delareamanager, screen):
        screen.blit(delareamanager.del_area.disappeard_area, delareamanager.del_area.rect)
    def Iscollision(self, delarea, player_radius, player_pos):
        # 원의 중심 좌표
        # print("충돌함수 실행")
        cx, cy = player_pos

        # 원의 중심에서 가장 가까운 사각형 위의 점
        closest_x = max(delarea.rect.left, min(cx, delarea.rect.right))
        closest_y = max(delarea.rect.top, min(cy, delarea.rect.bottom))

        # 두 점 사이의 거리
        distance = math.hypot(cx - closest_x, cy - closest_y)

        # 거리가 반지름 이하라면 충돌
        return distance <= player_radius


class Player:
    def __init__(self, hp, screen):
        self.player_color = (50, 200, 255)
        self.player_radius = 5
        self.posx = 600 // 2
        self.posy = 600 // 2
        self.speed = 4
        self.hp = hp
    def update(self, screen):
        pygame.draw.circle(screen, self.player_color, (int(self.posx), int(self.posy)), self.player_radius)
                
                


    

if __name__ == "__main__":
    running = True
    screen = pygame.display.set_mode((600, 600))
    screen.get_width
    screen.get_height()
    clock = pygame.time.Clock()
    del_area_manager = DelAreaManager(0, pygame.time.get_ticks(), screen)
    player = Player(3, screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (30, 30, 30), (600 // 2, 600 // 2), 250)
        del_area_manager.update(screen)
        player.update(screen)

        #플레이어 이동
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = player.speed
        new_x = player.posx + dx
        new_y = player.posy + dy
                
        #맵 경계선충돌 판정
        if math.hypot(new_x - 600 // 2, new_y - 600 // 2) <= 250 - player.player_radius:
            if not del_area_manager.Iscollision(player.player_radius, (new_x, new_y)):
                player.posx = new_x
                player.posy = new_y
        #플레이어 장외이탈 처리
        if del_area_manager.Iscollision(player.player_radius, (player.posx+player.speed, player.posy)) and del_area_manager.Iscollision(player.player_radius, (player.posx-player.speed, player.posy)):
            if del_area_manager.Iscollision(player.player_radius, (player.posx, player.posy+player.speed)) and del_area_manager.Iscollision(player.player_radius, (player.posx, player.posy-player.speed)):
                player.hp -= 3
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()