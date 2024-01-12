import pygame

image_pause: dict[str:pygame.Surface] = {
            "quit": pygame.transform.scale(pygame.image.load("../../assets/settings/quit.png"),
                                           (32, 32)),
            "save": pygame.transform.scale(pygame.image.load("../../assets/settings/save.png"),
                                           (32, 32)),
            "inventory": pygame.transform.scale(
                pygame.image.load("../../assets/settings/inventory.png"),
                (32, 32)),
            "map": pygame.transform.scale(pygame.image.load("../../assets/settings/map.png"),
                                          (32, 32)),
            "pokemon": pygame.transform.scale(pygame.image.load("../../assets/settings/pokemon.png"),
                                              (32, 32)),
            "option": pygame.transform.scale(pygame.image.load("../../assets/settings/option.png"),
                                             (32, 32)),
            "pokedex": pygame.transform.scale(pygame.image.load("../../assets/settings/pokedex.png"),
                                              (32, 32))}