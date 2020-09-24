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
tabella = tabella2

def stampa_tabella(tab):
    print('==' * 12)
    for i in range(len(tab)):
        if i % 3 == 0 and i != 0:
            print('- ' * 12)

        for j in range(len(tab[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end='')
            
            if j == 8:
                print(tab[i][j])
            else:
                print(f'{tab[i][j]} ', end='')
    print('==' * 12)

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


def risolvi(tab):
    # se la tabella è piena è risolta
    vuoti = trova_vuoti(tab)
    if not vuoti:
        return True
    else:
        riga, colonna = vuoti
        
    for num in range(1, 10):
        if valido(tab, num, (riga, colonna)):
            tab[riga][colonna] = num

            if risolvi(tab):
                return True
            tab[riga][colonna] = 0
    return False

if __name__ == "__main__":
    stampa_tabella(tabella)
    risolvi(tabella)
    stampa_tabella(tabella)
