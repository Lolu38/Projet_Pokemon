import re
import datetime

import pygame


class Text:
    @staticmethod
    def set_text(string: str, x, y, font_size=30, color=(255, 255, 255), center="center", type="Light",
                 font_name="Verlag"):
        try:
            font = pygame.font.Font(f"../../assets/fonts/{font_name}-{type}.ttf", font_size)
        except:
            try:
                font = pygame.font.Font(f"../../assets/fonts/{font_name}-{type}.otf", font_size)
            except Exception as e:
                print(e)

        pattern = r'<color=([A-Fa-f0-9]{6})>(.*?)</color>|<bold>(.*?)</bold>'
        parts = re.split(pattern, string)
        texts = []
        for i in range(0, len(parts), 4):
            if parts[i]:
                text = font.render(parts[i], True, color)
                texts.append(text)
            if i + 2 < len(parts) and parts[i + 1]:
                hex_color = parts[i + 1]
                colored_text = parts[i + 2]
                rgb_color = tuple(int(hex_color[j:j + 2], 16) for j in (0, 2, 4))
                text = font.render(colored_text, True, rgb_color)
                texts.append(text)
            if i + 3 < len(parts) and parts[i + 3]:
                bold_text = parts[i + 3]
                bold_font = pygame.font.Font(f"../../assets/fonts/{font_name}-Bold.otf", font_size)
                text = bold_font.render(bold_text, True, color)
                texts.append(text)

        total_width = sum(text.get_width() for text in texts)
        max_height = max(text.get_height() for text in texts)

        text_surface = pygame.Surface((total_width, max_height), pygame.SRCALPHA)

        x_offset = 0
        for text in texts:
            text_surface.blit(text, (x_offset, 0))
            x_offset += text.get_width()

        textRect = text_surface.get_rect()
        if center.lower() == "center":
            textRect.center = (x, y)
        elif center.lower() == "left":
            textRect.midleft = (x, y)
        elif center.lower() == "right":
            textRect.midright = (x, y)

        return text_surface, textRect

    @staticmethod
    def get_date() -> str:
        date = ""
        date += str(datetime.datetime.now().day) + "/"
        date += str(datetime.datetime.now().month) + "/" if datetime.datetime.now().month >= 10 else "0" + str(
            datetime.datetime.now().month) + "/"
        date += str(datetime.datetime.now().year)
        return date

    @staticmethod
    def get_hour() -> str:
        hour = ""
        hour += str(datetime.datetime.now().hour) + ":"
        hour += str(datetime.datetime.now().minute) if datetime.datetime.now().minute >= 10 else "0" + str(
            datetime.datetime.now().minute)
        hour += ":" + str(datetime.datetime.now().second) if datetime.datetime.now().second >= 10 else ":0" + str(
            datetime.datetime.now().second)
        return hour

    @staticmethod
    def get_time_player(time_played: datetime.timedelta) -> str:
        timeplayed = ""
        timeplayed += str(time_played.seconds // 3600) + ":"
        timeplayed += str((time_played.seconds // 60) % 60) if (
               time_played.seconds // 60) % 60 >= 10 else "0" + str(
                    (time_played.seconds // 60) % 60) + ":"
        timeplayed += str(
            time_played.seconds % 60) if time_played.seconds % 60 >= 10 else "0" + str(
            time_played.seconds % 60)
        return timeplayed

    @staticmethod
    def split_text(text, player="", length=120):
        # Séparer le texte en mots
        words = text.split()

        # Initialiser la liste des groupes de lignes
        line_groups = []

        # Initialiser le groupe de lignes courant
        current_line_group = []

        # Initialiser la ligne courante
        current_line = ""
        current_length = 0

        # Pour chaque mot...
        for word in words:
            # Si le mot est égal au caractère '£', ajouter la ligne courante au groupe de lignes courant et créer une nouvelle ligne
            if word == '£':
                current_line_group.append(current_line)
                current_line = ""
                current_length = 0
            # Si le mot est égal au caractère '§', ajouter le groupe de lignes courant à la liste des groupes de lignes et créer un nouveau groupe de lignes et une nouvelle ligne
            elif word == '§':
                current_line_group.append(current_line)
                line_groups.append(current_line_group)
                current_line_group = []
                current_line = ""
                current_length = 0
            # Si le mot est égal au caractère 'ù', remplacer le mot par le joueur
            elif word == 'ù':
                if current_length + len(player) + 1 <= length:
                    current_line += player + " "
                    current_length += len(player) + 1
                # Sinon, ajouter la ligne courante au groupe de lignes courant et créer une nouvelle ligne
                else:
                    current_line_group.append(current_line)
                    current_line = player + " "
                    current_length = len(player)
            # Si le mot ne dépasse pas la limite de longueur de ligne, l'ajouter à la ligne courante
            elif current_length + len(word) + 1 <= length:
                current_line += word + " "
                current_length += len(word) + 1
            # Sinon, ajouter la ligne courante au groupe de lignes courant et créer une nouvelle ligne
            else:
                current_line_group.append(current_line)
                current_line = word + " "
                current_length = len(word)

            # Si le groupe de lignes courant contient 3 lignes, l'ajouter à la liste des groupes de lignes et créer un nouveau groupe de lignes
            # if len(current_line_group) == 3:
            #    line_groups.append(current_line_group)
            #    current_line_group = []

        # Ajouter la dernière ligne au groupe de lignes courant (si elle existe)
        if current_line:
            current_line_group.append(current_line)

        # Ajouter le dernier groupe de lignes à la liste des groupes de lignes (si il existe)
        if current_line_group:
            line_groups.append(current_line_group)

        return line_groups
