import os


class Files:
    """Luokka, joka lukee ja tallettaa kartta-tiedostot

    Attributes:
        fname: Karttatiedoston nimi
    """

    def __init__(self):
        """Luokan konstruktori, joka luo uuden tiedostonkäsittelijän.
        """
        self.fname = 'f.map'

    def read(self):
        """Kartan luku tiedostosta.

        Returns:
            maparray: Luettu kartta kirjaintaulukkona
        """
        maparray = []
        try:
            dirname = os.path.dirname(__file__)
            data_file_path = os.path.join(dirname, '..', 'data', 'maps', self.fname)            
            with open(data_file_path) as file:
                irow = 0
                for row in file:
                    irow += 1
                    if irow > 4:
                        row = row.replace('\n', '')
                        maparray.append([char for char in row])
            print(f'Karttatiedosto {self.fname} luettu')
        except FileNotFoundError:
            print('Tiedostoa ei löytynyt')
        return maparray


    def write(self, map):
        """Kartan kirjoitus tiedostoon.
        Args:
            map: Talletettava kartta
        """
        dirname = os.path.dirname(__file__)
        data_file_path = os.path.join(dirname, '..', 'data', 'maps', self.fname)            
        with open(data_file_path, 'w') as file:
            s = 'type octile\n'
            file.write(s)
            s = 'height ' + str(len(map.nodes)) + '\n'
            file.write(s)
            s = 'width ' + str(len(map.nodes[0])) + '\n'
            file.write(s)
            s = 'map\n'
            file.write(s)
            for row in map.nodes:
                s = ''
                for node in row:
                    if node.blocked:
                        s += '@'
                    elif node.cost == 1:
                        s += '.'
                    else:
                        s += str(node.cost)
                s += '\n'
                file.write(s)
        print(f'Karttatiedosto {self.fname} talletettu')
