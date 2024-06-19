import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure of the Girl")

# Загрузка изображения для фонового изображения и увеличение его размера
background_image = pygame.image.load("forest.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background_image.get_rect()

# Размещение фонового изображения на экране
background_rect.topleft = (0, 0)

# Загрузка изображения для главного героя (девочки) и уменьшение его размера
girl_image = pygame.image.load("girls.png")  # Путь к изображению главного героя
girl_image = pygame.transform.scale(girl_image, (130, 110))

girl_rect = girl_image.get_rect()
girl_rect.bottomleft = (0, SCREEN_HEIGHT // 2)  # Установка начальных координат в левый нижний угол

# Загрузка изображения для монстра и уменьшение его размера
monster_image = pygame.image.load("monster.png")
monster_image = pygame.transform.scale(monster_image, (100, 100))

# Загрузка изображения начального экрана
start_screen_image = pygame.image.load("start.jpg")
start_screen_image = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_screen_rect = start_screen_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Список монстров
monsters = []

# Функция для создания нового монстра
def create_monster():
    monster = {
        "rect": monster_image.get_rect(),
        "speed": random.randint(1, 1),  # Уменьшение скорости монстра
    }
    monster["rect"].right = SCREEN_WIDTH
    monster["rect"].top = random.randint(0, SCREEN_HEIGHT - monster["rect"].height)
    return monster

# Функция для отрисовки монстров на экране
def draw_monsters():
    for monster in monsters:
        screen.blit(monster_image, monster["rect"])

# Функция для обновления положения монстров
def update_monsters():
    for monster in monsters:
        monster["rect"].x -= monster["speed"]

# Функция для проверки столкновения главного героя с монстрами
def check_collision():
    for monster in monsters:
        if girl_rect.colliderect(monster["rect"]):
            return True
    return False

# Функция для отображения изображения "Game Over"
def show_game_over():
    game_over_image = pygame.image.load("game.png")  # Загрузка изображения с надписью "Game Over"
    game_over_image = pygame.transform.scale(game_over_image, (400, 200))  # Изменение размера изображения
    image_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Определение положения изображения
    screen.blit(game_over_image, image_rect)  # Отображение изображения на экране

# Скорость перемещения главного героя (девочки)
speed = 3

# Таймер для создания новых монстров
CREATE_MONSTER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_MONSTER_EVENT, 1300)  # Уменьшение интервала появления монстров

# Функция для отображения начального экрана
def show_start_screen():
    screen.blit(start_screen_image, start_screen_rect)
    pygame.display.flip()
    wait_for_keypress()

# Функция ожидания нажатия клавиши
def wait_for_keypress():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Основной игровой цикл
running = True
game_over = False
start_screen_displayed = False

while running:
    if not start_screen_displayed:
        show_start_screen()
        start_screen_displayed = True

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == CREATE_MONSTER_EVENT:
            if not game_over:  # Добавляем проверку, чтобы монстры не создавались после завершения игры
                monsters.append(create_monster())

    if not game_over:
        # Управление главным героем (девочкой)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and girl_rect.top > 0:
            girl_rect.y -= speed
        if keys[pygame.K_DOWN] and girl_rect.bottom < SCREEN_HEIGHT:
            girl_rect.y += speed

        # Очистка экрана
        screen.fill(WHITE)

        # Отрисовка фонового изображения
        screen.blit(background_image, background_rect)

        # Отрисовка главного героя (девочки)
        screen.blit(girl_image, girl_rect)

        # Обновление и отрисовка монстров
        if not game_over:  # Добавляем проверку, чтобы монстры не двигались после завершения игры
            update_monsters()
            draw_monsters()

        # Проверка столкновения с монстрами
        if check_collision():
            game_over = True

        # Если game_over, показываем надпись "Game Over"
        if game_over:
            show_game_over()

        # Обновление экрана
        pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
sys.exit()
