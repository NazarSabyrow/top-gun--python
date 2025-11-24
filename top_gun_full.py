import pygame
import sys
import random
import math
from pygame import mixer

# PyGame инициализация
pygame.init()
mixer.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🎯 ТОП ГАН - БОЕВАЯ МИССИЯ 🚀")

# Цвета
BLUE_DARK = (10, 20, 100)
BLUE_LIGHT = (30, 60, 180)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (100, 255, 100)
RED = (255, 50, 50)
YELLOW = (255, 255, 100)
ORANGE = (255, 150, 50)
PURPLE = (180, 70, 250)
CYAN = (0, 255, 255)

# Создание простых звуковых эффектов (без numpy)
def create_beep_sound(frequency=440, duration=100):
    sample_rate = 44100
    n_samples = int(round(duration * 0.001 * sample_rate))
    sound_data = []
    max_amplitude = 32767
    
    for i in range(n_samples):
        t = i / sample_rate
        wave = int(max_amplitude * math.sin(2 * math.pi * frequency * t))
        sound_data.append((wave, wave))
    
    return pygame.sndarray.make_sound(pygame.array.array('h', [item for sublist in sound_data for item in sublist]))

# Шрифты
try:
    font_large = pygame.font.Font("freesansbold.ttf", 48)
    font_medium = pygame.font.Font("freesansbold.ttf", 36)
    font_small = pygame.font.Font("freesansbold.ttf", 24)
    font_tiny = pygame.font.Font("freesansbold.ttf", 18)
