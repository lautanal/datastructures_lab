import sys, pygame
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
image = pygame.image.load("./test.png")
image_rect = image.get_rect()

screen.fill((0,0,0))
screen.blit(image, image_rect)
screensurf = pygame.display.get_surface()

#pxarray = pygame.PixelArray(screensurf)
#for i in range(2):
#    for j in range(20):
#        pixel = pygame.Color(pxarray[i,j])
#        print((i,j))
#        print(pixel)
#        print(screensurf.get_at((i,j)))

while 1:

  for event in pygame.event.get():
     if event.type == pygame.MOUSEBUTTONDOWN :
        mouse = pygame.mouse.get_pos()
        pxarray = pygame.PixelArray(screensurf)
        pixel = pygame.Color(pxarray[mouse[0],mouse[1]])
        print(mouse)
        print(pixel)
        print(screensurf.get_at(mouse))

pygame.display.flip()