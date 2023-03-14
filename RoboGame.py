# TEE PELI TÄHÄN
from mainmenu import Menu
from Game import RoboGame

while True:
    Menu().run()
    RoboGame((1280, 720)).run()