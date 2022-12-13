import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400,400))

def getKey(keyName):
    ans = False
    for eve in pygame.event.get():
        pass
    keyInput = pygame.key.get_pressed()
    mykey = getattr(pygame, 'K_{}'.format(keyName))  #K_{LEFT},K_{RIGHT}....etc
    if keyInput[mykey]:
        ans = True
    pygame.display.update()    
    return ans

def main():
    if(getKey("LEFT")):
        print('LEFT')
    if(getKey("RIGHT")):
        print('RIGHT')
    

if __name__ == '__main__':
    init()
    while True:
        main()
