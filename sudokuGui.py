import pygame
import time
from risolvi_sudoku import risolvi

# colors
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
color = BLUE

tabella1 = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]
tabella2 = [
    [0, 0, 9, 0, 0, 0, 7, 0, 0],
    [0, 4, 0, 5, 0, 9, 0, 1, 0],
    [3, 0, 0, 0, 1, 0, 0, 0, 2],
    [0, 1, 0, 0, 6, 0, 0, 7, 0],
    [0, 0, 2, 7, 0, 1, 8, 0, 0],
    [0, 5, 0, 0, 4, 0, 0, 3, 0],
    [7, 0, 0, 0, 3, 0, 0, 0, 4],
    [0, 8, 0, 2, 0, 4, 0, 6, 0],
    [0, 0, 6, 0, 0, 0, 5, 0, 0]
]

pygame.font.init()


class Grid:
    tabella = tabella1

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.cubes = [[Cube(self.tabella[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
# piazza il numero se valido
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valido(self.model, val, (row, col)) and risolvi(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    
# disegna una bozza
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

# disegna la griglia
    def draw(self, win, color, boxcolor=BLACK):
        gap = self.width // 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            
            pygame.draw.line(win, boxcolor, (0, i * gap), (self.width, i * gap), thick) # black
            pygame.draw.line(win, boxcolor, (i * gap, 0), (i * gap, self.height), thick)  # black
        # disegna i cubi
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win, color)

# seleziona cubo
    def select(self, row, col):
        # reset altri cubi
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)
    
# svuota la casella se il numero è errato
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)
    

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        return None
    

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def risolvi(self):
        # se la tabella è piena è risolta
        self.update_model()
        vuoti = trova_vuoti(self.model)
        if not vuoti:
            return True
        else:
            riga, colonna = vuoti

        for num in range(1, 10):
            if valido(self.model, num, (riga, colonna)):
                self.model[riga][colonna] = num

                if self.risolvi():
                    return True
                self.model[riga][colonna] = 0
        return False

    def risolviGui(self):
        # se la tabella è piena è risolta
        self.update_model()
        vuoti = trova_vuoti(self.model)
        if not vuoti:
            return True
        else:
            riga, colonna = vuoti

        for num in range(1, 10):
            if valido(self.model, num, (riga, colonna)):
                self.model[riga][colonna] = num
                self.cubes[riga][colonna].set(num)
                self.cubes[riga][colonna].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                if self.risolviGui():
                    return True
                self.model[riga][colonna] = 0
                self.cubes[riga][colonna].set(0)
                self.cubes[riga][colonna].draw_change(self.win, False)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
        return False

    
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0


    def draw(self, win, color=BLUE, color_temp=GRAY):
        font = pygame.font.SysFont('comicsans', 40)

        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, color_temp) # gray
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, ( int(x + (gap/2 - text.get_width()/2)), int(y + (gap/2 - text.get_height()/2)) ))

        if self.selected:
            pygame.draw.rect(win, color, (x, y, gap, gap), 3) #blue
    
    def draw_change(self, win, g=True):
        font = pygame.font.SysFont('comicsans', 40)
        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (int(x + (gap / 2 - text.get_width() / 2)), int(y + (gap / 2 - text.get_height() / 2))))
        if g:
            pygame.draw.rect(win, GREEN, (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, RED, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val


    def set_temp(self, val):
        self.temp = val


def trova_vuoti(tab):
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j] == 0:
                return (i, j)  # riga, colonna

    return None


def valido(tab, num, pos):
    # controlla riga
    for i in range(len(tab[0])):
        if tab[pos[0]][i] == num and pos[1] != i:
            return False

    # controlla colonna
    for i in range(len(tab)):
        if tab[i][pos[1]] == num and pos[0] != i:
            return False

    # controlla quadrato
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if tab[i][j] == num and (i, j) != pos:
                return False

    return True

def redraw_window(win, tabella, time, strikes):
    global color
    win.fill(WHITE)
    # disegna tempo
    font = pygame.font.SysFont('comicsans', 40)
    text = font.render(f'Time: {format_time(time)}', 1, BLACK)
    win.blit(text, (540 - 160, 560))
    # disegna errori
    text = font.render('X ' * strikes, 1, RED)
    win.blit(text, (20, 560))
    # disegna griglia e tabella
    tabella.draw(win, color)
    color = BLUE


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    if sec < 10:
        t = f' {minute}:0{sec}'
        return t
    t = f' {minute}:{sec}'
    return t

def main():
    global color
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('Sudoku')
    rows = 9
    cols = 9
    tabella = Grid(rows, cols, 540, 540, win)
    solved = False
    key = None
    run = True

    start = time.time()
    strikes = 0
    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    tabella.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    tabella.risolviGui()
                    solved = True
                if event.key == pygame.K_RETURN:
                    i, j = tabella.selected

                    if tabella.cubes[i][j].temp != 0:
                        # se il numero è corretto, inseriscilo e colora di verde, else rosso
                        if tabella.place(tabella.cubes[i][j].temp):
                            color = GREEN
                        else:
                            color = RED
                            strikes += 1
                        key = None
                        if tabella.is_finished():
                            print(f'Hai finito! in {format_time(play_time)}')
                            run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = tabella.click(pos)
                if clicked:
                    tabella.select(clicked[0], clicked[1])
                    key = None
        if tabella.selected and key != None:
            tabella.sketch(key)


        redraw_window(win, tabella, play_time, strikes)
        pygame.display.update()

        if solved:
            pygame.time.delay(3000)
            run = False


main()
pygame.quit()
