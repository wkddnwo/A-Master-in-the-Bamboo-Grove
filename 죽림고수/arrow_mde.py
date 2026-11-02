import pygame
import sys
import math

pygame.init()
font = pygame.font.SysFont(None, 36)


# 화면 설정
WIDTH, HEIGHT = 600, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("죽림고수 회피 게임")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (50, 200, 255)
ARROW_COLOR = (255, 60, 60)
MAP_COLOR = (30, 30, 30)
BUTTON_COLOR = (80, 80, 80)
BUTTON_HOVER = (120, 120, 120)



class Arrow:
    def __init__(self, pos, target_pos):
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        dist = math.hypot(dx, dy)
        self.vel = [dx / dist * 3.5, dy / dist * 3.5]
        self.pos = list(pos)
        self.size = (4, 12)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def draw(self, screen):
        angle = math.atan2(self.vel[1], self.vel[0])
        surf = pygame.Surface(self.size)
        surf.fill(ARROW_COLOR)
        surf.set_colorkey(BLACK)
        rot_image = pygame.transform.rotate(surf, -math.degrees(angle))
        rect = rot_image.get_rect(center=self.pos)
        screen.blit(rot_image, rect)

    def get_rect(self):
        return pygame.Rect(self.pos[0] - 2, self.pos[1] - 6, 4, 12)

def draw_restart_button():
    text = font.render("go main", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50)
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR, button_rect)
    screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
    return button_rect

player_pos = [CENTER[0], CENTER[1]]


def spawn_arrow_toward_player():
    angle = math.atan2(player_pos[1] - CENTER[1], player_pos[0] - CENTER[0])
    spawn_x = CENTER[0] + math.cos(angle + (math.pi)) * (RADIUS + 40)
    spawn_y = CENTER[1] + math.sin(angle + (math.pi)) * (RADIUS + 40)
    arrows.append(Arrow((spawn_x, spawn_y), player_pos[:]))

def spawn_pattern_arrows():
    for i in range(10):
        angle = i * (2 * math.pi / 10)
        x = CENTER[0] + math.cos(angle) * (RADIUS + 40)
        y = CENTER[1] + math.sin(angle) * (RADIUS + 40)
        arrows.append(Arrow((x, y), player_pos[:]))

def run_arrow_mode(best_time = 0):
    player_radius = 5
    global arrows, player_pos, start_ticks, game_over
    global pattern_timer, basic_arrow_timer
    arrows = []
    player_pos[:] = CENTER[:]
    start_ticks = pygame.time.get_ticks()
    pattern_timer = start_ticks + 5000
    basic_arrow_timer = start_ticks
    game_over = False
    while True:
        dt = clock.tick(60)
        screen.fill(BLACK)
        pygame.draw.circle(screen, MAP_COLOR, CENTER, RADIUS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if draw_restart_button().collidepoint(event.pos):
                    return best_time

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
            if math.hypot(new_x - CENTER[0], new_y - CENTER[1]) <= RADIUS - player_radius:
                player_pos[0] = new_x
                player_pos[1] = new_y

            # 기본 화살 생성 (0.5초마다 1개)
            current_time = pygame.time.get_ticks()
            if current_time - basic_arrow_timer >= 500:
                spawn_arrow_toward_player()
                basic_arrow_timer = current_time

            # 패턴 화살 (5초 후, 이후 3초마다)
            if current_time >= pattern_timer:
                spawn_pattern_arrows()
                pattern_timer += 3000

            # 화살 업데이트
            for arrow in arrows:
                arrow.update()
                if arrow.get_rect().colliderect(
                    pygame.Rect(player_pos[0] - player_radius, player_pos[1] - player_radius, player_radius * 2, player_radius * 2)
                ):
                    game_over = True
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
                    best_time = max(best_time, elapsed_time)

            # 시간 표시
            elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
            screen.blit(font.render(f"Time: {elapsed_time}", True, WHITE), (20, 20))
            screen.blit(font.render(f"Best: {best_time}", True, WHITE), (20, 50))

            for arrow in arrows:
                arrow.draw(screen)

            pygame.draw.circle(screen, PLAYER_COLOR, (int(player_pos[0]), int(player_pos[1])), player_radius)

        else:
            screen.blit(font.render("Game Over", True, (255, 80, 80)), (WIDTH // 2 - 80, HEIGHT // 2 - 30))
            draw_restart_button()
            screen.blit(font.render(f"Best Time: {best_time}", True, WHITE), (WIDTH // 2 - 90, HEIGHT // 2 + 100))

        pygame.display.flip()


if __name__ == "__main__":
    run_arrow_mode()