import pygame as pg

pg.init()
pg.font.init()

class private:
    screen = None
    screenSize = [0, 0]
    frameRate = 60

    objectPosition = {}
    objects = {}

    time = []

class pygame:
    def screen(size):
        private.screen = pg.display.set_mode(size, pg.RESIZABLE)
        private.screenSize = size
    def setFrameRate(rate): private.frameRate = rate
    def update(color=[255, 255, 255]):
        screen = private.screen
        if not screen == None: pg.display.update(), screen.fill(color)
        # events
        if not screen == None:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    private.screen = None
                    pg.time.Clock().tick(private.frameRate)
                    return False
        else: 
            pg.time.Clock().tick(private.frameRate)
            return True
        pg.time.Clock().tick(private.frameRate)
        return True
    def rect(position=[0, 0, 0, 0], color=[255, 0, 0]): pg.draw.rect(private.screen, color, position)
    def circle(position=[0, 0, 0, 0], color=[255, 0, 0]): pg.draw.circle(private.screen, color, [position[0], position[1]], position[2])
    def text(position=[0,0], text="Hello, World!", size=24, color=[255, 0, 0]):
        font = pg.font.SysFont("makerpy/libaries/ARIAL.TTF", size)
        img = font.render(text, True, color)
        private.screen.blit(img, (20, 20))
    
    def getScreenSize(): return private.screenSize
    def getScreen(): return private.screen
    def killScreen(): private.screen = None

    def killObject(name): del private.objects[name]
    def killAllObjects(): private.objects = {}
    def customObject(name="", value=None): private.objects[name] = value
    def rectObject(name="", position=[0, 0, 0, 0], color=[255, 0, 0]): private.objects[name] = pg.draw.rect(private.screen, color, position)
    def circleObject(name="", position=[0, 0, 0, 0], color=[255, 0, 0]): private.objects[name] = pg.draw.circle(private.screen, color, [position[0], position[1]], position[2])
    def textObject(name="", position=[0,0], text="Hello, World!", size=24, color=[255, 0, 0]):
        font = pg.font.SysFont("makerpy/libaries/ARIAL.TTF", size)
        img = font.render(text, True, color)
        private.objects[name] = img

    def drawObject(name): private.screen.blit(private.objects[name], (20, 20))
    def drawAllObjects():
        for name in private.objects:
            private.screen.blit(private.objects[name], (20, 20))
    def getObject(name): return private.objects[name]

    def getMousePos():
        pos = pg.mouse.get_pos()
        return [pos[0], pos[1]]
    def getMouseClick():
        click = pg.mouse.get_pressed()
        return [click[0], click[1], click[2]]
        # what means what
        # 0 = left
        # 1 = right
        # 2 = middle
    
    def button(position=[0, 0, 0, 0], button=0):
        # return true if clicked inside position
        if pg.getMouseClick()[button] == 1:
            if pg.getMousePos()[0] > position[0] and pg.getMousePos()[0] < position[0] + position[2]:
                if pg.getMousePos()[1] > position[1] and pg.getMousePos()[1] < position[1] + position[3]:
                    return True
                else: return False
            else: return False
        else: return False
    
    def setTime(time=0, item=0):
        private.time[item] = time
    def getTime(item=0, all=False):
        if all == False: private.time[item] -= 1
        else:
            for i in range(len(private.time)):
                private.time[i] -= 1
        if private.time[item] == 0: return True
        else: return False