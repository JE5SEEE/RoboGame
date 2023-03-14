import pygame
from random import randint, choice

assets = {"Portal": pygame.image.load("ovi.png"), "Coin": pygame.image.load("kolikko.png"), "Robo": pygame.image.load("robo.png"), "Ghost": pygame.image.load("hirvio.png")}

class Robo(pygame.sprite.Sprite):
    def __init__(self, coords) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.hp:int = 100
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.speed = 3
        self.image = assets["Robo"]
        self.rect = self.image.get_rect(topleft=coords)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, coords, speed) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["Ghost"]
        self.spd = speed
        self.rect = self.image.get_rect(topleft=coords)

class Coin(pygame.sprite.Sprite):
    def __init__(self, coords) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["Coin"]
        self.rect = self.image.get_rect(topleft = coords)

class Portal(pygame.sprite.Sprite):
    def __init__(self, coords) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["Portal"]
        self.rect = self.image.get_rect(topleft=coords)

class GameData:
    def __init__(self, resolution) -> None:
        self.player = Robo((resolution[0]/3 - assets["Robo"].get_width()/2, resolution[1]/2 - assets["Robo"].get_height()/2))
        self.ghosts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.portals = pygame.sprite.GroupSingle(Portal((resolution[0]/1.5 - assets["Portal"].get_width()/2, resolution[1]/2 - assets["Portal"].get_height()/2)))
        self.ghostspeed = 1
        self.spawnrate = 1
        self.score = 0
        self.level = 0
        self.font = pygame.font.SysFont("Arial", 24)
        font1 = pygame.font.SysFont("Impact", 60)
        self.scoretext = self.font.render("Score:", True, (200,200,200))
        self.leveltext = self.font.render("Level:", True, (200,200,200))
        self.scorenumber = self.font.render(str(self.score), True, (200,200,200))
        self.levelnumber = self.font.render(str(self.level), True, (200,200,200))    
        self.gameovertext = font1.render("Game Over!", True, (255,0,0))
        self.gameovertext_1 = self.font.render("Press ESCAPE to continue", True, (200,200,200))

