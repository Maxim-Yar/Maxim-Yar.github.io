import pygame, random, sys, os, math
from account_login import initialization
from PIL import Image

# импорт нужных библиотек
# загрузка логина и авторизация в игре
login = initialization()
log = {}


def check_login():
    global log
    # изъятие из файла аккаунтов лучшего прохождения пользователя
    with open('data/logins.txt', 'r', encoding='utf8') as file:
        lines = file.readlines()
        for i in lines:
            x = i.split(' ')
            log[x[0]] = int(x[1])
        # проверка на наличие данного пользователя в файле
        if login in log:
            return log[login]
        else:
            log[login] = 0
            return 0
        # запись в список логинов в случае отсутствия его в файле для последующего сохранения


# создание нужных переменных для последующего их испрользования
pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 1080, 720
best_result = check_login()
inizial = login != ''
screen = pygame.display.set_mode(size)
all_enemy = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_bullet = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 165
player = None
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coord_x, coord_y = 500, 290
level = 0
len_enemy = []
bullet = []
live_player = False
id_image = 1
delay = 0
k_delay = 1
up_image = 0


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# добавление стен
Border(-1, -1, width, -1)
Border(-1, height, width, height)
Border(-1, -1, -1, height)
Border(width, -1, width, height)


def spawn_enemy():  # спавн противника
    x_enemy = random.randint(0, 952)
    y_enemy = random.randint(0, 564)
    x_player, y_player = player.get_coord_player()
    r = round(((y_enemy - y_player) ** 2 + (x_enemy - x_player) ** 2) ** 0.5)
    # проверка на различный спавн нескольких противников и удаленнорсть от игрока
    while [x_enemy, y_enemy] in len_enemy or r <= 250:
        x_enemy = random.randint(0, 952)
        y_enemy = random.randint(0, 564)
        r = round(((y_enemy - y_player) ** 2 + (x_enemy - x_player) ** 2) ** 0.5)
    len_enemy.append([x_enemy, y_enemy])
    return x_enemy, y_enemy


def save_logins():  # сохранение логинов в файл
    with open('data/logins.txt', 'w') as file:
        for i in log.keys():
            if i != '':
                file.write(f'{i} {log[i]}\n')


def terminate():  # полное закрытие окон игры
    pygame.quit()
    sys.exit()


