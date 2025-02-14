import pygame;
import random;

pygame.init();

display = pygame.display.set_mode([1280,720]);
display.fill((0,0,0));

running = True;

while running:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            running = False;
    print("Tick", pygame.time.get_ticks());
    pygame.event.pump();
    pygame.display.flip();
    pygame.time.wait(100);