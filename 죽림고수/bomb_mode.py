import pygame
import sys
import math
import random


pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("죽림고수 - 보스모드")
clock = pygame.time.Clock()

#이미지 불러오기

#위험 표시
danger_sign = [pygame.image.load("danger_sign.png"),
               pygame.image.load("danger_sign1.png"),
               pygame.image.load("danger_sign2.png"),
               pygame.image.load("danger_sign3.png")]
disappeared_area = [pygame.image.load("disappeared_area.png"),
                    pygame.image.load("disappeared_area1.png"),
                    pygame.image.load("disappeared_area2.png"),
                    pygame.image.load("disappeared_area3.png")]

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (50, 200, 255)
MAP_COLOR = (30, 30, 30)
BOMB_COLOR = (255, 100, 0)
EXPLOSION_COLOR = (255, 200, 50)

font = pygame.font.SysFont("malgungothic", 28, bold=True)

player_radius = 5
player_hp = 3
max_time = 30

class Bomb:
    def __init__(self, pos, target):
        dx, dy = target[0] - pos[0], target[1] - pos[1]
        dist = math.hypot(dx, dy)
        self.vel = [dx / dist * 5.5, dy / dist * 5.5]
        self.pos = list(pos)
        self.acc = 0.98
        self.timer = 0
        self.exploded = False
        self.explode_time = 0

    def update(self, dt):
        if not self.exploded:
            self.timer += dt
            self.vel[0] *= self.acc
            self.vel[1] *= self.acc
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            if self.timer >= 3000:  # 3초 후 폭발
                self.exploded = True
                self.explode_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - self.explode_time > 1000:
                return False  # 제거
        return True

    def draw(self):
        if self.exploded:
            pygame.draw.circle(screen, EXPLOSION_COLOR, (int(self.pos[0]), int(self.pos[1])), 30)
        else:
            pygame.draw.circle(screen, BOMB_COLOR, (int(self.pos[0]), int(self.pos[1])), 6)

    def get_rect(self):
        return pygame.Rect(self.pos[0] - 6, self.pos[1] - 6, 12, 12)

    def get_explosion_rect(self):
        return pygame.Rect(self.pos[0] - 30, self.pos[1] - 30, 60, 60)

def reset():
    global player_pos, bombs, player_hp, start_time, game_over, win, bomb_timer, pattern1_timer,well_be_del_area
    player_pos = list(CENTER)
    bombs = []
    player_hp = 3
    start_time = pygame.time.get_ticks()
    game_over = False
    win = False
    bomb_timer = 0
    pattern1_timer = 0
    well_be_del_area = random.randint(0, 3)

def spawn_bomb():
    angle = math.radians(pygame.time.get_ticks() % 360)
    x = CENTER[0] + math.cos(angle) * (RADIUS + 40)
    y = CENTER[1] + math.sin(angle) * (RADIUS + 40)
    bombs.append(Bomb((x, y), player_pos))

def spawn_pattern1():
    num_bombs = 12
    for i in range(num_bombs):
        angle = math.radians(i * (360 / num_bombs))
        x = CENTER[0] + math.cos(angle) * (RADIUS + 40)
        y = CENTER[1] + math.sin(angle) * (RADIUS + 40)
        bombs.append(Bomb((x, y), player_pos))

reset()

bomb_timer = 0
pattern1_timer = 0
pattern1_interval = 5000  # 5초마다 발동





# 지형 삭제

where_is_del_area = [[WIDTH / 2 - RADIUS, HEIGHT / 2 - RADIUS],
                     [WIDTH / 2, HEIGHT / 2 - RADIUS],
                     [WIDTH / 2 - RADIUS, HEIGHT / 2],
                     [WIDTH / 2, HEIGHT / 2]]

def remove_area(now_time, well_be_del_area):
    start = 12
    start = start * 1000

    if now_time > 3000 + start:
        screen.blit(disappeared_area[well_be_del_area], where_is_del_area[well_be_del_area])
        return well_be_del_area
    else:
        for i in range(0  + start, 3001 + start, 1000):
            if now_time > i and now_time < i+500:
                screen.blit(danger_sign[well_be_del_area], where_is_del_area[well_be_del_area])
                return -1




