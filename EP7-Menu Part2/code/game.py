import pygame

from keylistener import KeyListener
from map import Map
from player import Player
from screen import Screen
from controller import Controller
from option import Option
from save import Save
from text import Text
from sql import SQL


class Game:
    def __init__(self) -> None:
        self.running: bool = True
        self.screen: Screen = Screen()
        self.controller = Controller()
        self.sql = SQL()
        self.map: Map = Map(self.screen, self.controller, self.sql)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.screen, self.controller, 512, 288, self.keylistener)
        self.map.add_player(self.player)
        self.save = Save("save_0", self.map, self.sql)
        self.option = Option(self.screen, self.controller, self.map, "fr", self.save, self.keylistener, self.sql)

        self.click: tuple | None = None

    def run(self) -> None:
        while self.running:
            self.handle_input()
            if not self.player.menu_option:
                self.map.update()
            else:
                self.option.update(self.click)
            self.screen.update()

    def handle_input(self) -> None:
        self.click = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)
            elif event.type == 1026:
                self.click = pygame.mouse.get_pos()