def start_screen():  # прогрузка главного меню
    text = ["Аккаунт: " + login,  # список надписей в игре
            f"Лучший результат: {best_result}",
            "НАЧАТЬ",
            "ВЫХОД",
            "Благодарим Вас за скачивание данной игры.",
            'Чтобы предвиграться используйте клавиши W, A, S, D.',
            'Для атаки используйте любые кнопки мыши.',
            'Удачи в битве, солдат!']
    coord = [(580, 40),  # список координат этих надписей
             (580, 250),
             (650, 320),
             (650, 420),
             (540, 550),
             (505, 580),
             (540, 600),
             (625, 630)]
    global delay, k_delay, id_image, up_image
    fon = pygame.transform.scale(load_image(f'image_start_screen/start_screen_{id_image}.png'), (width, height))
    font = [pygame.font.Font(None, 35),  # список характерстик написания текста
            pygame.font.Font(None, 35),
            pygame.font.Font(None, 40),
            pygame.font.Font(None, 40),
            pygame.font.Font(None, 23),
            pygame.font.Font(None, 23),
            pygame.font.Font(None, 23),
            pygame.font.Font(None, 23)]
    while True:
        # проверка на нажатия игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_logins()
                terminate()  # полное закрытие игры
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos  # проверка нажатия на кнопки гланого меню
                if (600 <= x <= 810) and (400 <= y <= 460):
                    save_logins()
                    terminate()
                elif (600 <= x <= 810) and (300 <= y <= 360):
                    return
        x, y = pygame.mouse.get_pos()
        screen.blit(fon, (0, 0))
        text_coord = 50
        if delay == 200:  # измерение задержки для динамичного фона
            up_image += 1
            k_delay = -1
        elif delay == 0:
            up_image += 1
            k_delay = 1
        delay += k_delay
        # изменение id нужной отображаемой картинки
        if delay // 2 and up_image % 4 == 0 and 1 < id_image <= 100:
            id_image -= 1
        elif delay // 2 and up_image % 2 == 0 and 1 <= id_image < 100:
            id_image += 1
        if delay // 2 and up_image % 2 == 0:  # отрисовка получившегося фона
            fon = pygame.transform.scale(load_image(f'image_start_screen/start_screen_{id_image}.png'), (width, height))
        for i in range(len(text)):  # отрисовка текста
            string_rendered = font[i].render(text[i], 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = coord[i][1]
            intro_rect.x = coord[i][0]
            screen.blit(string_rendered, intro_rect)
        # отрисовка кнопок и курсора
        pygame.draw.rect(screen, (255, 255, 255), ((600, 400), (210, 60)), 2)
        pygame.draw.rect(screen, (255, 255, 255), ((600, 300), (210, 60)), 2)
        screen.blit(cursor_fon_image, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def lose_screen():  # прогрузка экрана смерти
    # содание необходимых параметров
    fon = pygame.transform.scale(load_image('lose_screen.png'), (width, height))
    lose_sound.play()
    font = pygame.font.Font(None, 30)
    text = login + ", Ваш результат: " + str(level)
    coord = (390, 500)
    global best_result  # изменение лучшего результата игрока при его улучшении
    if best_result < level:
        best_result = level
        log[login] = best_result
    while True:
        # проверка на действия игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_logins()  # сохранение в файл всех логинов
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # выход из экрана смерти через пробел
                    return
        # отображение фона и текста
        screen.blit(fon, (0, 0))
        string_rendered = font.render(text, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = coord[1]
        intro_rect.x = coord[0]
        screen.blit(string_rendered, intro_rect)
        screen.blit(cursor_fon_image, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():  # прогрузка экрана победы
    fon = pygame.transform.scale(load_image('win_screen.png'), (width, height))
    win_sound.play()
    font = [pygame.font.Font(None, 60), pygame.font.Font(None, 35), pygame.font.Font(None, 55)]
    text = [login.upper(), "Ваш результат: ", '15!']
    coord = [(530 - 14 * len(login), 100), (410, 590), (605, 581)]
    color = ['white', 'white', 'red']
    global best_result
    best_result = level  # сохранение лучшего результата
    log[login] = best_result
    while True:
        # проверка на действия игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # сохранение в файл всех логинов
                save_logins()
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # выход из экрана победы через пробел
                    return
        # отображение текста, фона и курсора
        screen.blit(fon, (0, 0))
        for i in range(len(text)):
            string_rendered = font[i].render(text[i], 1, pygame.Color(color[i]))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = coord[i][1]
            intro_rect.x = coord[i][0]
            screen.blit(string_rendered, intro_rect)
        screen.blit(cursor_fon_image, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):  # загрузка изображений из системы
    fullname = os.path.join('data\image', name)
    if not os.path.isfile(fullname):  # проверка на наличие изображений
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_sound(name):  # загрузка музыка из системы
    fullname = os.path.join('data\sound', name)
    if not os.path.isfile(fullname):  # проверка на наличие музыки
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound


# загрузка всех необходимых изображений и музыки
player_image_stay_down = load_image('player_stay_down.png')
player_image_going_left_1 = load_image('player_going_left_1.png')
player_image_going_left_2 = load_image('player_going_left_2.png')
player_image_stay_left = load_image('player_stay_left.png')
player_image_going_down = load_image('player_going_down.png')
player_image_going_right_1 = load_image('player_going_right_1.png')
player_image_going_right_2 = load_image('player_going_right_2.png')
player_image_stay_right = load_image('player_stay_right.png')
player_image_stay_up = load_image('player_stay_up.png')
player_image_going_up_1 = load_image('player_going_up_1.png')
player_image_going_up_2 = load_image('player_going_up_2.png')
enemy_image_stay_down = load_image('enemy_stay_down.png')
enemy_image_stay_up = load_image('enemy_stay_up.png')
enemy_image_stay_right = load_image('enemy_stay_right.png')
enemy_image_stay_left = load_image('enemy_stay_left.png')
enemy_image_going_right_1 = load_image('enemy_going_right_1.png')
enemy_image_going_right_2 = load_image('enemy_going_right_2.png')
enemy_image_going_left_1 = load_image('enemy_going_left_1.png')
enemy_image_going_left_2 = load_image('enemy_going_left_2.png')
enemy_image_going_down_1 = load_image('enemy_going_down_1.png')
enemy_image_going_down_2 = load_image('enemy_going_down_2.png')
enemy_image_going_up_1 = load_image('enemy_going_up_1.png')
enemy_image_going_up_2 = load_image('enemy_going_up_2.png')
start_screen_image_1 = Image.open('data/image/start_screen_1.png')
start_screen_image_2 = Image.open('data/image/start_screen_2.png')
cursor_fon_image = load_image('cursor_fon.png')
bullet_image = load_image('bullet.png')
cursor_image = load_image('aim.png')
player_damage = load_sound('player_damage.wav')
enemy_damage = load_sound('enemy_damage.wav')
lose_sound = load_sound('lose_sound.wav')
win_sound = load_sound('win_sound.wav')


class Player(pygame.sprite.Sprite):  # создание фигурки игрока
    def __init__(self):
        super().__init__(player_group)
        self.image = player_image_stay_down
        self.rect = self.image.get_rect().move(coord_x, coord_y)
        self.x = 0
        self.y = 0
        self.hp = 20 + 10 * 2 ** level

    def update(self):
        global coord_x, coord_y
        g = 40
        self.y = (self.y + 1) % (g * 2)  # изменение задержки для имитации ходьбы
        v = 3
        if self.x == pygame.K_d:
            if self.y < g:  # имитация хотьбы
                self.image = player_image_going_right_1
            else:
                self.image = player_image_going_right_2
            coord_x += v  # передвижение фигурки игрока
            self.rect = self.rect.move(v, 0)
        elif self.x == pygame.K_a:
            if self.y < g:  # имитация хотьбы
                self.image = player_image_going_left_1
            else:
                self.image = player_image_going_left_2
            coord_x -= v  # передвижение фигурки игрока
            self.rect = self.rect.move(-v, 0)
        elif self.x == pygame.K_s:
            self.image = player_image_going_down  # имитация хотьбы
            coord_y += v  # передвижение фигурки игрока
            self.rect = self.rect.move(0, v)
        elif self.x == pygame.K_w:
            if self.y < g:  # имитация хотьбы
                self.image = player_image_going_up_1
            else:
                self.image = player_image_going_up_2
            coord_y -= v  # передвижение фигурки игрока
            self.rect = self.rect.move(0, -v)
        if coord_y >= 360:  # передвижение иггрока внуть ринга
            b = min(0, height - self.image.get_height() - coord_y)
        else:
            b = max(0, -coord_y)
        if coord_x >= 540:
            a = min(0, width - self.image.get_width() - coord_x)
        else:
            a = max(0, -coord_x)
        self.rect = self.rect.move(a, b)
        coord_x += a
        coord_y += b
        self.x = 0

    def move(self, x):  # исчитывание нажатия клавиш
        self.x = x
        self.update()

    def move_last(self, x):  # изменение изображение при отсутствии нажатий игрока
        # изображение при отсутствии движения
        if x == pygame.K_a:
            self.image = player_image_stay_left
        elif x == pygame.K_d:
            self.image = player_image_stay_right
        elif x == pygame.K_w:
            self.image = player_image_stay_up
        elif x == pygame.K_s:
            self.image = player_image_stay_down

    def get_coord_player(self):  # возвращение координат центра фигурки игрока
        return self.rect.center

    def get_see_player(self):  # возвращает сторону, куда повернут игрок
        down = [player_image_stay_down, player_image_going_down]
        right = [player_image_stay_right, player_image_going_right_1, player_image_going_right_2]
        up = [player_image_stay_up, player_image_going_up_1, player_image_going_up_2]
        left = [player_image_stay_left, player_image_going_left_1, player_image_going_left_2]
        if self.image in down:
            return 'down'
        elif self.image in right:
            return 'right'
        elif self.image in left:
            return 'left'
        elif self.image in up:
            return 'up'

    def get_size_image_player(self):  # возвращает размеры изображения картинки
        return self.image.get_size()

    def player_rotated(self, pos):  # вращение игрока относительно координат нажатия мыши
        x, y = pos
        x_pl, y_pl = self.rect.center
        # нахождение угла между разницами координат осей x и y через косинус
        angle = math.acos((x - x_pl) / ((x - x_pl) ** 2 + (y - y_pl) ** 2) ** 0.5) / math.pi * 180
        if y > y_pl:
            angle = (360 - angle) % 360
        if angle <= 45 or angle > 315:
            self.image = player_image_stay_right
        elif 45 < angle <= 135:
            self.image = player_image_stay_up
        elif 135 < angle <= 225:
            self.image = player_image_stay_left
        elif 225 < angle <= 315:
            self.image = player_image_stay_down

    def damage(self):  # уменьшение хп игрока при получении урона
        self.hp -= 4 + 2 ** level // 2
        player_damage.play()
        self.die()

    def die(self):  # смерть игрока
        if self.hp <= 0:
            global live_player
            live_player = True
            self.kill()

    def get_player_hp(self):  # возвращение хп игрока
        return self.hp

    def restart(self):  # возвращение характеристик игрока после окончания раунда
        self.image = player_image_stay_down
        global coord_x, coord_y
        self.rect = self.rect.move(-coord_x + 500, -coord_y + 290)
        coord_y = 290
        coord_x = 500
        self.x = 0
        self.y = 0
        self.hp = 20 + 10 * 2 ** level


class Enemy(pygame.sprite.Sprite):  # создание фигурок противников
    def __init__(self):
        super().__init__(all_enemy)
        self.image = enemy_image_stay_down
        self.coord_x, self.coord_y = spawn_enemy()
        self.rect = self.image.get_rect().move(self.coord_x, self.coord_y)
        self.width = self.rect.width
        self.height = self.rect.height
        self.coord_player = None
        self.coord_enemy = 'down'
        self.hp = 18 + 3 * 2 ** level
        self.y = 0
        self.time = 0

    def get_coord_player(self):  # нахождение игрока относительно фигурки противника
        x_player, y_player = player.get_coord_player()
        x_enemy, y_enemy = self.rect.center
        a = ((x_player - x_enemy) ** 2 + (y_player - y_enemy) ** 2) ** 0.5  # расстояние между игроком и противником
        c = ((x_enemy + 1 - x_player) ** 2 + (
                    y_enemy - y_player) ** 2) ** 0.5  # расстояние между игроком и соседней координатой противника
        self.cos_player = (a ** 2 + 1 - c ** 2) / (2 * a)  # нахождение угла через теорему косинусов
        if self.cos_player >= 1 / 2 ** 0.5:
            self.coord_player = 'right'
        elif self.cos_player >= -1 / 2 ** 0.5 and coord_y > y_enemy:
            self.coord_player = 'down'
        elif self.cos_player >= -1 / 2 ** 0.5:
            self.coord_player = 'up'
        elif self.cos_player >= -1:
            self.coord_player = 'left'

    def update(self):  # передвижение противника
        g = 40
        v = 2
        time_out = True
        self.y = (self.y + 1) % (g * 2)
        x_player, y_player = player.get_coord_player()
        r = round(
            ((self.coord_y + self.height // 2 - y_player) ** 2 + (
                    self.coord_x + self.width // 2 - x_player) ** 2) ** 0.5)
        # нахождение растояния между противником и игроком
        self.get_coord_player()
        if self.coord_enemy != self.coord_player:
            self.coord_enemy = self.coord_player
        if r <= 300:  # передвижение противника до расстояния между игроком 300
            # поворот противника в сторону игрока
            if self.coord_enemy == 'right':
                self.image = enemy_image_stay_right
            elif self.coord_enemy == 'left':
                self.image = enemy_image_stay_left
            elif self.coord_enemy == 'up':
                self.image = enemy_image_stay_up
            elif self.coord_enemy == 'down':
                self.image = enemy_image_stay_down
            if self.time == 75:  # атака при завершении перезарядки
                time_out = True
                self.attack()
        elif r > 300:
            if self.time == 75:  # завершение перезарядки при
                time_out = False
            x_enemy, y_enemy = self.rect.center
            # нахождение минимальной нужой скорости передвижения
            min_x = min(v, abs(x_enemy - x_player))
            min_y = min(v, abs(y_enemy - y_player))
            edge_x, edge_y = 1080, 720
            # передвижение при одинаковой одной из координат
            if x_player == x_enemy and y_player > y_enemy:
                if self.y < g:  # имитация ходьбы
                    self.image = enemy_image_going_down_1
                else:
                    self.image = enemy_image_going_down_2
                self.rect = self.rect.move(0, min_y)  # передвижение противника
                self.coord_y += min_y
                if pygame.sprite.spritecollideany(self,
                                                  horizontal_borders):  # отход противника при достижении края ринга
                    self.coord_y -= min_y
                    self.rect = self.rect.move(0, -min_y)
            elif x_player == x_enemy and y_player < y_enemy:
                if self.y < g:  # имитация ходьбы
                    self.image = enemy_image_going_up_1
                else:
                    self.image = enemy_image_going_up_2
                self.rect = self.rect.move(0, -min_y)  # передвижение противника
                self.coord_y -= min_y
                if pygame.sprite.spritecollideany(self,
                                                  horizontal_borders):  # отход противника при достижении края ринга
                    self.coord_y += min_y
                    self.rect = self.rect.move(0, min_y)
            elif x_player > x_enemy and y_player == y_enemy:
                if self.y < g:  # имитация ходьбы
                    self.image = enemy_image_going_right_1
                else:
                    self.image = enemy_image_going_right_2
                self.rect = self.rect.move(min_x, 0)  # передвижение противника
                self.coord_x += min_x
                if pygame.sprite.spritecollideany(self, vertical_borders):  # отход противника при достижении края ринга
                    self.coord_x -= min_x
                    self.rect = self.rect.move(-min_x, 0)
            elif x_player < x_enemy and y_player == y_enemy:
                if self.y < g:  # имитация ходьбы
                    self.image = enemy_image_going_left_1
                else:
                    self.image = enemy_image_going_left_2
                self.rect = self.rect.move(-min_x, 0)  # передвижение противника
                self.coord_x -= min_x
                if pygame.sprite.spritecollideany(self, vertical_borders):  # отход противника при достижении края ринга
                    self.coord_x += min_x
                    self.rect = self.rect.move(min_x, 0)
            # нахождение осевой скорости противника
            if x_player != x_enemy:
                tan_alpha = abs(y_enemy - y_player) / abs(x_enemy - x_player)
            else:
                tan_alpha = 1
            x_going = math.ceil(v / (tan_alpha ** 2 + 1) ** 0.5 * tan_alpha)
            y_going = math.ceil(v / (tan_alpha ** 2 + 1) ** 0.5)
            min_x = min(x_going, abs(x_enemy - x_player))
            min_y = min(y_going, abs(y_enemy - y_player))
            if x_player > x_enemy and y_player > y_enemy:
                # нахождение минимально нужных скоростей
                min_x = min(min_x, edge_x - self.rect.width - self.coord_x)
                min_y = min(min_y, edge_y - self.rect.height - self.coord_y)
                if min_x >= min_y:  # имитация ходьбы
                    if self.y < g:
                        self.image = enemy_image_going_right_1
                    else:
                        self.image = enemy_image_going_right_2
                else:
                    if self.y < g:
                        self.image = enemy_image_going_down_1
                    else:
                        self.image = enemy_image_going_down_2
                self.rect = self.rect.move(min_x, min_y)  # передвижение противника
                self.coord_x += min_x
                self.coord_y += min_y
                if pygame.sprite.spritecollideany(self, vertical_borders) or \
                        pygame.sprite.spritecollideany(self,
                                                       horizontal_borders):  # отход противника при достижении края ринга
                    self.coord_x -= min_x
                    self.coord_y -= min_y
                    self.rect = self.rect.move(-min_x, -min_y)
            elif x_player > x_enemy and y_player < y_enemy:
                # нахождение минимально нужных скоростей
                min_x = min(min_x, edge_x - self.rect.width - self.coord_x)
                min_y = min(min_y, self.coord_y)
                if min_x >= min_y:  # имитация ходьбы
                    if self.y < g:
                        self.image = enemy_image_going_right_1
                    else:
                        self.image = enemy_image_going_right_2
                else:
                    if self.y < g:
                        self.image = enemy_image_going_up_1
                    else:
                        self.image = enemy_image_going_up_2
                self.rect = self.rect.move(min_x, -min_y)  # передвижение противника
                self.coord_x += min_x
                self.coord_y -= min_y
                if pygame.sprite.spritecollideany(self, vertical_borders) or \
                        pygame.sprite.spritecollideany(self,
                                                       horizontal_borders):  # отход противника при достижении края ринга
                    self.coord_x -= min_x
                    self.coord_y += min_y
                    self.rect = self.rect.move(-min_x, min_y)
            elif x_player < x_enemy and y_player < y_enemy:
                # нахождение минимально нужных скоростей
                min_x = min(min_x, self.coord_x)
                min_y = min(min_y, self.coord_y)
                if min_x >= min_y:  # имитация ходьбы
                    if self.y < g:
                        self.image = enemy_image_going_left_1
                    else:
                        self.image = enemy_image_going_left_2
                else:
                    if self.y < g:
                        self.image = enemy_image_going_up_1
                    else:
                        self.image = enemy_image_going_up_2
                self.rect = self.rect.move(-min_x, -min_y)  # передвижение противника
                self.coord_x -= min_x
                self.coord_y -= min_y
                if pygame.sprite.spritecollideany(self, vertical_borders) or \
                        pygame.sprite.spritecollideany(self,
                                                       horizontal_borders):  # отход противника при достижении края ринга
                    self.coord_x += min_x
                    self.coord_y += min_y
                    self.rect = self.rect.move(min_x, min_y)
            elif x_player < x_enemy and y_player > y_enemy:
                # нахождение минимально нужных скоростей
                min_x = min(min_x, self.coord_x)
                min_y = min(min_y, edge_y - self.rect.height - self.coord_y)
                if min_x >= min_y:  # имитация ходьбы
                    if self.y < g:
                        self.image = enemy_image_going_left_1
                    else:
                        self.image = enemy_image_going_left_2
                else:
                    if self.y < g:
                        self.image = enemy_image_going_down_1
                    else:
                        self.image = enemy_image_going_down_2
                self.rect = self.rect.move(-min_x, min_y)  # передвижение противника
                self.coord_x -= min_x
                self.coord_y += min_y
                if pygame.sprite.spritecollideany(self, vertical_borders) or \
                        pygame.sprite.spritecollideany(self,
                                                       horizontal_borders):  # отход противника при достижении края ринга
                    self.coord_x += min_x
                    self.coord_y -= min_y
                    self.rect = self.rect.move(min_x, -min_y)
        if time_out:  # изменение задержки перезарядки
            self.time = (self.time + 1) % 100

    def die(self):  # смерть противника
        if self.hp <= 0:
            del enemy[enemy.index(self)]
            self.kill()

    def attack(self):  # атака противника
        bullet.append(Bullet('enemy', player.get_coord_player(), self))

    def damage(self):  # получение урона
        self.hp -= 4 + 2 ** (level + 1)
        enemy_damage.play()
        self.die()

    def get_coord_enemy(self):  # возвращает координаты центра изображения противника
        return self.rect.center

    def get_see_enemy(self):  # возвращает сторону, в которую смотрит противник
        down = [enemy_image_going_down_1, enemy_image_going_down_2, enemy_image_stay_down]
        right = [enemy_image_going_right_1, enemy_image_going_right_2, enemy_image_stay_right]
        up = [enemy_image_going_up_1, enemy_image_going_up_2, enemy_image_stay_up]
        left = [enemy_image_going_left_1, enemy_image_going_left_2, enemy_image_stay_left]
        if self.image in down:
            return 'down'
        elif self.image in right:
            return 'right'
        elif self.image in left:
            return 'left'
        elif self.image in up:
            return 'up'

    def get_size_image_enemy(self):  # возвращает размеры изображения противника
        return self.image.get_size()


def blitRotate(image, pos, originPos, angle):  # поворот картинки вокруг своей оси
    # смещение от оси поворота к центру
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    # смещение поворота от оси поворота к центру
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    # повернутый центр изображения
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    # получение повернутого изображения
    rotated_image = pygame.transform.rotate(image, angle)
    # поверот и размазывание изображения
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    return rotated_image, rotated_image_rect


class Bullet(pygame.sprite.Sprite):  # создание фигурки пули
    def __init__(self, type_bullet, pos, enemy=None):
        super().__init__(all_bullet)
        self.image = bullet_image
        self.coord_x, self.coord_y = self.get_first_coord_bullet(type_bullet, enemy)
        self.angle = self.get_angle(pos)
        self.type = type_bullet
        # поворот изображения на грудус между линией цели и координат появления и горизонталью
        self.image, self.rect = blitRotate(self.image, (self.coord_x + 24, self.coord_y + 12), (24, 12), self.angle)
        self.lost_distance = (self.coord_x, self.coord_y)
        self.distance = {'player': 400, 'enemy': 300}
        self.v = 10
        self.delta_y = -self.v * math.sin(self.angle * math.pi / 180)
        self.delta_x = self.v * math.cos(self.angle * math.pi / 180)
        self.a, self.b = None, None

    def get_first_coord_bullet(self, type_bullet, enemy):  # нахождение начальных координат
        # нахождение координат владельца пули
        if type_bullet == 'player':
            x, y = player.get_coord_player()
            see = player.get_see_player()
            delta_x, delta_y = [i // 2 for i in player.get_size_image_player()]
        else:
            x, y = enemy.get_coord_enemy()
            see = enemy.get_see_enemy()
            delta_x, delta_y = [i // 2 for i in enemy.get_size_image_enemy()]
        g = 24  # ичитывание погрешности при повороте изображения
        # нахождение первоначальных координат с нужной стороны хозяева
        if see == 'down':
            y += (delta_y + g)
            x -= 24
        elif see == 'right':
            x += delta_x + g
            y -= 12
        elif see == 'up':
            y -= (delta_y + 2 * g)
            x -= 12
        elif see == 'left':
            x -= (delta_x + 2.5 * g)
            y -= 12
        return x, y

    def get_angle(self, pos):  # нахождение угла поворота пули
        x, y = pos
        c = ((x - self.coord_x - 24) ** 2 + (y - self.coord_y - 12) ** 2) ** 0.5
        angle = math.acos(abs(x - self.coord_x - 24) / c)
        if x < self.coord_x:
            angle = math.pi - angle
        if y > self.coord_y:
            angle = -angle
        return angle / math.pi * 180

    def die(self):  # уничтожение пули при столкновении или длительном полёте
        distanse = ((self.coord_x - self.lost_distance[0]) ** 2 + (self.coord_y - self.lost_distance[1]) ** 2) ** 0.5
        if distanse >= self.distance[self.type] or self.a or self.b:
            self.kill()

    def update(self):  # изменение координат пули
        # проверка столкновения пули
        self.a = pygame.sprite.spritecollideany(self, all_enemy) and self.type == 'player'
        self.b = pygame.sprite.spritecollideany(self, player_group) and self.type == 'enemy'
        if not (self.a or self.b):
            # перемещение пули
            self.rect = self.rect.move(self.delta_x, self.delta_y)
            self.coord_x += self.delta_x
            self.coord_y += self.delta_y
            # проверка на длительный полёт
            self.die()
        if self.a:
            # поиск объекта, в которого попала пуля
            list_enemy = pygame.sprite.spritecollide(self, all_enemy, False)
            for i in list_enemy:
                self.die()  # смерть пули
                i.damage()  # урон противнику
        if self.b:
            self.die()  # смерть пули
            player.damage()  # урон игроку


if __name__ == '__main__':
    running_2 = True
    save_logins()  # сохранение паролей на случай, елси игрок только зайдет в главное меню
    while running_2 and inizial:  # проверка входа в игру
        running_1 = True
        start_screen()  # главное меню
        player = Player()  # создание игроа
        while running_1 and level < 15 and not live_player:  # создание уровня и проверка на создание следуюцего
            enemy = [Enemy() for i in range(round(2 ** level))]  # создание нужного количества врагов
            len_enemy.clear()
            running = True
            going = False
            key = 0
            coord_text = [(490, 20),
                          (20, 20),
                          (20, 50)]
            pygame.mouse.set_visible(False)
            fon = pygame.transform.scale(load_image('fon_level.png'), (width, height))
            font = pygame.font.Font(None, 30)
            while running:
                if live_player:  # прекращение раунда при смерти игрока
                    break
                if len(enemy) == 0:  # прекращение раунда при отсутствии врагов
                    for i in bullet:
                        i.kill()
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # выход из игры
                        running = False
                        running_1 = False
                        running_2 = False
                    if event.type == pygame.KEYDOWN:  # проверка на нажати клавиш движения игрока
                        going = True
                        key = event.key
                    if event.type == pygame.KEYUP:  # проверка на прекращение движения игрока
                        going = False
                        player.move_last(event.key)
                        key = 0
                    if event.type == pygame.MOUSEBUTTONDOWN:  # атака игрока
                        player.player_rotated(event.pos)
                        bullet.append(Bullet('player', event.pos))
                # отображение текста, противников, игрока, фона, курсора
                screen.blit(fon, (0, 0))
                text = [f'уровень: {level + 1}',
                        f'хп: {player.get_player_hp()}',
                        f'враги: {len(enemy)}']
                x, y = pygame.mouse.get_pos()
                player.move(key)
                player_group.draw(screen)
                all_enemy.draw(screen)
                player_group.update()
                all_enemy.update()
                all_bullet.draw(screen)
                all_bullet.update()
                for i in range(len(text)):
                    string_rendered = font.render(text[i], 1, pygame.Color('#76EE00'))
                    intro_rect = string_rendered.get_rect()
                    intro_rect.top = coord_text[i][1]
                    intro_rect.x = coord_text[i][0]
                    screen.blit(string_rendered, intro_rect)
                screen.blit(cursor_image, (x - 30, y - 30))
                clock.tick(FPS)
                pygame.display.flip()
            # переход на следующий раунд в случае выживании игрока в прошлом
            if not live_player:
                level += 1
                player.restart()
        if level < 15 and live_player and running_2:  # проверка на смерть игрока
            lose_screen()
        elif level == 15 and running_2:  # проверка на победу игрока
            win_screen()
        if best_result < level:  # изменение результата игрока и его сохранение
            best_result = level
            log[login] = level
            save_logins()
        # подготовка к новой игре
        level = 0
        live_player = False
        for i in enemy:
            i.kill()
        enemy.clear()
        for i in bullet:
            i.kill()
        bullet.clear()
    pygame.quit()
