import os


def read(fname):
    """Read a map from a file.

    Returns:
        maparray: The map as an array
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
        print(f'Map file {fname} read')
    except FileNotFoundError:
        print('File not found')
    return maparray


def write(map, fname):
    """Write a map to a file.
    Args:
        map: The map to be written
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
    print(f'Map file {fname} saved')

map = read('6.map')
write(map, '6b.map')