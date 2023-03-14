import pygame as pg
from sys import exit

class MenuOption:
    def __init__(self, y, text: str, color, altcolor, action: int) -> None:
        font1 = pg.font.SysFont("Arial", 40)
        self.cmd = action
        self.img = font1.render(text, True, color)
        self.altimg = font1.render(text, True, altcolor)
        self.rect = self.img.get_rect(topleft=(240-self.img.get_width()/2, y))
        self.y = y
        self.hovering = False
    
class Menu:

    def __init__(self) -> None:
        pg.init()
        self.display = pg.display.set_mode((480, 500))
        self.running = True
        self.helpscreen = False
        self.x = 0
        self.y = 0
        font = pg.font.SysFont("Impact", 60)
        font1 = pg.font.SysFont("Arial", 40)
        self.title = font.render("RoboGame!", True, (255,0,0))

        play = MenuOption(200, "Start Game", (100,100,100), (255,255,255), 1,)
        help = MenuOption(250, "How to Play", (100,100,100), (255,255,255), 2)
        quit_game = MenuOption(300, "Quit Game", (100,100,100), (255,255,255), 3)

        self.colliders = [play, help, quit_game]
        self.helpscreentext = [font1.render("WASD to move", True, (200,200,200)), font1.render("Avoid the ghosts", True, (200,200,200)), font1.render("Collect coins", True, (200,200,200)), font1.render("SPACE to enter portal", True, (200,200,200))]


        self.clock = pg.time.Clock()

    def draw(self, option: MenuOption):
        if option.hovering:
            self.display.blit(option.altimg, (240-option.img.get_width()/2, option.y))
        else:
            self.display.blit(option.img, (240-option.img.get_width()/2, option.y))

    def action(self, option: MenuOption):
        match option.cmd:
            case 1:
                self.running = False
            case 2:
                self.helpscreen = True
            case 3:
                pg.quit()
                exit()

    def run(self): 
        
        while self.running:
            isClicking = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    isClicking = True

            if not self.helpscreen:
                i = 0
                #check for hovering mouse over menu text
                cursor = pg.mouse.get_pos()

                self.display.fill((30,30,30))
                self.display.blit(self.title, (240 - self.title.get_width()/2, 50))

                for collider in self.colliders:
                    if collider.rect.collidepoint(cursor):
                        collider.hovering = True
                        if isClicking:
                            self.action(collider)
                    else:
                        collider.hovering = False
                    
                    self.draw(collider)
            else:
                
                if i <= 20:
                    i += 1
                self.display.fill((30,30,30))
                height = 150
                for text in self.helpscreentext:
                    self.display.blit(text, (240-text.get_width()/2,height))
                    height += 50

            if isClicking and i >= 20:
                self.helpscreen = False


            pg.display.flip()
            self.clock.tick(30)

        pg.quit()

if __name__ == "__main__":
    Menu().run()
    print("gaming")