except:
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 18)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.width = 40
        self.height = 60
        self.speed = 6
        self.health = 100
        self.max_health = 100
        self.last_shot = 0
        self.shot_delay = 250
        self.special_weapon = 0
        self.invincible = 0
        self.score_multiplier = 1
        self.lives = 3
        
    def draw(self):
        if self.invincible > 0 and pygame.time.get_ticks() % 200 < 100:
            return  # Эффект мерцания
            
        # Улучшенный дизайн самолета
        # Основной корпус
        points = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width - 5, self.y + self.height - 10),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
            (self.x + 5, self.y + self.height - 10)
        ]
        pygame.draw.polygon(screen, GREEN, points)
        
        # Кабина
        pygame.draw.circle(screen, (150, 220, 255), 
                          (self.x + self.width // 2, self.y + 15), 10)
        pygame.draw.circle(screen, (200, 240, 255), 
                          (self.x + self.width // 2, self.y + 15), 6)
        
        # Крылья
        wing_points = [
            (self.x - 15, self.y + 25),
            (self.x + self.width + 15, self.y + 25),
            (self.x + self.width + 8, self.y + 35),
            (self.x - 8, self.y + 35)
        ]
        pygame.draw.polygon(screen, (50, 200, 50), wing_points)
        
        # Эффект огня - улучшенный
        flame_size = 8 + math.sin(pygame.time.get_ticks() * 0.02) * 3
        flame_points = [
            (self.x + self.width // 2 - 4, self.y + self.height),
            (self.x + self.width // 2 + 4, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height + flame_size)
        ]
        pygame.draw.polygon(screen, ORANGE, flame_points)
        pygame.draw.polygon(screen, YELLOW, [
            (self.x + self.width // 2 - 2, self.y + self.height),
            (self.x + self.width // 2 + 2, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height + flame_size - 3)
        ])
        
        # Индикатор специального оружия
        if self.special_weapon > 0:
            indicator_color = PURPLE if self.special_weapon > 1 else CYAN
            pygame.draw.circle(screen, indicator_color, 
                             (self.x + self.width // 2, self.y - 10), 5)
    
    def move(self, keys):
        speed = self.speed
        if keys[pygame.K_LSHIFT]:  # Быстрое движение
            speed = self.speed * 1.5
            
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += speed
            
        if self.invincible > 0:
            self.invincible -= 1
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_delay:
            bullets = []
            
            # Обычные пули
            bullets.append(Bullet(
                self.x + self.width // 2 - 2,
                self.y,
                True,
                "normal"
            ))
            
            # Боковые орудия (с уровня 2)
            if game.level >= 2:
                bullets.append(Bullet(
                    self.x + 8,
                    self.y + 20,
                    True,
                    "normal"
                ))
                bullets.append(Bullet(
                    self.x + self.width - 12,
                    self.y + 20,
                    True,
                    "normal"
                ))
            
            # Специальное оружие
            if self.special_weapon > 0:
                if self.special_weapon == 1:  # Лазер
                    bullets.append(Bullet(
                        self.x + self.width // 2 - 1,
                        self.y,
                        True,
                        "laser"
                    ))
                else:  # Ракета
                    bullets.append(Bullet(
                        self.x + self.width // 2 - 6,
                        self.y,
                        True,
                        "rocket"
                    ))
                    bullets.append(Bullet(
                        self.x + self.width // 2 + 4,
                        self.y,
                        True,
                        "rocket"
                    ))
                self.special_weapon -= 1
            
            game.bullets.extend(bullets)
            self.last_shot = current_time

class Enemy:
    def __init__(self, level):
        enemy_type = random.random()
        
        if enemy_type < 0.6:
            # Обычный враг
            self.x = random.randint(0, SCREEN_WIDTH - 35)
            self.y = -50
            self.width = 35
            self.height = 45
            self.speed = 1.5 + level * 0.4
            self.color = RED
            self.health = 1
            self.type = "normal"
            self.points = 10
        elif enemy_type < 0.85:
            # Быстрый враг
            self.x = random.randint(0, SCREEN_WIDTH - 30)
            self.y = -50
            self.width = 30
            self.height = 40
            self.speed = 2.5 + level * 0.5
            self.color = (255, 100, 100)
            self.health = 1
            self.type = "fast"
            self.points = 15
        else:
            # Босс
            self.x = random.randint(0, SCREEN_WIDTH - 60)
            self.y = -80
            self.width = 60
            self.height = 75
            self.speed = 0.7 + level * 0.2
            self.color = (180, 30, 30)
            self.health = 4 + level
            self.type = "boss"
            self.points = 40
        
        self.last_shot = 0
        self.shot_delay = 2000 + random.random() * 1000
        self.move_pattern = random.choice(["straight", "zigzag", "circle"])
        self.pattern_time = 0
        
    def draw(self):
        # Улучшенный дизайн врага
        if self.type == "fast":
            # Быстрый враг - более аэродинамичный
            points = [
                (self.x + self.width // 2, self.y),
                (self.x + self.width, self.y + self.height - 10),
                (self.x + self.width - 10, self.y + self.height),
                (self.x + 10, self.y + self.height),
                (self.x, self.y + self.height - 10)
            ]
        else:
            # Обычный и босс
            points = [
                (self.x + self.width // 2, self.y),
                (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height)
            ]
        
        pygame.draw.polygon(screen, self.color, points)
        
        # Кабина
        pygame.draw.circle(screen, (255, 180, 180), 
                          (self.x + self.width // 2, self.y + 12), 7)
        
        # Особенности босса
        if self.type == "boss":
            # Полоска здоровья
            pygame.draw.rect(screen, (30, 30, 30), 
                            (self.x - 5, self.y - 20, self.width + 10, 8))
            health_width = (self.width + 10) * (self.health / (4 + game.level))
            pygame.draw.rect(screen, (0, 255, 0), 
                            (self.x - 5, self.y - 20, health_width, 8))
            
            # Крылья
            pygame.draw.rect(screen, (150, 30, 30), 
                           (self.x - 15, self.y + 25, self.width + 30, 12))
    
    def update(self):
        self.pattern_time += 1
        
        # Паттерны движения
        if self.move_pattern == "zigzag":
            self.x += math.sin(self.pattern_time * 0.1) * 3
        elif self.move_pattern == "circle":
            self.x += math.sin(self.pattern_time * 0.05) * 4
            self.y += math.cos(self.pattern_time * 0.05) * 1
        
        self.y += self.speed
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        return self.y > SCREEN_HEIGHT
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_delay:
            if self.type == "boss":
                # Множественный огонь босса
                for i in range(3):
                    game.enemy_bullets.append(Bullet(
                        self.x + self.width // 2 - 2 + (i-1)*10,
                        self.y + self.height,
                        False,
                        "enemy"
                    ))
            else:
                game.enemy_bullets.append(Bullet(
                    self.x + self.width // 2 - 2,
                    self.y + self.height,
                    False,
                    "enemy"
                ))
            
            self.last_shot = current_time

class Bullet:
    def __init__(self, x, y, is_player=True, bullet_type="normal"):
        self.x = x
        self.y = y
        self.is_player = is_player
        self.type = bullet_type
        
        if bullet_type == "laser":
            self.width = 2
            self.height = 20
            self.speed = 12
            self.color = CYAN
            self.damage = 2
        elif bullet_type == "rocket":
            self.width = 8
            self.height = 16
            self.speed = 6
            self.color = ORANGE
            self.damage = 3
        else:
            self.width = 4
            self.height = 12
            self.speed = 8
            self.color = YELLOW if is_player else RED
            self.damage = 1
    
    def draw(self):
        if self.type == "laser":
            # Эффект лазера
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x-1, self.y, self.width+2, 6))
        elif self.type == "rocket":
            # Дизайн ракеты
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.polygon(screen, RED, [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width // 2, self.y - 5)
            ])
            # Огонь ракеты
            flame_size = 4 + math.sin(pygame.time.get_ticks() * 0.1) * 2
            pygame.draw.rect(screen, YELLOW, 
                           (self.x + self.width // 2 - 1, self.y + self.height, 2, flame_size))
        else:
            # Обычная пуля
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            if self.is_player:
                pygame.draw.rect(screen, WHITE, (self.x-1, self.y, self.width+2, 4))
    
    def update(self):
        if self.is_player:
            self.y -= self.speed
        else:
            self.y += self.speed
        
        return self.y < -20 or self.y > SCREEN_HEIGHT + 20

class Particle:
    def __init__(self, x, y, color, particle_type="normal"):
        self.x = x
        self.y = y
        self.type = particle_type
        
        if particle_type == "spark":
            self.size = random.uniform(1, 3)
            self.speed_x = random.uniform(-5, 5)
            self.speed_y = random.uniform(-5, 5)
            self.life = random.randint(15, 30)
        else:
            self.size = random.uniform(2, 6)
            self.speed_x = random.uniform(-4, 4)
            self.speed_y = random.uniform(-4, 4)
            self.life = random.randint(20, 40)
            
        self.color = color
        self.original_color = color
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        
        # Изменение цвета
        if self.life < 10:
            fade_alpha = int(255 * (self.life / 10))
            self.color = (
                self.original_color[0],
                self.original_color[1],
                self.original_color[2]
            )
        
        return self.life <= 0
    
    def draw(self):
        if self.type == "spark":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
        else:
            alpha = min(255, self.life * 6)
            size = int(self.size * (self.life / 40))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 2
        self.type = random.choice(["health", "weapon", "score", "shield", "life"])
        
        if self.type == "health":
            self.color = GREEN
            self.symbol = "+"
        elif self.type == "weapon":
            self.color = PURPLE
            self.symbol = "W"
        elif self.type == "score":
            self.color = GOLD
            self.symbol = "S"
        elif self.type == "life":
            self.color = CYAN
            self.symbol = "L"
        else:
            self.color = BLUE_LIGHT
            self.symbol = "D"
    
    def draw(self):
        # Эффект вращающегося бонуса
        size_mod = math.sin(pygame.time.get_ticks() * 0.01) * 3
        current_size = int(self.width // 2 + size_mod)
        
        pygame.draw.circle(screen, self.color, 
                         (int(self.x + self.width // 2), int(self.y + self.height // 2)), 
                         current_size)
        pygame.draw.circle(screen, WHITE, 
                         (int(self.x + self.width // 2), int(self.y + self.height // 2)), 
                         int(current_size * 0.6))
        
        # Символ
        symbol_text = font_tiny.render(self.symbol, True, (0, 0, 0))
        screen.blit(symbol_text, (self.x + self.width // 2 - 4, self.y + self.height // 2 - 6))
    
    def update(self):
        self.y += self.speed
        return self.y > SCREEN_HEIGHT

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.particles = []
        self.powerups = []
        self.score = 0
        self.level = 1
        self.last_enemy_spawn = 0
        self.enemy_spawn_rate = 2000
        self.game_state = "start"
        self.game_time = 0
        self.combo = 0
        self.last_kill_time = 0
        self.background_stars = []
        self.initialize_stars()
        self.high_score = 0
        
    def initialize_stars(self):
        self.background_stars = []
        for _ in range(100):
            self.background_stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'size': random.uniform(0.5, 2),
                'brightness': random.randint(100, 255)
            })
    
    def update_stars(self):
        for star in self.background_stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw_stars(self):
        for star in self.background_stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])
    
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > self.enemy_spawn_rate:
            self.enemies.append(Enemy(self.level))
            self.last_enemy_spawn = current_time
            
            # Постепенное уменьшение скорости появления
            self.enemy_spawn_rate = max(800, self.enemy_spawn_rate - 5)
    
    def spawn_powerup(self, x, y):
        if random.random() < 0.3:  # 30% шанс
            self.powerups.append(PowerUp(x, y))
    
    def create_particles(self, x, y, color, count, particle_type="normal"):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, particle_type))
    
    def check_collisions(self):
        # Пули игрока с врагами
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    self.create_particles(
                        enemy.x + enemy.width // 2,
                        enemy.y + enemy.height // 2,
                        ORANGE,
                        5,
                        "spark"
                    )
                    
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    enemy.health -= bullet.damage
                    
                    if enemy.health <= 0:
                        # Система комбо
                        current_time = pygame.time.get_ticks()
                        if current_time - self.last_kill_time < 2000:
                            self.combo += 1
                        else:
                            self.combo = 1
                        self.last_kill_time = current_time
                        
                        # Расчет очков
                        base_score = enemy.points * self.level
                        combo_bonus = base_score * (self.combo * 0.1)
                        total_score = int(base_score + combo_bonus)
                        self.score += total_score
                        
                        self.enemies.remove(enemy)
                        self.create_particles(
                            enemy.x + enemy.width // 2,
                            enemy.y + enemy.height // 2,
                            YELLOW,
                            15 if enemy.type == "boss" else 8
                        )
                        
                        # Появление бонуса
                        self.spawn_powerup(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                    
                    break
        
        # Вражеские пули с игроком
        for bullet in self.enemy_bullets[:]:
            if (bullet.x < self.player.x + self.player.width and
                bullet.x + bullet.width > self.player.x and
                bullet.y < self.player.y + self.player.height and
                bullet.y + bullet.height > self.player.y and
                self.player.invincible == 0):
                
                self.create_particles(
                    self.player.x + self.player.width // 2,
                    self.player.y + self.player.height // 2,
                    (100, 200, 255),
                    6,
                    "spark"
                )
                
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                self.player.health -= 10
                
                if self.player.health <= 0:
                    self.player.lives -= 1
                    if self.player.lives > 0:
                        # Восстановление жизни
                        self.player.health = 100
                        self.player.invincible = 120  # 2 секунды неуязвимости
                        self.player.x = SCREEN_WIDTH // 2
                        self.player.y = SCREEN_HEIGHT - 100
                    else:
                        self.create_particles(
                            self.player.x + self.player.width // 2,
                            self.player.y + self.player.height // 2,
                            RED,
                            25
                        )
                        self.high_score = max(self.high_score, self.score)
                        self.game_state = "game_over"
                break
        
        # Столкновения врагов с игроком
        for enemy in self.enemies[:]:
            if (enemy.x < self.player.x + self.player.width and
                enemy.x + enemy.width > self.player.x and
                enemy.y < self.player.y + self.player.height and
                enemy.y + enemy.height > self.player.y and
                self.player.invincible == 0):
                
                self.create_particles(
                    enemy.x + enemy.width // 2,
                    enemy.y + enemy.height // 2,
                    ORANGE,
                    10
                )
                
                damage = 30 if enemy.type == "boss" else 20
                self.player.health -= damage
                self.enemies.remove(enemy)
                
                if self.player.health <= 0:
                    self.player.lives -= 1
                    if self.player.lives > 0:
                        self.player.health = 100
                        self.player.invincible = 120
                        self.player.x = SCREEN_WIDTH // 2
                        self.player.y = SCREEN_HEIGHT - 100
                    else:
                        self.high_score = max(self.high_score, self.score)
                        self.game_state = "game_over"
                break
        
        # Бонусы
        for powerup in self.powerups[:]:
            if (powerup.x < self.player.x + self.player.width and
                powerup.x + powerup.width > self.player.x and
                powerup.y < self.player.y + self.player.height and
                powerup.y + powerup.height > self.player.y):
                
                self.apply_powerup(powerup)
                self.powerups.remove(powerup)
                break
    
    def apply_powerup(self, powerup):
        if powerup.type == "health":
            self.player.health = min(self.player.max_health, self.player.health + 30)
            self.create_particles(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2,
                GREEN,
                10
            )
        elif powerup.type == "weapon":
            self.player.special_weapon = random.randint(2, 4)
            self.create_particles(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2,
                PURPLE,
                12
            )
        elif powerup.type == "score":
            self.score += 50 * self.level
            self.create_particles(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2,
                GOLD,
                8
            )
        elif powerup.type == "life":
            self.player.lives += 1
            self.create_particles(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2,
                CYAN,
                15
            )
        else:  # shield
            self.player.invincible = 180  # 3 секунды
            self.create_particles(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2,
                BLUE_LIGHT,
                15
            )
    
    def next_level(self):
        self.level += 1
        self.player.health = min(self.player.health + 25, self.player.max_health)
        self.player.special_weapon = 0
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.particles = []
        self.powerups = []
        self.combo = 0
        self.game_state = "playing"
    
    def restart(self):
        self.high_score = max(self.high_score, self.score)
        self.__init__()
        self.game_state = "playing"
        self.high_score = self.high_score  # Сохранить рекорд
    
    def update(self):
        self.game_time += 0.1
        
        if self.game_state == "playing":
            self.update_stars()
            self.spawn_enemy()
            
            for enemy in self.enemies[:]:
                if enemy.update():
                    self.enemies.remove(enemy)
                
                if random.random() < 0.01 * self.level:
                    enemy.shoot()
            
            for bullet in self.bullets[:]:
                if bullet.update():
                    self.bullets.remove(bullet)
            
            for bullet in self.enemy_bullets[:]:
                if bullet.update():
                    self.enemy_bullets.remove(bullet)
            
            for particle in self.particles[:]:
                if particle.update():
                    self.particles.remove(particle)
            
            for powerup in self.powerups[:]:
                if powerup.update():
                    self.powerups.remove(powerup)
            
            self.check_collisions()
            
            # Проверка времени комбо
            current_time = pygame.time.get_ticks()
            if current_time - self.last_kill_time > 2000:
                self.combo = 0
            
            if self.score >= self.level * 100:
                self.game_state = "level_complete"
    
    def draw_ui(self):
        # Фон UI
        pygame.draw.rect(screen, (0, 0, 0, 180), (10, 10, 320, 140), border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), (10, 10, 320, 140), 2, border_radius=10)
        
        # Счет и уровень
        score_text = font_medium.render(f"СЧЕТ: {self.score}", True, WHITE)
        level_text = font_medium.render(f"УРОВЕНЬ: {self.level}", True, WHITE)
        health_text = font_medium.render("ЗДОРОВЬЕ:", True, WHITE)
        
        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 55))
        screen.blit(health_text, (20, 90))
        
        # Полоска здоровья
        pygame.draw.rect(screen, (50, 50, 50), (20, 120, 200, 20), border_radius=5)
        health_width = max(0, self.player.health * 2)
        
        # Градиентная полоска здоровья
        if self.player.health > 70:
            health_color = (0, 255, 0)
        elif self.player.health > 30:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)
        
        pygame.draw.rect(screen, health_color, (20, 120, health_width, 20), border_radius=5)
        
        # Проценты здоровья и жизни
        health_percent = font_small.render(f"{self.player.health}%", True, WHITE)
        screen.blit(health_percent, (230, 120))
        
        # Индикатор жизней
        lives_text = font_small.render(f"ЖИЗНИ: {self.player.lives}", True, GREEN)
        screen.blit(lives_text, (20, 145))
        
        # Индикатор комбо
        if self.combo > 1:
            combo_text = font_small.render(f"COMBO: x{self.combo}", True, GOLD)
            screen.blit(combo_text, (SCREEN_WIDTH - 120, 20))
        
        # Индикатор специального оружия
        if self.player.special_weapon > 0:
            weapon_text = font_small.render(f"SPECIAL: {self.player.special_weapon}", True, PURPLE)
            screen.blit(weapon_text, (SCREEN_WIDTH - 150, 50))

# Запуск игры
game = Game()
clock = pygame.time.Clock()
running = True

# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game.game_state == "playing":
                game.player.shoot()
            elif event.key == pygame.K_RETURN:
                if game.game_state == "start":
                    game.game_state = "playing"
                elif game.game_state == "level_complete":
                    game.next_level()
                elif game.game_state == "game_over":
                    game.restart()
            elif event.key == pygame.K_r:
                game.restart()
            elif event.key == pygame.K_ESCAPE:
                if game.game_state == "playing":
                    game.game_state = "paused"
                elif game.game_state == "paused":
                    game.game_state = "playing"
    
    keys = pygame.key.get_pressed()
    
    if game.game_state == "playing":
        game.player.move(keys)
        if keys[pygame.K_SPACE]:
            game.player.shoot()
    
    game.update()
    
    # Отрисовка
    screen.fill(BLUE_DARK)
    
    # Фон
    game.draw_stars()
    
    # Пули
    for bullet in game.enemy_bullets:
        bullet.draw()
    for bullet in game.bullets:
        bullet.draw()
    
    # Враги
    for enemy in game.enemies:
        enemy.draw()
    
    # Бонусы
    for powerup in game.powerups:
        powerup.draw()
    
    # Игрок
    if game.game_state != "start":
        game.player.draw()
    
    # Частицы
    for particle in game.particles:
        particle.draw()
    
    # UI
    game.draw_ui()
    
    # Меню
    if game.game_state == "start":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = font_large.render("🎯 ТОП ГАН 🚀", True, GOLD)
        subtitle = font_medium.render("БОЕВАЯ МИССИЯ", True, WHITE)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 190))
        
        instructions = [
            "Уничтожьте вражеские самолеты!",
            "Соберите 100 очков для перехода",
            "Избегайте вражеских атак!",
            "Собирайте бонусы для улучшений",
            "",
            "Управление:",
            "←↑↓→ - Движение, SHIFT - Ускорить",
            "ПРОБЕЛ - Стрельба, R - Рестарт",
            "ESC - Пауза"
        ]
        
        for i, instruction in enumerate(instructions):
            color = GOLD if i < 4 else WHITE
            text = font_small.render(instruction, True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i * 28))
        
        start_text = font_medium.render("Нажмите ENTER чтобы начать", True, GREEN)
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 500))
    
    elif game.game_state == "level_complete":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = font_large.render("МИССИЯ ВЫПОЛНЕНА! ✅", True, GREEN)
        level_text = font_medium.render(f"Уровень {game.level} пройден", True, WHITE)
        score_text = font_medium.render(f"Счет: {game.score}", True, WHITE)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 250))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 290))
        
        next_text = font_medium.render("Нажмите ENTER для следующего уровня", True, WHITE)
        screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 400))
    
    elif game.game_state == "game_over":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = font_large.render("МИССИЯ ПРОВАЛЕНА 💀", True, RED)
        score_text = font_medium.render(f"Ваш счет: {game.score}", True, WHITE)
        level_text = font_medium.render(f"Достигнутый уровень: {game.level}", True, WHITE)
        high_score_text = font_medium.render(f"Рекорд: {game.high_score}", True, GOLD)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 200))
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 240))
        screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, 280))
        
        restart_text = font_medium.render("Нажмите ENTER или R чтобы повторить", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    
    elif game.game_state == "paused":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pause_text = font_large.render("ПАУЗА", True, YELLOW)
        continue_text = font_medium.render("Нажмите ESC чтобы продолжить", True, WHITE)
        
        screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, 250))
        screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, 320))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()