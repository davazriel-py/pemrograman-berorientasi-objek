import pygame
import sys
import os
import math
import random

SCREEN_W, SCREEN_H = 420, 680
FPS            = 60
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR      = os.path.join(BASE_DIR, "assets")
PLAYER_TARGET_W = 110
FISH_TARGET_W  = 84
BOMB_TARGET_W   = 84
PLAYER_EAT_FILE = "playereat.png"
PLAYER_EAT_ANIM_FRAMES = 10
EAT_SOUND_FILE  = "nyam.mp3"
GAME_OVER_SOUND_FILE = "gameover.mp3"
SKY_FILE         = "sky.jpg"
GROUND_TARGET_H = 95
GROUND_FILE     = "ground.png"
HEART_TARGET_W  = 28
HEART_FILE      = "heart.png"

C_WHITE  = (255, 255, 255)
C_BLACK  = (0,   0,   0)

PLAYER_SPEED        = 10
FISH_BASE_SPEED    = 4
FISH_MAX_SPEED     = 12
FISH_SPEED_STEP    = 1.2
FISH_SPEEDUP_EVERY = FPS * 10
BOMB_BASE_SPEED     = 4
BOMB_MAX_SPEED      = 12
BOMB_SPEED_STEP     = 1.2
BOMB_SPEEDUP_EVERY  = FPS * 10
SPAWN_BASE_INTERVAL = 66
SPAWN_MIN_INTERVAL  = 30
SPAWN_INTERVAL_STEP = 6
SPAWN_SPEEDUP_EVERY = FPS * 10
BOMB_SPAWN_CHANCE   = 0.17
MAX_MISS            = 3
PLAYER_HITBOX_SHRINK_X = 0.34
PLAYER_HITBOX_SHRINK_Y = 0.22
BOMB_HITBOX_SHRINK_X   = 0.56
BOMB_HITBOX_SHRINK_Y   = 0.56
FISH_HITBOX_SHRINK_X  = 0.28
FISH_HITBOX_SHRINK_Y  = 0.28

class GameObject:
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.image  = image
        self.width  = image.get_width()
        self.height = image.get_height()
        self.x      = x
        self.y      = y

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))


class Player(GameObject):
    def __init__(self, image: pygame.Surface, eat_image: pygame.Surface | None = None):
        x = SCREEN_W // 2 - image.get_width()  // 2
        y = SCREEN_H - image.get_height() - 50
        super().__init__(x, y, image)

        self.normal_image = image
        self.eat_image = eat_image if eat_image is not None else image
        self.eat_anim_timer = 0
        self.speed = PLAYER_SPEED
        self.score = 0
        self.miss  = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        self.x = max(0, min(SCREEN_W - self.width, self.x))

    def trigger_eat_animation(self, duration_frames: int = PLAYER_EAT_ANIM_FRAMES):
        self.eat_anim_timer = max(1, duration_frames)
        self.image = self.eat_image

    def update_animation(self):
        if self.eat_anim_timer > 0:
            self.eat_anim_timer -= 1
            if self.eat_anim_timer == 0:
                self.image = self.normal_image