class RoboGame:
    def __init__(self, resolution) -> None:
        pygame.init()
        self.data = GameData(resolution)
        self.resolution = resolution
        self.display = pygame.display.set_mode((resolution))
        self.gameover = False
        self.running = True
        self.clock = pygame.time.Clock()

    def spawnObjects(self):
        
        for _ in range(2,6):
            self.data.coins.add(Coin((randint(40, self.resolution[0] - assets["Coin"].get_width()-40), randint(40, self.resolution[1]-40-assets["Coin"].get_height()))))

        self.data.portals.add(Portal((randint(40, self.resolution[0]-assets["Portal"].get_width()-40), randint(40, self.resolution[1]-40-assets["Portal"].get_height()))))

    def spawnGhost(self, spd):

        choices = [(choice(range(10, self.resolution[0] - 10 - assets["Ghost"].get_width())), -10 - assets["Ghost"].get_height()), (choice(range(10, self.resolution[0] - 10 - assets["Ghost"].get_width())), self.resolution[1] + 10), (-10 - assets["Ghost"].get_width(), choice(range(40, self.resolution[1] - 40 - assets["Ghost"].get_height()))), (self.resolution[0] + 10, choice(range(40, self.resolution[1] - 40 - assets["Ghost"].get_height())))]
        speeds = [(0, spd), (0, -spd), (spd, 0), (-spd, 0)]
        rand = randint(0,3)
        self.data.ghosts.add(Ghost(choices[rand], speeds[rand]))

    def updatescore(self):
        self.data.scorenumber = self.data.font.render(str(self.data.score), True, (200,200,200))
        self.data.levelnumber = self.data.font.render(str(self.data.level), True, (200,200,200))

    def levelup(self):

        self.data.score += self.data.level
        self.data.player.rect.x = self.resolution[0]/2 - assets["Robo"].get_width()/2
        self.data.player.rect.y = self.resolution[1]/2 - assets["Robo"].get_height()/2
        self.data.level += 1
        self.data.coins.empty()
        self.data.ghosts.empty()
        self.spawnObjects()
        self.updatescore()
        if self.data.level % 5 == 0:
            self.data.ghostspeed += 1
        if self.data.level % 10 == 0:
            self.data.spawnrate += 1

    def eventmanager(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.data.player.up = True
                if event.key == pygame.K_s:
                    self.data.player.down = True
                if event.key == pygame.K_a:
                    self.data.player.left = True
                if event.key == pygame.K_d:
                    self.data.player.right = True
                if event.key == pygame.K_SPACE:
                    self.data.player.space = True
                if event.key == pygame.K_ESCAPE:
                    self.running = False


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.data.player.up = False
                if event.key == pygame.K_s:
                    self.data.player.down = False
                if event.key == pygame.K_a:
                    self.data.player.left = False
                if event.key == pygame.K_d:
                    self.data.player.right = False
                if event.key == pygame.K_SPACE:
                    self.data.player.space = False

            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def draw(self):
        self.display.fill((50,50,50))
        
        ##### HUD BARS:
        pygame.draw.rect(self.display, (30,30,30), pygame.Rect(0, 40, self.resolution[0], self.resolution[1] - 80))
        ##### HUD ELEMENTS:
        pygame.draw.line(self.display, (150,0,0,), (28, 18), (132, 18), width= 24)
        pygame.draw.line(self.display, (255,0,0,), (30, 18), (30 + self.data.player.hp, 18), width= 20)
        self.display.blit(self.data.leveltext, (30, self.resolution[1]-7-self.data.leveltext.get_height()))
        self.display.blit(self.data.levelnumber, (90, self.resolution[1]-7-self.data.levelnumber.get_height()))
        self.display.blit(self.data.scoretext, (140, self.resolution[1]-7-self.data.scoretext.get_height()))
        self.display.blit(self.data.scorenumber, (207, self.resolution[1]-7-self.data.scorenumber.get_height()))

        ##### Coins and Portal
        self.data.coins.draw(self.display)
        self.data.portals.draw(self.display)

        self.display.blit(self.data.player.image, self.data.player.rect)
        for ghost in self.data.ghosts:
            self.display.blit(ghost.image, ghost.rect)

    def run(self):

        while self.running:

            if not self.gameover:
                self.eventmanager()

                ##### Movement Logic
                if self.data.player.up and self.data.player.rect.y > 40:
                    self.data.player.rect.y -= self.data.player.speed
                if self.data.player.down and self.data.player.rect.y + self.data.player.image.get_height() < self.resolution[1] - 40:
                    self.data.player.rect.y += self.data.player.speed
                if self.data.player.left and self.data.player.rect.x > 0:
                    self.data.player.rect.x -= self.data.player.speed
                if self.data.player.right and self.data.player.rect.x + self.data.player.image.get_width() < self.resolution[0]:
                    self.data.player.rect.x += self.data.player.speed
                
                ##### Spawn ghosts
                if randint(0,100) < self.data.spawnrate:
                    self.spawnGhost(self.data.ghostspeed)


                ##### Move ghosts
                for ghost in self.data.ghosts:
                    ghost.rect.x += ghost.spd[0]
                    ghost.rect.y += ghost.spd[1]

                ##### De-spawn Ghosts
                self.data.ghosts = pygame.sprite.Group([ghost for ghost in self.data.ghosts if not (ghost.rect.x < -100 or ghost.rect.x > self.resolution[0] + 100) or ghost.rect.y < -100 or ghost.rect.y > self.resolution[1] + 100])
                        

                ##### Collision
                coin = pygame.sprite.spritecollideany(self.data.player, self.data.coins)
                if coin is not None:
                    coin.kill()
                    self.data.score += 1
                    self.updatescore()

                portal = pygame.sprite.spritecollideany(self.data.player, self.data.portals)
                if self.data.player.space and portal is not None:
                    self.levelup()

                if pygame.sprite.spritecollideany(self.data.player, self.data.ghosts):
                    self.data.player.hp -= 1
                    if self.data.player.hp <= 0:
                        self.gameover = True
            
                ##### Draw screen
                self.draw()
            
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                ##### Draw screen
                self.draw()
                self.display.blit(self.data.gameovertext, (self.resolution[0]/2 - self.data.gameovertext.get_width()/2, self.resolution[1]/2 - self.data.gameovertext.get_height()/2 - 40))
                self.display.blit(self.data.gameovertext_1, (self.resolution[0]/2 - self.data.gameovertext_1.get_width()/2, self.resolution[1]/2 - self.data.gameovertext_1.get_height()/2 + 20))

            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = RoboGame((1280,720))
    game.run()