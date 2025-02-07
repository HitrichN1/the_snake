import random

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константа центра экрана
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цветовые константы:
BOARD_BACKGROUND_COLOR = (165, 165, 165)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BODY_COLOR = (0, 0, 0)

# Константа ячеек поля
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
)

KEY_MAPPING = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT
}

# Скорость движения змейки:
snake_speed = 10

# Рекорд длины змейки
high_score = 0

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.
    Определяет цвет и позицию объекта, а также метод его отрисовки.
    """

    def __init__(self, color=BODY_COLOR):
        self.body_color = color

    def draw_cell(self, position, color=None):
        """Рисует одну ячейку."""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Пустой метод."""
        pass


class Apple(GameObject):
    """
    Класс, представляющий яблоко на игровом поле.
    Яблоко появляется в случайной позиции и может быть съедено змейкой.
    """

    def __init__(self, occupied_positions=None, color=APPLE_COLOR):
        super().__init__(color)
        if occupied_positions is None:
            occupied_positions = set()
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в случайную позицию на поле."""
        self.position = random.choice(tuple(ALL_CELLS
                                            - set(occupied_positions)))

    def draw(self):
        """Рисует яблоко на поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """
    Класс, представляющий змейку.
    Змейка двигается по полю, увеличивается при поедании яблок и
    может столкнуться с самой собой.
    """

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(color)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.last = None
        self.length = 1

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змейку на экране."""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def update_direction(self, new_direction):
        """Обновляет направление змейки."""
        # Проверяем, чтобы змейка не могла развернуться назад
        if ((self.direction == UP and new_direction != DOWN)
           or (self.direction == DOWN and new_direction != UP)
           or (self.direction == LEFT and new_direction != RIGHT)
           or (self.direction == RIGHT and new_direction != LEFT)):
            self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.positions.insert(0, (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        ))
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def check_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        return (self.length > 4 and self.get_head_position() in
                self.positions[4:])


# Функция обработки действий пользователя
def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    global snake_speed
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key in KEY_MAPPING:
                snake.update_direction(KEY_MAPPING[event.key])
            elif event.key == pg.K_PAGEUP:
                snake_speed = min(20, snake_speed + 1)
                update_caption()
            elif event.key == pg.K_PAGEDOWN:
                snake_speed = max(1, snake_speed - 1)
                update_caption()
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def update_caption():
    """Обновляет заголовок окна с текущими
    значениями рекорда и скорости.
    """
    pg.display.set_caption(f'Змейка'
                           f' | Рекорд: {high_score} |'
                           f' Скорость: {snake_speed}'
                           f' (Pg.Up +, Pg.Dn -)'
                           f' | ESC - выйти')


def main():
    """
    Основная функция игры.
    Инициализирует игру и запускает основной игровой цикл.
    """
    global snake_speed, high_score
    # Инициализация PyGame:
    pg.init()
    # Устанавливаем фон
    screen.fill(BOARD_BACKGROUND_COLOR)
    # Создаём экземпляры классов
    snake = Snake()
    apple = Apple(snake.positions)
    # Обновление заголовка
    update_caption()

    # Основной цикл
    while True:
        clock.tick(snake_speed)
        # Обработка ввода пользователя
        handle_keys(snake)
        # Движение змейки
        snake.move()
        # Флаг, указывающий, было ли съедено яблоко
        apple_eaten = False

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            # Увеличивает длину змейки
            snake.length += 1
            # Перемещаем яблоко с учетом занятых позиций
            apple.randomize_position(snake.positions)
            apple_eaten = True

        # Проверка столкновения с собой
        if not apple_eaten and snake.check_collision():
            screen.fill(BOARD_BACKGROUND_COLOR)
            # Обновляем рекорд, если текущая длина больше
            high_score = max(high_score, snake.length)
            update_caption()
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка объектов.
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