class Fish(GameObject):
    def __init__(self, image: pygame.Surface, x: int, speed: float = FISH_BASE_SPEED):
        y = -image.get_height()
        super().__init__(x, y, image)

        self.speed  = speed
        self.active = True
        self.angle = random.uniform(0, 360)
        self.rotate_speed = 0.8

    def update(self):
        self.y += self.speed
        self.angle = (self.angle + self.rotate_speed) % 360

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_H

    def draw(self, surface: pygame.Surface):
        rotated = pygame.transform.rotozoom(self.image, self.angle, 1.0)
        center = (self.x + self.width // 2, self.y + self.height // 2)
        rect = rotated.get_rect(center=center)
        surface.blit(rotated, rect.topleft)


class Bomb(GameObject):
    def __init__(self, image: pygame.Surface, x: int, speed: float = BOMB_BASE_SPEED):
        y = -image.get_height()
        super().__init__(x, y, image)

        self.speed  = speed
        self.active = True

    def update(self):
        self.y += self.speed

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_H


def draw_background(surface: pygame.Surface, ground_img=None, sky_img=None):
    ground_h = ground_img.get_height() if ground_img else GROUND_TARGET_H
    ground_y = SCREEN_H - ground_h

    if sky_img is not None:
        surface.blit(sky_img, (0, 0))

    if ground_img:
        for x in range(0, SCREEN_W, ground_img.get_width()):
            surface.blit(ground_img, (x, ground_y))
    else:
        pygame.draw.rect(surface, (101, 67, 33), (0, ground_y, SCREEN_W, ground_h))
        pygame.draw.rect(surface, (80, 160, 45), (0, ground_y, SCREEN_W, 16))
        for gx in range(8, SCREEN_W, 20):
            pygame.draw.ellipse(surface, (55, 130, 30),
                                (gx, ground_y - 6, 14, 10))

def draw_hud(surface, player: Player, heart_img: pygame.Surface,
             font_med, font_sm):
    panel = pygame.Surface((SCREEN_W, 54), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 110))
    surface.blit(panel, (0, 0))

    score_txt = font_med.render(f"Skor: {player.score}", True, C_WHITE)
    surface.blit(score_txt, (12, 10))

    lives = MAX_MISS - player.miss
    for i in range(MAX_MISS):
        hx = SCREEN_W - 38 - i * 36
        if i < lives:
            surface.blit(heart_img, (hx, 12))
        else:
            grey = heart_img.copy()
            grey.fill((80, 80, 80, 160), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(grey, (hx, 12))

def load_image_scaled(name: str, target_w: int) -> pygame.Surface:
    img = pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha()
    w, h = img.get_size()
    if w == 0 or h == 0:
        return img
    scale = target_w / w
    target_h = max(1, int(h * scale))
    return pygame.transform.smoothscale(img, (target_w, target_h))


def load_fish_images(target_w: int) -> list[pygame.Surface]:
    fish_names = sorted(
        file_name
        for file_name in os.listdir(ASSET_DIR)
        if file_name.lower().startswith("fish") and file_name.lower().endswith(".png")
    )

    fish_images = [load_image_scaled(name, target_w) for name in fish_names]

    if not fish_images:
        fish_images.append(load_image_scaled("fish.png", target_w))

    return fish_images


def load_heart_image(name: str, target_w: int):
    path = os.path.join(ASSET_DIR, name)
    if not os.path.exists(path):
        return None

    img = pygame.image.load(path).convert_alpha()
    bbox = img.get_bounding_rect(min_alpha=1)
    if bbox.width > 0 and bbox.height > 0:
        img = img.subsurface(bbox).copy()

    w, h = img.get_size()
    if w == 0 or h == 0:
        return None

    scale = target_w / w
    target_h = max(1, int(h * scale))
    return pygame.transform.smoothscale(img, (target_w, target_h))


def load_ground_image(name: str, target_h: int):
    path = os.path.join(ASSET_DIR, name)
    if not os.path.exists(path):
        return None

    img = pygame.image.load(path).convert_alpha()
    bbox = img.get_bounding_rect(min_alpha=1)
    if bbox.width > 0 and bbox.height > 0:
        img = img.subsurface(bbox).copy()

    w, h = img.get_size()
    if w == 0 or h == 0:
        return None

    scale = target_h / h
    target_w = max(1, int(w * scale))
    return pygame.transform.smoothscale(img, (target_w, target_h))


def load_sky_image(name: str, target_size: tuple[int, int]):
    path = os.path.join(ASSET_DIR, name)
    if not os.path.exists(path):
        return None

    try:
        img = pygame.image.load(path).convert_alpha()
    except pygame.error:
        return None

    return pygame.transform.smoothscale(img, target_size)


def load_sound(name: str):
    path = os.path.join(ASSET_DIR, name)
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None


def shrink_rect(rect: pygame.Rect, shrink_x: float, shrink_y: float) -> pygame.Rect:
    dx = int(rect.width * shrink_x)
    dy = int(rect.height * shrink_y)
    dx = max(0, min(dx, rect.width - 2))
    dy = max(0, min(dy, rect.height - 2))
    return rect.inflate(-dx, -dy)


def screen_start(surface, clock, player_img, fish_imgs, bomb_img,
                 ground_img, sky_img, font_big, font_med, font_sm):
    tick = 0
    while True:
        tick += 1
        draw_background(surface, ground_img, sky_img)

        title = font_big.render("Catch the Fish!", True, (200, 50, 30))
        surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 75))
        bob = int(math.sin(tick * 0.05) * 8)
        fish_preview = fish_imgs[(tick // 25) % len(fish_imgs)]
        surface.blit(fish_preview,  (60,  175 + bob))
        surface.blit(player_img, (SCREEN_W // 2 - player_img.get_width() // 2, 160))
        surface.blit(bomb_img,   (SCREEN_W - 150, 175 + bob))

        lines = [
            ("<-  -> / A D  :  Gerak",          (50,  50,  50)),
            (f"Tangkap ikan  =  +1 skor",     (20, 120,  20)),
            (f"Miss {MAX_MISS}x ikan  =  Game Over", (180,  40,  40)),
            ("Kena bom  =  Game Over",         (180,  40,  40)),
        ]
        for i, (txt, col) in enumerate(lines):
            r = font_sm.render(txt, True, col)
            surface.blit(r, (SCREEN_W // 2 - r.get_width() // 2, 308 + i * 34))

        if (tick // 30) % 2 == 0:
            s = font_med.render("[ ENTER ]  Mulai", True, (40, 40, 180))
            surface.blit(s, (SCREEN_W // 2 - s.get_width() // 2, 465))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def screen_game_over(surface, clock, score: int, reason: str,
                     high_score: int, is_new_high: bool,
                     ground_img, sky_img, font_big, font_med, font_sm) -> bool:
    tick = 0
    while True:
        tick += 1
        draw_background(surface, ground_img, sky_img)

        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 145))
        surface.blit(ov, (0, 0))

        if is_new_high:
            new_label = font_sm.render("NEW HIGH SCORE!", True, (255, 235, 90))
            surface.blit(new_label, (SCREEN_W // 2 - new_label.get_width() // 2, 140))

        for txt, y in [
            (font_big.render("GAME OVER",             True, (230, 40,  40)), 176),
            (font_med.render(reason,                   True, (255, 210, 80)), 252),
            (font_med.render(f"Skor : {score}",       True, C_WHITE), 306),
            (font_med.render(f"High Score : {high_score}", True, (220, 235, 255)), 340),
        ]:
            surface.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, y))

        if (tick // 30) % 2 == 0:
            for txt, col, y in [
                ("[ ENTER ]  Main Lagi", (160, 255, 160), 398),
                ("[ ESC ]    Keluar",    (255, 160, 160), 438),
            ]:
                r = font_sm.render(txt, True, col)
                surface.blit(r, (SCREEN_W // 2 - r.get_width() // 2, y))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return True
                if event.key == pygame.K_ESCAPE: return False


def run_game(surface, clock, player_img, player_eat_img, fish_imgs, bomb_img,
             heart_img, ground_img, sky_img, font_med, font_sm,
             eat_sound=None, game_over_sound=None) -> tuple:

    player = Player(player_img, player_eat_img)  # 1 objek Player
    fishes: list = []                           # list objek FISH aktif
    bombs: list = []                            # list objek Bomb  aktif

    spawn_timer         = 0
    spawn_interval      = SPAWN_BASE_INTERVAL
    spawn_speedup_timer = 0
    fish_speedup_timer = 0
    bomb_speedup_timer  = 0
    fish_speed         = FISH_BASE_SPEED
    bomb_speed          = BOMB_BASE_SPEED
    game_over_reason = ""
    running        = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_over_reason = "Keluar manual"
                running = False

        fish_speedup_timer += 1
        if fish_speedup_timer >= FISH_SPEEDUP_EVERY:
            fish_speedup_timer = 0
            fish_speed = min(FISH_MAX_SPEED, fish_speed + FISH_SPEED_STEP)

        bomb_speedup_timer += 1
        if bomb_speedup_timer >= BOMB_SPEEDUP_EVERY:
            bomb_speedup_timer = 0
            bomb_speed = min(BOMB_MAX_SPEED, bomb_speed + BOMB_SPEED_STEP)

        spawn_speedup_timer += 1
        if spawn_speedup_timer >= SPAWN_SPEEDUP_EVERY:
            spawn_speedup_timer = 0
            spawn_interval = max(SPAWN_MIN_INTERVAL, spawn_interval - SPAWN_INTERVAL_STEP)

        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0

            if random.random() < BOMB_SPAWN_CHANCE:
                bx = random.randint(10, SCREEN_W - bomb_img.get_width() - 10)
                bombs.append(Bomb(bomb_img, bx, bomb_speed))
            else:
                fish_img = random.choice(fish_imgs)
                fx = random.randint(10, SCREEN_W - fish_img.get_width() - 10)
                fishes.append(Fish(fish_img, fx, fish_speed))

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update_animation()

        p_rect = shrink_rect(
            player.get_rect(),
            PLAYER_HITBOX_SHRINK_X,
            PLAYER_HITBOX_SHRINK_Y
        )

        for fish in fishes[:]:
            fish.update()

            catch_zone = pygame.Rect(
                player.x - 6, player.y,
                player.width + 12, player.height // 2
            )

            fish_hitbox = shrink_rect(
                fish.get_rect(),
                FISH_HITBOX_SHRINK_X,
                FISH_HITBOX_SHRINK_Y
            )
            if fish.active and catch_zone.colliderect(fish_hitbox):
                # Buah tertangkap
                player.score += 1
                player.trigger_eat_animation()
                if eat_sound is not None:
                    eat_sound.play()
                fish.active = False
                fishes.remove(fish)
                continue

            if fish.is_off_screen():
                player.miss += 1
                fishes.remove(fish)
                if player.miss >= MAX_MISS:
                    game_over_reason = f"Fish lolos {MAX_MISS}x  \U0001f494"
                    if game_over_sound is not None:
                        game_over_sound.play()
                    running = False
                    break

        for bomb in bombs[:]:
            bomb.update()

            bomb_hitbox = shrink_rect(
                bomb.get_rect(),
                BOMB_HITBOX_SHRINK_X,
                BOMB_HITBOX_SHRINK_Y
            )
            if bomb.active and p_rect.colliderect(bomb_hitbox):
                game_over_reason = "Kena Bom! \U0001f4a3"
                if game_over_sound is not None:
                    game_over_sound.play()
                running = False
                break

            if bomb.is_off_screen():
                bombs.remove(bomb)

        draw_background(surface, ground_img, sky_img)

        for fish in fishes:
            fish.draw(surface)

        for bomb in bombs:
            bomb.draw(surface)

        player.draw(surface)

        draw_hud(surface, player, heart_img, font_med, font_sm)

        pygame.display.flip()

    return player.score, game_over_reason


def main():
    pygame.init()
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error:
        pass

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Catch the FISH")
    clock = pygame.time.Clock()


    player_img = load_image_scaled("player.png", PLAYER_TARGET_W)
    player_eat_img = load_image_scaled(PLAYER_EAT_FILE, PLAYER_TARGET_W)
    if player_eat_img.get_size() != player_img.get_size():
        player_eat_img = pygame.transform.smoothscale(player_eat_img, player_img.get_size())
    fish_imgs = load_fish_images(FISH_TARGET_W)
    bomb_img   = load_image_scaled("bomb.png", BOMB_TARGET_W)
    sky_img    = load_sky_image(SKY_FILE, (SCREEN_W, SCREEN_H))
    ground_img = load_ground_image(GROUND_FILE, GROUND_TARGET_H)
    heart_img  = load_heart_image(HEART_FILE, HEART_TARGET_W)
    eat_sound  = load_sound(EAT_SOUND_FILE)
    game_over_sound = load_sound(GAME_OVER_SOUND_FILE)

    font_big = pygame.font.SysFont("comicsansms", 40, bold=True)
    font_med = pygame.font.SysFont("comicsansms", 26, bold=True)
    font_sm  = pygame.font.SysFont("comicsansms", 20)
    high_score = 0

    screen_start(screen, clock, player_img, fish_imgs, bomb_img,
                 ground_img, sky_img, font_big, font_med, font_sm)

    while True:
        score, reason = run_game(screen, clock, player_img, player_eat_img, fish_imgs,
                                 bomb_img, heart_img, ground_img, sky_img,
                                 font_med, font_sm, eat_sound, game_over_sound)
        is_new_high = score > high_score
        if is_new_high:
            high_score = score
        play_again = screen_game_over(screen, clock, score, reason,
                                      high_score, is_new_high,
                                      ground_img, sky_img, font_big, font_med, font_sm)
        if not play_again:
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()