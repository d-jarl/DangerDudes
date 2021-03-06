###########################################################################
#                                                                         #
#                                                                         #
#                               ddclient                                  #
#                                                                         #
#                                                                         #
###########################################################################
#                                                                         #
#   Communication to ddserver                                             #
#      Connect()                                                          #
#      ActionRequest()                                                    #
#                                                                         #
###########################################################################
#                                                                         #
#   high level functions                                                  #
#      Move()                                                             #
#                                                                         #
############################################################################
import os, sys, pygame
from erlport import Protocol, Port, String
from threading import Thread
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Danger dudes')
pygame.mouse.set_visible(0)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class DD(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ddf.bmp', -1)
        self.rect.topleft = x, y
        
    def update(self):
        pass

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name, (255,255,255))
        self.rect.topleft = x, y

    def update(self):
        pass
        
class ddclient(Protocol):
    _port = None
    _hero = DD(400,300)
    allsprites = pygame.sprite.RenderPlain(_hero)

    def sendRequest(action):
        if self._port:
            self._port.write(action)
        
    def handle_init(self,port):
        self._port=port   

    def handle_worldinfo(self,worldinfo):
        self.allsprites.empty()
        world=worldinfo.splitlines()
        
        for i in world:            
            objectInfo = i.split(' ')
            newObject = objectInfo[0]
            x = int(objectInfo[1])
            y = int(objectInfo[2])

            if newObject == 'Player':
                player = DD(x, y)
                player.add(self.allsprites)
            elif newObject == 'Stone':
                stone = Block(x, y, 'block_circle.bmp')
                stone.add(self.allsprites)

def main():   
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_UP:
                client.sendRequest('UP')
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                client.sendRequset('RIGHT')
            elif event.type == KEYDOWN and event.key == K_DOWN:
                client.sendRequset('DOWN')
            elif event.type == KEYDOWN and event.key == K_LEFT:
                client.sendRequset('LEFT')
            elif event.type == KEYUP and event.key == K_UP:
                client.sendRequset('UP_0')
            elif event.type == KEYUP and event.key == K_RIGHT:
                client.sendRequset('RIGHT_0')
            elif event.type == KEYUP and event.key == K_DOWN:
                client.sendRequset('DOWN_0')
            elif event.type == KEYUP and event.key == K_LEFT:
                client.sendRequset('LEFT_0')        
    
        screen.blit(background, (0, 0)) 
        client.allsprites.draw(screen)
        pygame.display.flip()
        
class listener(Thread):
    _client = None
    def __init__(self, client):
        self._client = client
        Thread.__init__(self)

    def run(self):
        self._client.run(Port(use_stdio=True))
        
if __name__ == "__main__":
    client = ddclient()
    listener = listener(client)
    listener.daemon = True
    listener.start()
    main()
