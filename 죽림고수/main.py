import pygame
import math
from disapear import DelAreaManager
import random
from pathlib import Path
import json



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
        
        self.state = Playeralive_arrow_mode(screen)
    def update(self, screen):
        #맵 그리기
        screen.screen.fill(color.BLACK)
        pygame.draw.circle(screen.screen, (30, 30, 30), (screen.WIDTH // 2, screen.HEIGHT // 2), 250)
        
        
        self.state.update(screen, self)
        
    
    def event_update(self, event):
        self.state.event_update(event)

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

        self.state = Playeralive_boom_mode(screen)

    def update(self, screen):
        screen.screen.fill(color.BLACK)
        pygame.draw.circle(screen.screen, (30, 30, 30), (screen.WIDTH // 2, screen.HEIGHT // 2), 250)
        
        self.state.update(screen, self)
        

    def event_update(self, event):
        self.state.event_update(event)



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
                
                
        
        

class GameState:
    def update(self, screen):
        pass
    def event_update(self, event):
        pass

class Playeralive_arrow_mode(GameState):
    def __init__(self, screen):
        self.player = Player(1, screen)
        self.arrow_manager = ArrowManager(pygame.time.get_ticks())
        self.start_ticks = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, 36)
    def update(self, screen, arrow_mode):
        self.player.update(screen)
        self.arrow_manager.update(screen, self.player)
        #플레이어 이동
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.player.speed
        new_x = self.player.posx + dx
        new_y = self.player.posy + dy
                
        #맵 경계선충돌 판정
        if math.hypot(new_x - screen.WIDTH // 2, new_y - screen.HEIGHT // 2) <= 250 - self.player.player_radius:
            self.player.posx = new_x
            self.player.posy = new_y



        #화살 충돌판정
        for arrow in self.arrow_manager.arrow_generator.arrows:
            if self.IsArrow_collision(self.player.posx, self.player.posy, self.player.player_radius, arrow.rect):
                if (pygame.time.get_ticks() - self.start_ticks) / 1000 > screen.save.best_time:
                    screen.save.best_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
                    screen.save.update()
                arrow_mode.state = PlayerDie_arrow_mode(screen)

        screen.screen.blit(self.font.render(f"Time: {(pygame.time.get_ticks() - self.start_ticks) // 1000}", True, color.WHITE), (20, 20))
        screen.screen.blit(self.font.render(f"Best: {screen.save.best_time}", True, color.WHITE), (20, 50))
        
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





class PlayerDie_arrow_mode(GameState):
    def __init__(self, screen):
        self.game_over_txt = font.malgunbd.render("Game Over", True, (255, 80, 80))
        self.best_time_txt = font.malgunbd.render(f"Best time: {screen.save.best_time}",True, color.WHITE)
        def go_main():
            screen.state = main_menu(screen)
        self.go_main_btn = Button("Go main", (screen.WIDTH / 2 - self.game_over_txt.get_width()/2, screen.HEIGHT/2 +25), (self.game_over_txt.get_width(), 50), go_main)
    def update(self, screen, arrow_mode):
        screen.screen.blit(self.game_over_txt, (screen.WIDTH // 2 - self.game_over_txt.get_width()/ 2, screen.HEIGHT // 2 - self.game_over_txt.get_height()/2))
        self.go_main_btn.update(screen)
        screen.screen.blit(self.best_time_txt, (screen.WIDTH // 2 - self.game_over_txt.get_width()/ 2, screen.HEIGHT // 2 - self.game_over_txt.get_height()/2 + 100))

    def event_update(self, event):
        self.go_main_btn.isClicked(event)

class Boom:
    def __init__(self, pos, target_pos):
        self.time_of_birth = pygame.time.get_ticks()

        self.posx = pos[0]
        self.posy = pos[1]
        target_posx = target_pos[0]
        target_posy = target_pos[1]
        dist = math.hypot(target_posx-self.posx, target_posy - self.posy)
        self.speed = 5.5
        self.frictional_force = 0.98
        self.dx = (target_posx - self.posx) / dist
        self.radius = 6
        self.dy = (target_posy - self.posy) / dist

        self.state = self.nomal_state
        
    def update(self, screen):
        self.state(screen)

    def nomal_state(self, screen):
        self.speed *= self.frictional_force
        self.posx += (self.dx * self.speed)
        self.posy += (self.dy * self.speed)
        pygame.draw.circle(screen.screen, (255, 100, 0), (int(self.posx), int(self.posy)), self.radius)
        if pygame.time.get_ticks() - self.time_of_birth >= 3000:
            self.radius = 30
            self.state = self.explosion_state

    def explosion_state(self, screen):
        pygame.draw.circle(screen.screen, (255, 200, 50), (int(self.posx), int(self.posy)), self.radius)

    def IsBoomDie(self):
        return pygame.time.get_ticks() - self.time_of_birth >= 4000





class Playeralive_boom_mode(GameState):
    def __init__(self, screen):
        self.font = pygame.font.SysFont(None, 36)
        self.player = Player(3, screen)
        self.boom_manager = BoomManager(pygame.time.get_ticks())
        self.start_time = pygame.time.get_ticks()
        self.player_last_hit = 0
        self.del_area_manager = DelAreaManager(random.randint(0, 3), pygame.time.get_ticks(), screen.screen)

    def update(self, screen, boom_mode):
        self.del_area_manager.update(screen.screen)
        self.boom_manager.update(screen, self.player)
        self.player.update(screen)

        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.player.speed
        new_x = self.player.posx + dx
        new_y = self.player.posy + dy
                
        #맵 경계선충돌 판정
        if math.hypot(new_x - 600 // 2, new_y - 600 // 2) <= 250 - self.player.player_radius:
            if not self.del_area_manager.Iscollision(self.player.player_radius, (new_x, new_y)):
                self.player.posx = new_x
                self.player.posy = new_y
        #플레이어 장외이탈 처리
        if self.del_area_manager.Iscollision(self.player.player_radius, (self.player.posx+self.player.speed, self.player.posy)) and self.del_area_manager.Iscollision(self.player.player_radius, (self.player.posx-self.player.speed, self.player.posy)):
            if self.del_area_manager.Iscollision(self.player.player_radius, (self.player.posx, self.player.posy+self.player.speed)) and self.del_area_manager.Iscollision(self.player.player_radius, (self.player.posx, self.player.posy-self.player.speed)):
                boom_mode.state = PlayerDie_boom_mode(screen)

        #플레이어 충돌처리
        if pygame.time.get_ticks() - self.player_last_hit >= 1500:
            for boom in self.boom_manager.boom_generator.booms:
                if self.IsBoomCollision((self.player.posx, self.player.posy), self.player.player_radius, (boom.posx, boom.posy), boom.radius):
                    self.player.hp -= 1
                    self.player_last_hit = pygame.time.get_ticks()
                    if self.player.hp <= 0:
                        boom_mode.state = PlayerDie_boom_mode(screen)
                    break
        


        #플레이어 우승여부 확인
        if pygame.time.get_ticks() - self.start_time >= 30000:
            boom_mode.state = PlayerWin_boom_mode(screen)


        #시간 HP 출력
        screen.screen.blit(self.font.render(f"HP: {self.player.hp}", True, color.WHITE), (20, 20))
        screen.screen.blit(self.font.render(f"Time: {(pygame.time.get_ticks() - self.start_time)//1000}", True, color.WHITE), (20, 50))
        
    def event_update(self, event):
        pass

    def IsBoomCollision(self, pos1, radius1, pos2, radius2):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]

        distance = math.hypot(dx, dy)

        return distance <= radius1 + radius2

class PlayerDie_boom_mode(GameState):
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

class PlayerWin_boom_mode(GameState):
    def __init__(self, screen):
        self.game_over_txt = font.malgunbd.render("You Win", True, (255, 80, 80))
        def go_main():
            screen.state = main_menu(screen)
        self.go_main_btn = Button("Go main", (screen.WIDTH / 2 - self.game_over_txt.get_width()/2, screen.HEIGHT/2 +25), (self.game_over_txt.get_width(), 50), go_main)
    def update(self, screen, arrow_mode):
        screen.screen.blit(self.game_over_txt, (screen.WIDTH // 2 - self.game_over_txt.get_width()/ 2, screen.HEIGHT // 2 - self.game_over_txt.get_height()/2))
        self.go_main_btn.update(screen)

    def event_update(self, event):
        self.go_main_btn.isClicked(event)


class BoomManager:
    def __init__(self, game_start_time):
        self.boom_generator = BoomGenerator(game_start_time)
    def update(self, screen, player):
        self.boom_generator.update(screen, player)
        for arrow in self.boom_generator.booms:
            arrow.update(screen)
        self.del_boom(screen)

    def del_boom(self, screen):
        self.boom_generator.booms = [boom for boom in self.boom_generator.booms if not boom.IsBoomDie()]


class BoomGenerator:
    def __init__(self, game_start_time):
        self.booms = []
        self.last_time = game_start_time
        self.last_time_special = game_start_time
        self.firing_cooldown = 500
        self.special_firing_cooldown = 5000
    def update(self, screen, player):
        if pygame.time.get_ticks() - self.last_time >= self.firing_cooldown :
            angle = math.atan2(player.posy - screen.HEIGHT // 2, player.posx - screen.WIDTH // 2)
            pos_x = screen.WIDTH // 2 + math.cos(angle + (math.pi)) * (250 + 40) #맵 지름에 40을 더함
            pos_y = screen.HEIGHT // 2 + math.sin(angle + (math.pi)) * (250 + 40)
            self.booms.append(Boom((pos_x, pos_y), (player.posx, player.posy)))
            self.last_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_time_special >= self.special_firing_cooldown:
            for i in range(12):
                angle = i * (2 * math.pi / 10)
                x = screen.WIDTH // 2 + math.cos(angle) * (250 + 40)#맵 지름에 40을 더함
                y = screen.HEIGHT // 2 + math.sin(angle) * (250 + 40)
                self.booms.append(Boom((x, y), (player.posx, player.posy)))
            self.last_time_special = pygame.time.get_ticks()
        



class Screen:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("죽림고수 - 모드 선택")
        self.save = Save()
        self.state = main_menu(self)

    def update(self):
        self.state.update(self)

    def event_update(self, event):
        self.state.event_update(event)


class Save:
    def __init__(self):
        self.file_addres = "죽림고수/save/save.json"
        file_path = Path(self.file_addres)

        if not file_path.exists():
            file_path.touch()
            with open(self.file_addres, "w", encoding="utf-8") as data:
                json.dump({
                    "best_time":0
                },data , ensure_ascii=False, indent=4)
        with open(self.file_addres, "r", encoding="utf-8") as save:
            data = json.load(save)
            self.best_time = data["best_time"]
    def update(self):
        with open(self.file_addres, "w", encoding="utf-8") as save:
            json.dump({
                "best_time":self.best_time
            }, save,  ensure_ascii=False, indent=4)

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