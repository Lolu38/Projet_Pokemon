import json
import os
import sys

import pygame
import datetime

from controller import Controller
from map import Map
from player import Player
from screen import Screen
from sql import SQL
from save import Save
from tool import Tool
from keylistener import KeyListener
from text import Text
from config import image_pause


class Option:
    def __init__(self, screen: Screen, controller: Controller, map: Map, language: str, save: Save,
                 keylistener: KeyListener, sql: SQL):
        self.buttons_options = None
        self.screen: Screen = screen
        self.controller: Controller = controller
        self.map: Map = map
        self.language: str = language
        self.save: Save = save
        self.sql: SQL = sql
        self.player: Player = self.map.player
        self.keylistener = keylistener

        self.full_background: pygame.Surface = pygame.surface.Surface(self.screen.get_size())
        self.image_background: pygame.Surface | None = None
        self.initialization: bool = False

        self.background_color = (4, 18, 18)
        self.background: pygame.Surface = pygame.surface.Surface((self.screen.get_size()[0], 80))
        self.background.fill(self.background_color)

        self.images_pauses = {key: image_pause[key].convert_alpha() for key in image_pause.keys()}
        self.unlockedoption = {
            "Quit": "Quitter",
            "Save": "Sauvegarder",
            "Inventory": "Inventaire",
            "Map": "Carte",
            "Pokemon": "Pokémon",
            "Option": "Options",
            "Pokedex": "Pokédex",
        }
        self.selected = "menu"

        self.image_map = pygame.transform.scale_by(pygame.image.load("../../assets/settings/navimap.png"),
                                                   1).convert_alpha()
        self.map_decale_x = 0
        self.map_decale_y = 0
        self.pos_mouse_before = None

        self.image_box = pygame.image.load("../../assets/settings/box.png").convert_alpha()
        self.nodata = pygame.transform.scale(pygame.image.load("../../assets/settings/nodata.png").convert_alpha(), (128, 128))

    def update(self, click=None):
        if not self.initialization:
            self.initialization = True
            self.initialize()
        self.draw()
        self.check_action(click)
        self.check_end()

    def initialize(self):
        self.image_background = self.screen.image_screen()
        self.image_background = Tool.blur(self.image_background, 8)

    def draw(self):
        self.player.update_ingame_time()
        self.full_background.blit(self.image_background, (0, 0))
        self.drawcontent()
        self.full_background.blit(self.background, (0, 0))
        self.full_background.blit(self.background, (0, self.screen.get_size()[1] - self.background.get_height()))

        text, pos = Text.set_text(Text.get_date(), 16, 24, 24, (20, 87, 70), "left")
        self.full_background.blit(text, pos)

        text, pos = Text.set_text(Text.get_hour(), 16, 56, 24, (20, 87, 70), "left")
        self.full_background.blit(text, pos)

        text, pos = Text.set_text(Text.get_time_player(self.player.ingame_time), self.screen.get_width() - 16, 24, 25,
                                  (20, 87, 70), "right")
        self.full_background.blit(text, pos)

        text, pos = Text.set_text(str(self.player.pokedollars) + " P", self.screen.get_width() - 16, 56, 25,
                                  (20, 87, 70), "right")
        self.full_background.blit(text, pos)

        text, pos = Text.set_text("Lieu actuel:", self.screen.get_width() - 32, self.screen.get_height() - 56, 25,
                                  (20, 87, 70), "right")
        self.full_background.blit(text, pos)
        try:
            text, pos = Text.set_text(self.map.name, self.screen.get_width() - 32,
                                      self.screen.get_height() - 25, 25, (179, 176, 71), "right")
            self.full_background.blit(text, pos)
        except:
            pass

        text, pos = Text.set_text("Aucune quête suivie", self.screen.get_width() / 2, self.screen.get_height() - 40,
                                  25,
                                  (20, 87, 70), "center")
        self.full_background.blit(text, pos)
        self.drawIcons()
        self.screen.get_display().blit(self.full_background, (0, 0))

    def check_end(self):
        if self.keylistener.key_pressed(self.controller.get_key("quit")):
            self.initialization = False
            self.player.menu_option = False
            self.keylistener.remove_key(self.controller.get_key("quit"))
            return

    def check_action(self, click):
        if click is not None:
            for k, v in self.buttons_options.items():
                if v.collidepoint(click):
                    if k == "quit":
                        pygame.quit()
                        sys.exit()
                    elif k == "save":
                        self.selected = "save"
                    elif k == "inventory":
                        self.selected = "inventory"
                    elif k == "map":
                        self.selected = "menu"
                    elif k == "pokemon":
                        self.selected = "pokemon"
                    elif k == "option":
                        self.selected = "option"
                    elif k == "pokedex":
                        self.selected = "pokedex"
        if self.selected == "menu":
            self.check_map()
        # if self.keylistener and self.selected == "save" and pygame.K_c in self.keylistener.get():
        #     self.save = True

    def drawIcons(self):
        self.buttons_options = {}
        nb_image_pause = len(self.unlockedoption.keys())
        i = 0
        for key, value in self.images_pauses.items():
            self.buttons_options[key] = pygame.Rect(self.screen.get_width() / 2 - (nb_image_pause * 96) / 2 + (96 * i)
                                                    + 8, 0, 96, 80)
            i += 1
        i = 0
        for key, value in self.images_pauses.items():
            if key.title() in self.unlockedoption.keys():
                color = (20, 87, 70)
                if self.buttons_options[key].collidepoint(pygame.mouse.get_pos()) or (
                        (self.selected == "menu" and key == "map") or self.selected == key):
                    self.full_background.blit(value,
                                              (
                                                  self.screen.get_width() / 2 - (nb_image_pause * 96) / 2 + (
                                                              96 * i) + 40,
                                                  8))
                    color = (106, 176, 126)
                    if (self.selected == "menu" and key == "map") or self.selected == key:
                        rect = pygame.Rect(self.screen.get_width() / 2 - (nb_image_pause * 96) / 2 + (96 * i) + 24,
                                           76,
                                           64, 4)
                        pygame.draw.rect(self.full_background, (106, 176, 126), rect)
                else:
                    image_alpha_128 = value.copy()
                    image_alpha_128.set_alpha(128)
                    self.full_background.blit(image_alpha_128,
                                              (
                                                  self.screen.get_width() / 2 - (nb_image_pause * 96) / 2 + (
                                                              96 * i) + 40,
                                                  8))

                text, pos = Text.set_text(key.title(),
                                          self.screen.get_width() / 2 - (nb_image_pause * 96) / 2 + (96 * i) + 56,
                                          64,
                                          24,
                                          color, "center")
                self.full_background.blit(text, pos)
                i += 1

    def drawcontent(self):
        if self.selected == "menu":
            self.drawMap()
        elif self.selected == "save":
            self.drawSave()
        elif self.selected == "inventory":
            self.drawInventory()
        elif self.selected == "pokemon":
            self.drawPokemon()
        elif self.selected == "option":
            self.drawOption()
        elif self.selected == "pokedex":
            self.drawPokedex()

    def drawMap(self):
        self.full_background.blit(self.image_map, (0 + self.map_decale_x, 80 + self.map_decale_y))

    def drawSave(self):
        surface = pygame.Surface((self.screen.get_width() / 3, 64))
        surface.fill((1, 47, 43))
        self.screen.blit(surface, (self.screen.get_width() / 2 - self.screen.get_width() / 6,
                                   self.screen.get_height() / 4 - 24))

        if False:
            pass
        # save
        else:
            textsurface = pygame.Surface((self.screen.get_width() / 2.5, self.screen.get_height() / 12))
            textsurface.fill((1, 47, 43))
            text, pos = Text.set_text("Sauvegarde", textsurface.get_width() / 2, textsurface.get_height() / 2,
                                       32,
                                       (255, 255, 255), "center")
            textsurface.blit(text, pos)
            self.full_background.blit(textsurface,(self.screen.get_width() / 2 - textsurface.get_width() / 2, self.screen.get_height() / 5))
            surface = pygame.Surface((self.screen.get_width() / 2.5, self.screen.get_height() / 2.5))
            surface.fill((1, 47, 43))
            surface.blit(self.nodata, (surface.get_width() / 2 - self.nodata.get_width() / 2,
                                                    surface.get_height() / 2 - self.nodata.get_height() / 2 - 32))

            texts = Text.split_text(
                "Vous pouvez sauvegarder sur cet emplacement sans avoir peur d'écraser une autre partie, ouf !",
                length=50)
            for i in range(len(texts[0])):
                text, pos = Text.set_text(texts[0][i], 16,
                                          (surface.get_height() - 64) + 24 * i,
                                           24,
                                           (106, 176, 126), "left")
                surface.blit(text, pos)

                self.full_background.blit(surface, (self.screen.get_width() / 2 - surface.get_width() / 2,
                                                    self.screen.get_height() / 2 - self.screen.get_height() / 6))

    def drawInventory(self):
        self.full_background.blit(self.image_box, (self.screen.get_width() / 2 - self.image_box.get_width() / 2, self.screen.get_height() / 2 - self.image_box.get_height() / 2))

    def drawPokemon(self):
        pass

    def drawOption(self):
        pass

    def drawPokedex(self):
        pass

    def check_map(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pos_mouse_before is not None:
                if self.pos_mouse_before != pygame.mouse.get_pos():
                    if pygame.mouse.get_pos()[0] - self.pos_mouse_before[
                        0] + self.map_decale_x + self.image_map.get_width() > self.screen.get_width() and \
                            pygame.mouse.get_pos()[0] - self.pos_mouse_before[0] + self.map_decale_x < 0:
                        self.map_decale_x += pygame.mouse.get_pos()[0] - self.pos_mouse_before[0]
                    if pygame.mouse.get_pos()[1] - self.pos_mouse_before[
                        1] + self.map_decale_y + self.image_map.get_height() > self.screen.get_height() - 160 and \
                            pygame.mouse.get_pos()[1] - self.pos_mouse_before[1] + self.map_decale_y < 0:
                        self.map_decale_y += pygame.mouse.get_pos()[1] - self.pos_mouse_before[1]
        self.pos_mouse_before = pygame.mouse.get_pos()
