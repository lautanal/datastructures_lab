import os, sys, pygame

def mapwrite(self, fname):
    """Kartan kirjoitus tiedostoon.

    Args:
        fname: Tiedoston nimi
    """
    dirname = os.path.dirname(__file__)
    data_file_path = os.path.join(dirname, '..', 'data', 'maps', fname)            
    with open(data_file_path, 'w') as file:
        for row in self.map.nodes:
            s = ''
            for node in row:
                if node.blocked:
                    s += 'B'
                else:
                    s += str(node.cost)
            s += '\n'
            file.write(s)
    print(f'Karttatiedosto {fname} talletettu')

pygame.init()
size = width, height = 350, 275
screen = pygame.display.set_mode(size)
dirname = os.path.dirname(__file__)
img_file_path = os.path.join(dirname, '..', 'testmaps', 'test.png')            
image = pygame.image.load(img_file_path)
image_rect = image.get_rect()

screen.fill((0,0,0))
screen.blit(image, image_rect)
screensurf = pygame.display.get_surface()

fname = '5.map'
dirname = os.path.dirname(__file__)
data_file_path = os.path.join(dirname, '..', 'data', 'maps', fname)            
with open(data_file_path, 'w') as file:
    for i in range(height):
        s = ''
        for j in range(width):
            val = screensurf.get_at((j,i))[0] // 24
            if val > 7:
                s += 'B'
            else:
                s += str(val)
        s += '\n'
        file.write(s)

#while 1:
#
#  for event in pygame.event.get():
#     if event.type == pygame.MOUSEBUTTONDOWN :
#        mouse = pygame.mouse.get_pos()
#        pxarray = pygame.PixelArray(screensurf)
#        pixel = pygame.Color(pxarray[mouse[0],mouse[1]])
#        print(mouse)
#        print(screensurf.get_at(mouse))
#  pygame.display.flip()
