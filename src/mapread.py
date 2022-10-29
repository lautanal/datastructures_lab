import os


def read(fname):
    """Kartan luku tiedostosta.

    Returns:
        maparray: Luettu kartta kirjaintaulukkona
    """
    maparray = []
    try:
        dirname = os.path.dirname(__file__)
        data_file_path = os.path.join(dirname, '..', 'data', 'maps', fname)            
        with open(data_file_path) as file:
            irow = 0
            for row in file:
                irow += 1
                if irow > 4:
                    row = row.replace('\n', '')
                    maparray.append([char for char in row])
        print(f'Karttatiedosto {fname} luettu')
    except FileNotFoundError:
        print('Tiedostoa ei löytynyt')
    return maparray


def write(map, fname):
    """Kartan kirjoitus tiedostoon.
    Args:
        map: Talletettava kartta
    """
    dirname = os.path.dirname(__file__)
    data_file_path = os.path.join(dirname, '..', 'data', 'maps', fname)            
    with open(data_file_path, 'w') as file:
        s = 'type octile\n'
        file.write(s)
        s = 'height ' + str(len(map)) + '\n'
        file.write(s)
        s = 'width ' + str(len(map[0])) + '\n'
        file.write(s)
        s = 'map\n'
        file.write(s)
        for row in map:
            s = ''
            for node in row:
                s += node
            for node in row:
                s += node
            s += '\n'
            file.write(s)
    print(f'Karttatiedosto {fname} talletettu')

map = read('6.map')
write(map, '6b.map')