import os
import pygame
# импорт нужных библиотек
pygame.init()
# создание характеристик текста логина и экрана
screen = pygame.display.set_mode((550, 240))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
login = ''
book = 'qwertyuiopasdfghjklzxcvbnm1234567890_'


class InputBox:  # создание строчки ввода логина
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.key_down = 0
        self.rect.w = 346

    def handle_event(self, event):  # отрисовка всего текста
        if event.type == pygame.MOUSEBUTTONDOWN:
            # проверка на нажатие на строку ввода логина
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # активация строки ввода
            else:
                self.active = False  # дезактивация строки ввода
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE  # изменение цвета строки ввода для её активации
        if event.type == pygame.KEYDOWN:
            if self.active:
                # прверка на провиьлный ввод логина
                if event.key == pygame.K_RETURN and 5 < len(self.text) < 17 and self.check_login():
                    # сохранение ологина и окончание регистриции / входа
                    global login
                    login = self.text
                    self.text = ''
                    self.key_down = 0
                elif event.key == pygame.K_BACKSPACE:
                    # удаление последнего символа логина
                    self.key_down -= 1
                    self.text = self.text[:-1]
                elif self.key_down < 16:
                    # написание символа в логин
                    self.key_down += 1
                    self.text += event.unicode
                # рендер текста
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # создание картинки строки ввода
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # отрисовка строки ввода
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # список характерисктик текста
        font = [pygame.font.Font(None, 35),
                pygame.font.Font(None, 35),
                pygame.font.Font(None, 23),
                pygame.font.Font(None, 23),
                pygame.font.Font(None, 23)]
        # список координат текста
        coord_text = [(182, 20),
                      (40, 104),
                      (50, 170),
                      (50, 190),
                      (50, 210)]
        # список текста
        text = ['Вход в аккаунт',
                'Логин:',
                'Если у Вас нет аккаунта, то он будет создан автоматически.',
                'Логин может содержать от 6 до 16 символов, английские',
                'буквы, цифры и знак _. После ввода логина нажмите Enter.']
        # отрисовка текста
        for i in range(len(text)):
            string_rendered = font[i].render(text[i], 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = coord_text[i][1]
            intro_rect.x = coord_text[i][0]
            screen.blit(string_rendered, intro_rect)

    def check_login(self):  # проверка на наличие ненужных символов в логине
        for i in self.text.lower():
            if i not in book:
                return False
        return True


def initialization():  # вход в аккаунт
    clock = pygame.time.Clock()
    input_box1 = InputBox(140, 100, 140, 32)  # создание строки ввода и текста
    done = False
    # изменение курсора
    pygame.mouse.set_visible(False)
    fullname = os.path.join('data\image', 'cursor_fon.png')
    cursor = pygame.image.load(fullname)
    while not done:
        for event in pygame.event.get():  # проверка на действия игрока
            if event.type == pygame.QUIT or login != '':  # проверка на конец входа
                done = True
            input_box1.handle_event(event)  # отрисовка изменений в окне
        # отрисовка текста и курсора
        screen.fill((30, 30, 30))
        input_box1.draw(screen)
        screen.blit(cursor, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(60)
    return login  # возвращение логина


if __name__ == '__main__':
    initialization()  # вход в аккаунт
    pygame.quit()