#삭제된 지역 충돌 처리
def is_not_remove_area(new_x, new_y, what_is_area_del):
    if what_is_area_del == 0: #제2사분면
        if new_x < WIDTH / 2 and new_y < HEIGHT /2:
            return False # 제 1사분면
    elif what_is_area_del == 1:
        if new_x > WIDTH / 2 and new_y < HEIGHT /2:
            return False
    elif what_is_area_del == 2:#제 3사분면
        if new_x < WIDTH / 2 and new_y > HEIGHT /2:
            return False
    elif what_is_area_del == 3: #제4사분면
        if new_x > WIDTH / 2 and new_y > HEIGHT /2:
            return False
            
    return True

def run_bomb_mode():
    what_is_area_del = -1
    well_be_del_area = random.randint(0, 3)

    global player_pos, bombs, player_hp, start_time, game_over, win, bomb_timer, pattern1_timer
    player_pos = list(CENTER)
    bombs = []
    player_hp = 3
    start_time = pygame.time.get_ticks()
    game_over = False
    win = False
    bomb_timer = 0
    pattern1_timer = 0
    well_be_del_area = random.randint(0, 3)
    while True:
        dt = clock.tick(60)
        screen.fill(BLACK)
        pygame.draw.circle(screen, MAP_COLOR, CENTER, RADIUS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                return

        if not game_over:
            # 이동
            keys = pygame.key.get_pressed()
            dx = dy = 0
            speed = 4
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = speed

            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy
            if math.hypot(new_x - CENTER[0], new_y - CENTER[1]) <= RADIUS - player_radius and is_not_remove_area(new_x, new_y, what_is_area_del):
                #math.hypot(new_x - CENTER[0], new_y - CENTER[1])가 원 플레이어와 중심사이의 최단거리를 구함 이 값이 반지름 - 플레이어 반지름 이 넘지 않도록 하는것임
                #즉 플레이어가 원 중심으로부터 얼마나 떨어졌는지 확인하는 것임
                player_pos[0] = new_x
                player_pos[1] = new_y

            

            # 폭탄 생성 (기본)
            bomb_timer += dt
            if bomb_timer >= 500:
                spawn_bomb()
                bomb_timer = 0

            # 패턴1 생성
            pattern1_timer += dt
            if pattern1_timer >= pattern1_interval:
                spawn_pattern1()
                pattern1_timer = 0

            #폭탄 업데이트 및 충돌 처리
            for bomb in bombs[:]:
                alive = bomb.update(dt)
                if not alive:
                    bombs.remove(bomb)
                    continue

                if not bomb.exploded:
                    if bomb.get_rect().colliderect(
                        pygame.Rect(player_pos[0] - player_radius, player_pos[1] - player_radius, player_radius * 2, player_radius * 2)):
                        # 직격 시 즉사
                        player_hp = 0
                        game_over = True
                        break
                else:
                    if bomb.get_explosion_rect().colliderect(
                        pygame.Rect(player_pos[0] - player_radius, player_pos[1] - player_radius, player_radius * 2, player_radius * 2)):
                        player_hp -= 1
                        bombs.remove(bomb)
                        if player_hp <= 0:
                            game_over = True
                        break

            # 남은 시간 계산
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
            remain = max(0, max_time - elapsed)
            if remain == 0:
                win = True
                game_over = True

            # 그리기


            #사라지는 지역 처리
            what_is_area_del = remove_area(pygame.time.get_ticks() - start_time, well_be_del_area) #지형 삭제
            if is_not_remove_area(player_pos[0], player_pos[1],what_is_area_del) == False: #삭제된 지역으로 들어가있으면 죽임(삭제 될때까지 뻐긴 경우)
                game_over = True



            for bomb in bombs:
                bomb.draw()
            pygame.draw.circle(screen, PLAYER_COLOR, (int(player_pos[0]), int(player_pos[1])), player_radius)
            screen.blit(font.render(f"HP: {player_hp}", True, WHITE), (20, 20))
            screen.blit(font.render(f"남은 시간: {remain}", True, WHITE), (20, 50))
            
        else:
            msg = "클리어!" if win else "Game Over"
            screen.blit(font.render(msg, True, (255, 80, 80)), (WIDTH // 2 - 80, HEIGHT // 2 - 30))
            screen.blit(font.render("클릭해서 메인으로", True, WHITE), (WIDTH // 2 - 120, HEIGHT // 2 + 30))

        pygame.display.flip()


if __name__ == "__main__":
    run_bomb_mode()