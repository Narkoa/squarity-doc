# https://i.postimg.cc/L6JjRr6f/snake-match-tileset.png
# https://i.postimg.cc/FsFvnhzN/snake-match-tileset.png
# https://i.postimg.cc/nhRHcFYk/snake-match-tileset.png

# Note pour plus tard : imgbb c'est de la daube comme hébergeur d'images.
# Ça, ça marche mieux. Et ça retaille pas stupidement les images sans prévenir.
# https://postimages.org/

# https://ldjam.com/events/ludum-dare/48/$237474/snakematch
# https://tinyurl.com/f7bbky72

"""
{
    "game_area": {
        "nb_tile_width": 10,
        "nb_tile_height": 15
    },
    "tile_size": 32,
    "img_coords": {
        "fruit_00": [0, 0],
        "fruit_01": [32, 0],
        "fruit_02": [64, 0],
        "block_00": [96, 0],
        "backgrnd": [128, 0],

        "snake_neck_up": [64, 0],
        "snake_neck_right": [64, 0],
        "snake_neck_down": [64, 0],
        "snake_neck_left": [64, 0],
        "snake_head_up": [64, 35],
        "snake_head_right": [96, 35],
        "snake_head_down": [128, 35],
        "snake_head_left": [160, 35],
        "fade_black": [192, 35],

        "snake_horiz": [0, 35],
        "snake_vertic": [32, 35],
        "snake_turn_up_left": [0, 70],
        "snake_turn_up_right": [32, 70],
        "snake_turn_down_right": [64, 70],
        "snake_turn_down_left": [96, 70],

        "match_up": [0, 105],
        "match_right": [32, 105],
        "match_down": [64, 105],
        "match_left": [96, 105],
        "match_horiz": [128, 105],
        "match_vertic": [160, 105],

        "arrow_deep_forbidden": [160, 0],
        "arrow_deep_go": [192, 0],

        "earth": [0, 140],
        "sky": [32, 140],
        "sky_unpassable": [32, 140],
        "back_home": [64, 140],
        "fruit_03": [96, 140],
        "fruit_04": [128, 140],
        "fruit_05": [160, 140],

        "bla": [0, 0]
    }
}
"""

"""

Snake-Match

Déplacez votre serpent et mangez les fruits.

Ne vous étonnez pas, au début, les fruits ne tombent pas,
et dès qu'on fait le premier mouvement, ils tombent.

C'est parce que j'ai pas fini de tout coder.

Le bouton d'action "1" permet d'aller plus profondément.
Mais ça fait bugger le serpent si vous lui faites faire des circuits bizarres !

Jusqu'ici c'est pas trop mal quand même.

"""

# On approche de la fin. C'est le moment de lister tout ce qu'il reste à faire:
# TODO au pluriel.

# X Le début du jeu, avec un décor de ciel et de terre.
# X quand on rewind le serpent et qu'on appuie encore une fois sur la flèche du haut, on revient au début du jeu et on recommence une partie.
# X petit icône "maison" avec flèche du haut dans l'interface, pour expliquer que ça fait repartir à la maison.
# X 3 types de fruits en plus.
# X le bouton d'action numéro 1 fait rewind le serpent. Pour aller plus vite quand on doit faire un grand rewind.
# X calculer la longueur du serpent et la limiter. Petit message si le serpent est au max et qu'on veut le faire avancer.
# X calculer la quantité de trucs que bouffe le serpent. Le limiter quand il est saturé. Avec un petit message.
# - des XP quand on mange et qu'on fait des matchs. Augmenter de niveau augmente sa longueur et sa capacité de bouffage. Petit message à chaque fois qu'on monte de niveau.
# - petit message quand on recommence, avec : nb d'XP gagné par les matchs, par le bouffage, et nombre d'XP restant avant le prochain niveau.
# - à la profondeur 1664, on trouve le but du jeu : Le Guide on Van-Random. Il est entouré de blocs. Il faut les détruire pour le sauver.
# - petit icône de message quand on affiche un message. Parce que les gens penseront pas forcément à regarder le texte dans la console.
# - un écran de fin.
# - le set_content_random change selon la profondeur : de plus en plus de blocs, et de plus en plus de type de fruits.
# - un type de fruit en plus parce que même avec 6, c'est trop facile. (surtout qu'au début, on les met pas tous)
# - calculer la profondeur et donner des XP quand on atteint certains seuils. Avec un petit message, comme d'hab'.
# - À un certain niveau, le serpent obtient le pouvoir de bouffer des blocs, mais ça lui coûte 10 points de bouffage.
# - Des putains de graphismes mieux que ce que j'ai fait là.
# - background qui change plus on va profond.
# - bug pourri au début du jeu. Si on recule le serpent il se réaffiche en partant du haut et pas de la gauche. Mais osef.

# Idées d'achievement pour plus tard :
# - Terminer un niveau avec à la fois l'estomac plein et la longueur max du serpent atteinte.
# - Terminer avec la longueur max atteinte, et un estomac très très vide (on a avancé en faisant pratiquement que des matchs)

import random

# Je mets 5 et pas 6 pour l'instant. Sinon, y'a rien qui va matcher et je vais galérer pour tester.
NB_FRUITS = 5

DEBUG = False


DIR_UP = 0
DIR_RIGHT = 2
DIR_DOWN = 4
DIR_LEFT = 6

DIR_FROM_EVENT = {"U": DIR_UP, "R": DIR_RIGHT, "D": DIR_DOWN, "L": DIR_LEFT}

OPPOSITE_DIR = {
    DIR_UP: DIR_DOWN,
    DIR_RIGHT: DIR_LEFT,
    DIR_DOWN: DIR_UP,
    DIR_LEFT: DIR_RIGHT,
}

DELAY_GRAVITY_MS = 250
ACTION_GRAVITY = f""" {{ "delayed_actions": [ {{"name": "apply_gravity", "delay_ms": {DELAY_GRAVITY_MS}}} ] }} """

DELAY_ANIM_MATCH = 100
ACTION_ANIM_MATCH = f""" {{ "delayed_actions": [ {{"name": "anim_match", "delay_ms": {DELAY_ANIM_MATCH}}} ] }} """

# Ha ha ha ! Fade to Black. Une subtile et lointaine référence
# à la suite du jeu vidéo Flash Back. Tout le monde s'en fout ? OK..
DELAY_FADE_TO_BLACK = 100
ACTION_FADE_TO_BLACK = f""" {{ "delayed_actions": [ {{"name": "anim_fade_to_black", "delay_ms": {DELAY_FADE_TO_BLACK}}} ] }} """


def message_to_player(strings):
    print("-" * 10)
    for string in strings:
        print(string)
    print("-" * 10)


class Tile:
    def __init__(self, game_model, x, y):
        self.game_model = game_model
        self.x = x
        self.y = y
        self.fruit = None
        self.block_type = None
        # snake_part est une string, correspondant directement
        # au gamobj du snake. (Pas besoin de se prendre plus la tête
        # que ça, à priori)
        self.snake_part = None
        self.game_objects = []
        self.gamobj_matches = []
        self.has_horizontal_match = False
        self.has_vertical_match = False
        self.gamobj_miscellaneous = None

    def set_random_content(self):
        """
        Place un élément au hasard, mais forcément quelque chose.
        On met pas un élément vide, parce que j'ai pas besoin de ça !
        """
        self.emptify()
        # TODO : ce sera pas comme ça du tout, car plus on va profondément
        # plus on a de chance de tomber sur des blocs.
        choice = random.randrange(NB_FRUITS + 1)
        if choice == 0:
            if self.game_model.deep_distance > 5:
                self.block_type = 0
            else:
                self.fruit = 0
        else:
            self.fruit = choice - 1
        self.render()

    def set_gamobj_miscellaneous(self, gamobj):
        self.gamobj_miscellaneous = gamobj
        self.render()

    def set_snake_part(self, snake_part):
        self.emptify()
        self.snake_part = snake_part
        self.render()

    def add_match(self, gamobj):
        self.gamobj_matches.append(gamobj)
        # TODO : c'est moche de gérer avec les gamobj,
        # on essaiera de faire mieux si on a le temps.
        if "right" in gamobj or "left" in gamobj or "horiz" in gamobj:
            self.has_horizontal_match = True
        else:
            self.has_vertical_match = True

    def clear_match(self):
        self.gamobj_matches = []
        self.has_horizontal_match = False
        self.has_vertical_match = False

    def render(self):
        if self.gamobj_miscellaneous is not None:
            self.game_objects[:] = [self.gamobj_miscellaneous]
        else:
            self.game_objects[:] = ["backgrnd"]
        if self.fruit is not None:
            gamobj_fruit = f"fruit_{self.fruit:02}"
            self.game_objects.append(gamobj_fruit)
        elif self.block_type is not None:
            gamobj_block = f"block_{self.block_type:02}"
            self.game_objects.append(gamobj_block)
        elif self.snake_part is not None:
            self.game_objects.append(self.snake_part)

        self.game_objects += self.gamobj_matches * self.game_model.match_show_gamobj

    def does_stop_gravity(self):
        # Plus tard, on aura peut-être des blocs qui tombent.
        # Donc je checke explicitement le numéro de type.
        if self.block_type == 0:
            return True
        if self.snake_part is not None:
            return True
        if self.gamobj_matches:
            # Les tiles en cours de match ne peuvent pas tomber.
            # Ça fait bizarre, car pendant quelques fractions de
            # secondes, on verra des fruits qui restent en l'air
            # pendant qu'ils se matchent. Mais ça simplifie beaucoup de choses.
            return True
        return False

    def is_empty(self):
        return all(
            (self.fruit is None, self.block_type is None, self.snake_part is None)
        )

    def get_content_from_other_tile(self, other):
        self.fruit = other.fruit
        self.block_type = other.block_type
        self.snake_part = other.snake_part
        self.gamobj_matches = other.gamobj_matches
        self.has_horizontal_match = other.has_horizontal_match
        self.has_vertical_match = other.has_vertical_match
        self.gamobj_miscellaneous = other.gamobj_miscellaneous

        self.render()

    def emptify(self):
        self.fruit = None
        self.block_type = None
        self.snake_part = None
        self.gamobj_matches = []
        # emptify ne supprime pas les gamobj_miscellaneous. Parce que voilà.
        self.render()


class Snake:

    MOVE_RESULT_FAIL_BLOCKED = 0
    MOVE_RESULT_FAIL_TOO_SHORT = 1
    MOVE_RESULT_FAIL_STOMACH_FULL = 2
    MOVE_RESULT_OK = 3

    GAMOBJ_FROM_HEAD_DIR = {
        DIR_UP: "snake_head_up",
        DIR_RIGHT: "snake_head_right",
        DIR_DOWN: "snake_head_down",
        DIR_LEFT: "snake_head_left",
    }

    # clé : tuple de 2 éléments.
    #  - la direction au début de la tile du body.
    #  - la direction à la fin de la tile du body.
    # Il y a des combinaisons impossibles (toutes celles où on
    # fait demi-tour, par exemple RIGHT, RIGHT). Osef, on met tout.
    GAMOBJ_BODY_FROM_DIRS = {
        (DIR_UP, DIR_UP): "snake_vertic",
        (DIR_UP, DIR_RIGHT): "snake_turn_up_right",
        (DIR_UP, DIR_DOWN): "snake_vertic",
        (DIR_UP, DIR_LEFT): "snake_turn_up_left",
        (DIR_RIGHT, DIR_UP): "snake_turn_up_right",
        (DIR_RIGHT, DIR_RIGHT): "snake_horiz",
        (DIR_RIGHT, DIR_DOWN): "snake_turn_down_right",
        (DIR_RIGHT, DIR_LEFT): "snake_horiz",
        (DIR_DOWN, DIR_UP): "snake_vertic",
        (DIR_DOWN, DIR_RIGHT): "snake_turn_down_right",
        (DIR_DOWN, DIR_DOWN): "snake_vertic",
        (DIR_DOWN, DIR_LEFT): "snake_turn_down_left",
        (DIR_LEFT, DIR_UP): "snake_turn_up_left",
        (DIR_LEFT, DIR_RIGHT): "snake_horiz",
        (DIR_LEFT, DIR_DOWN): "snake_turn_down_left",
        (DIR_LEFT, DIR_LEFT): "snake_horiz",
    }

    def __init__(self, game_model, y_start):
        self.game_model = game_model

        # Liste de liste de 3 elems :
        # - direction du serpent au début de la tile.
        # - la tile sur laquelle se trouve le morceau de corps du serpent.
        # - direction du serpent à la fin de la tile.
        self.bodies = []
        tile_snake_body = self.game_model.tiles[y_start][0]

        self.bodies.append([DIR_LEFT, tile_snake_body, DIR_RIGHT])
        tile_snake_body.set_snake_part("snake_horiz")
        tile_snake_body = tile_snake_body.adjacencies[DIR_RIGHT]
        self.bodies.append([DIR_LEFT, tile_snake_body, DIR_RIGHT])
        tile_snake_body.set_snake_part("snake_horiz")
        tile_snake_body = tile_snake_body.adjacencies[DIR_RIGHT]

        self.tile_snake_head = tile_snake_body
        self.head_dir = DIR_RIGHT
        gamobj_head = Snake.GAMOBJ_FROM_HEAD_DIR[self.head_dir]
        self.tile_snake_head.set_snake_part(gamobj_head)

        self.current_length = len(self.bodies) + 1
        self.qty_eaten = 0

    def rewind(self):
        if not self.bodies:
            return
        # Copié-collé de bouts de code de on_event_direction.
        # Beurk. On n'est plus à ça près.
        tile_last_body_infos = self.bodies[-1]
        tile_last_body = tile_last_body_infos[1]
        self.tile_snake_head.emptify()
        # Le serpent revient en arrière.
        self.bodies.pop()
        self.head_dir = OPPOSITE_DIR[tile_last_body_infos[0]]
        self.tile_snake_head = tile_last_body
        gamobj_head = Snake.GAMOBJ_FROM_HEAD_DIR[self.head_dir]
        self.tile_snake_head.set_snake_part(gamobj_head)
        self.current_length -= 1

    def on_event_direction(self, direction):
        """
        Renvoie une valeur Snake.MOVE_RESULT_XXX
        """
        if not self._can_move(direction):
            return Snake.MOVE_RESULT_FAIL_BLOCKED

        tile_dest = self.tile_snake_head.adjacencies[direction]
        cancel_last_body = False
        tile_last_body_infos = None
        if self.bodies:
            tile_last_body_infos = self.bodies[-1]
            tile_last_body = tile_last_body_infos[1]
            if tile_last_body == tile_dest:
                cancel_last_body = True

        if cancel_last_body:
            self.tile_snake_head.emptify()
            # Le serpent revient en arrière.
            self.bodies.pop()
            self.head_dir = OPPOSITE_DIR[tile_last_body_infos[0]]
            self.current_length -= 1
        else:
            # Le serpent veut avancer, mais on doit vérifier
            # qu'il a encore de la marge de longueur.
            if self.current_length >= self.game_model.snake_length_max:
                return Snake.MOVE_RESULT_FAIL_TOO_SHORT

            if (
                tile_dest.fruit is not None
                and self.qty_eaten >= self.game_model.stomach_capacity
            ):
                return Snake.MOVE_RESULT_FAIL_STOMACH_FULL

            tile_new_body = self.tile_snake_head
            if tile_last_body_infos is None:
                # Il n'y a pas du tout de body. On prend une direction par défaut.
                # Et comme le serpent arrive par le haut de l'écran, on prend up.
                start_dir = DIR_UP
            else:
                start_dir = OPPOSITE_DIR[tile_last_body_infos[2]]
            gamobj_body = Snake.GAMOBJ_BODY_FROM_DIRS[(start_dir, direction)]
            tile_new_body.set_snake_part(gamobj_body)
            new_body_part = [start_dir, tile_new_body, direction]
            self.bodies.append(new_body_part)
            self.head_dir = direction
            self.current_length += 1
            if tile_dest.fruit is not None:
                self.qty_eaten += 1

        self.tile_snake_head = tile_dest
        gamobj_head = Snake.GAMOBJ_FROM_HEAD_DIR[self.head_dir]
        self.tile_snake_head.set_snake_part(gamobj_head)
        return Snake.MOVE_RESULT_OK

    def _can_move(self, direction):
        tile_dest = self.tile_snake_head.adjacencies[direction]
        if tile_dest is None:
            return False
        if tile_dest.block_type is not None:
            return False
        if tile_dest.gamobj_matches:
            # On ne peut pas manger des fruits en train d'être matchés.
            return False
        if tile_dest.snake_part is not None:
            # Le snake peut revenir en arrière, uniquement sur la snake part précédente.
            if not self.bodies:
                print("No body, but body. Not supposed to happen")
                return False
            else:
                tile_last_body_infos = self.bodies[-1]
                tile_last_body = tile_last_body_infos[1]
                if tile_last_body == tile_dest:
                    return True
                else:
                    return False
        # Ni vu ni connu je t'embrouille. Je gère le début du jeu avec
        # des game_object qui sont censés être uniquement des éléments de décors.
        if tile_dest.gamobj_miscellaneous in ("earth", "sky_unpassable"):
            return False
        return True

    def update_scroll_to_deeper(self):
        self.tile_snake_head = self.tile_snake_head.adjacencies[DIR_UP]
        if self.tile_snake_head is None:
            # Not supposed to happen.
            raise Exception("On est allé plus profond jusqu'à supprimer le serpent")
        for body_infos in self.bodies:
            tile_body = body_infos[1]
            tile_body = tile_body.adjacencies[DIR_UP]
            body_infos[1] = tile_body
        self.bodies = [
            body_infos for body_infos in self.bodies if body_infos[1] is not None
        ]

    def check_scroll_deeper(self):
        x_forbids_go_deep = []
        if self.tile_snake_head.y == 0:
            x_forbids_go_deep.append(self.tile_snake_head.x)
        for body_infos in self.bodies:
            dir_start, tile_body, dir_end = body_infos
            if tile_body.y == 0 and dir_start == DIR_DOWN:
                x_forbids_go_deep.append(tile_body.x)
        return x_forbids_go_deep


class GameModel:
    def __init__(self):
        self.w = 10
        self.h = 15
        self.game_w = 9
        self.game_h = 13
        self.offset_interface_x = 1
        self.offset_interface_y = 2
        snake_x = self.w // 2
        snake_y = 1

        self.match_anim_time = 0
        self.match_show_gamobj = 0

        tiles = []
        for y in range(self.game_h):
            line = [Tile(self, x, y) for x in range(self.game_w)]
            line = tuple(line)
            tiles.append(line)
        self.tiles = tuple(tiles)

        for y, line in enumerate(self.tiles):
            for x, tile in enumerate(line):
                adj = self.make_adjacencies(x, y)
                tile.adjacencies = adj
                # tile.set_random_content()

        self.applying_gravity = False
        self.matched_tiles = []
        # Liste de coordonnées X, indiquant les positions
        # où se trouve des morceaux de serpent qui empêche d'aller plus bas.
        self.x_forbids_go_deep = []
        self.fading_to_black = 0
        self.snake_length_max = 100
        self.stomach_capacity = 15
        self.start_game_run()

    def start_game_run(self):
        self.deep_distance = 0
        self.warned_about_snake_length = False
        self.warned_about_stomach = False
        for line in self.tiles:
            for tile in line:
                tile.emptify()

        # Plein de numéros magiques en dur. Osef. À l'arrache.
        for line in self.tiles[:-5]:
            for tile in line:
                tile.set_gamobj_miscellaneous("sky")
        for tile in self.tiles[-5]:
            tile.set_gamobj_miscellaneous("sky_unpassable")
        for tile in self.tiles[-4]:
            tile.set_gamobj_miscellaneous("sky")
        for tile in self.tiles[-3]:
            tile.set_gamobj_miscellaneous("earth")
        tile_passage = self.tiles[-3][self.game_w // 2]
        tile_passage.emptify()
        tile_passage.gamobj_miscellaneous = None
        tile_passage.render()
        for y in (-2, -1):
            for tile in self.tiles[y]:
                # Pas de fonction set. Osef.
                tile.block_type = 0
                tile.render()
            # Je suis un bourrin et j'aurais dû mettre des foncsions set.
            tile_passage = self.tiles[y][self.game_w // 2]
            tile_passage.emptify()
            tile_passage.gamobj_miscellaneous = None
            tile_passage.fruit = 0
            tile.block_type = 0
            tile_passage.render()

        self.snake = Snake(self, self.game_h - 4)

    def make_adjacencies(self, x, y):
        """
        Renvoie les tiles adjacentes à la tile aux coordonnées x, y.
        On renvoie toujours une liste de 8 éléments (les 8 directions), mais certains éléments
        peuvent être None, si les coordonnées x, y sont sur un bord de l'aire de jeu.
        0 : haut, 1 diagonale haut-droite, 2 : droite, etc.
        """
        adjacencies = (
            self.tiles[y - 1][x] if 0 <= y - 1 else None,
            self.tiles[y - 1][x + 1] if 0 <= y - 1 and x + 1 < self.game_w else None,
            self.tiles[y][x + 1] if x + 1 < self.game_w else None,
            self.tiles[y + 1][x + 1]
            if y + 1 < self.game_h and x + 1 < self.game_w
            else None,
            self.tiles[y + 1][x] if y + 1 < self.game_h else None,
            self.tiles[y + 1][x - 1] if y + 1 < self.game_h and 0 <= x - 1 else None,
            self.tiles[y][x - 1] if 0 <= x - 1 else None,
            self.tiles[y - 1][x - 1] if 0 <= y - 1 and 0 <= x - 1 else None,
        )
        return adjacencies

    def export_all_tiles(self):
        exported_tiles = []

        for y in range(self.offset_interface_y):
            # Pas d'interface pour l'instant, mais ça va venir.
            line = [[] for x in range(self.w)]
            exported_tiles.append(line)

        for game_line in self.tiles:
            interface_line = []
            for x in range(self.offset_interface_x):
                # Toujours pas d'interface.
                interface_line.append([])
            for game_tile in game_line:
                interface_line.append(game_tile.game_objects)
            exported_tiles.append(interface_line)
        if DEBUG:
            print(exported_tiles)

        for x in self.x_forbids_go_deep:
            exported_tiles[1][x + self.offset_interface_x].append(
                "arrow_deep_forbidden"
            )

        show_home = any(
            (
                not self.snake.bodies,
                self.warned_about_snake_length,
                self.warned_about_stomach,
            )
        )
        if show_home:
            if self.snake.bodies:
                # Deux indexage suivant d'un .x, c'est bien crade.
                # Désolay...
                x_home = self.snake.bodies[0][1].x
            else:
                x_home = self.snake.tile_snake_head.x
            x_home += self.offset_interface_x
            exported_tiles[1][x_home].append("back_home")

        if self.fading_to_black:
            # Gros bourrin parce qu'on reparcourt toute l'aire de jeu.
            # Osef, quand on le fait, on fait rien d'autre que ça.
            for exported_line in exported_tiles:
                for tile_gamobjs in exported_line:
                    tile_gamobjs.extend(["fade_black"] * self.fading_to_black)

        return exported_tiles

    def check_fall_column(self, x_column, fall_column):
        # print("fall_column", fall_column)
        if not fall_column:
            return False

        if not all((tile.is_empty() for tile in fall_column)):
            return True

        tile_top = fall_column[-1]
        tile_top_up = tile_top.adjacencies[DIR_UP]
        if not tile_top_up.is_empty():
            return True
        return False

    def compute_gravity_falls(self, x_column):
        """
        Renvoie une liste de liste.
        Chaque élément de la liste de liste est une tile,
        indiquant que cette tile doit prendre
        le contenu de la tile au-dessus d'elle, pour appliquer une gravité.
        Chaque sous-liste indique implicitement qu'il faut prendre la
        dernière tile au-dessus et la vider.
        """
        gravity_falls = []
        currently_falling = False
        current_fall_column = []
        current_tile = self.tiles[self.game_h - 1][x_column]

        for _ in range(self.game_h - 1):
            if currently_falling:
                if current_tile.does_stop_gravity():
                    # Faut annuler la chute de la tile d'avant.
                    current_fall_column.pop()
                    if self.check_fall_column(x_column, current_fall_column):
                        gravity_falls.append(current_fall_column)
                    current_fall_column = []
                    currently_falling = False
                else:
                    current_fall_column.append(current_tile)
            else:
                if current_tile.is_empty():
                    current_fall_column.append(current_tile)
                    currently_falling = True
            current_tile = current_tile.adjacencies[DIR_UP]

        if currently_falling:

            tile_top = current_fall_column[-1]
            tile_up_top = tile_top.adjacencies[DIR_UP]

            if tile_up_top.does_stop_gravity():
                # Faut aussi annuler la chute de la tile d'avant.
                # Ou quelque chose du genre. Bref, j'ai testé et faut faire comme ça.
                current_fall_column.pop()
            if self.check_fall_column(x_column, current_fall_column):
                gravity_falls.append(current_fall_column)
        # print(gravity_falls)
        return gravity_falls

    def apply_gravity(self, gravity_falls):
        # print("gravity_falls wtf", gravity_falls)
        for current_fall in gravity_falls:
            for tile_dst in current_fall:

                # Donc là ça va péter si tiles_src est la tile tout en haut.
                # Mais comme j'ai bien codé ma fonction compute_gravity_falls.
                # on va jamais jusqu'en haut.
                tile_src = tile_dst.adjacencies[DIR_UP]
                tile_dst.get_content_from_other_tile(tile_src)
            # À la fin du fall, on vide la dernière tile.
            tile_src.emptify()

    def check_gravity_all_area(self):
        gravities_to_apply = []
        must_apply_gravity = False
        for x in range(self.game_w):
            gravity_falls = self.compute_gravity_falls(x)
            gravities_to_apply.append(gravity_falls)
            if gravity_falls:
                must_apply_gravity = True
        if not must_apply_gravity:
            gravities_to_apply = None
        return gravities_to_apply

    def check_all_match(self):

        # clear des matches précédents.
        matched_tiles = set()
        for line in self.tiles:
            for tile in line:
                tile.clear_match()

        # --- check des matches horizontaux ---
        for line in self.tiles:
            for tile_start in line:
                # TODO : mettre ça dans une fonction parce que là c'est
                # trop de code imbriqué.
                current_matches = []
                current_fruit_type = tile_start.fruit
                if (
                    not tile_start.has_horizontal_match
                    and current_fruit_type is not None
                ):
                    tile_cur = tile_start
                    while tile_cur is not None and tile_cur.fruit == current_fruit_type:
                        current_matches.append(tile_cur)
                        tile_cur = tile_cur.adjacencies[DIR_RIGHT]
                    # print(tile_start.x, tile_start.y, len(current_matches))
                    if len(current_matches) >= 3:
                        # print(
                        #     "first and length : ",
                        #     tile_start.x,
                        #     tile_start.y,
                        #     len(current_matches),
                        # )
                        # print("last", current_matches[-1].x, current_matches[-1].y)
                        current_matches[0].add_match("match_right")
                        for tile in current_matches[1:-1]:
                            tile.add_match("match_horiz")
                        current_matches[-1].add_match("match_left")
                        matched_tiles = matched_tiles.union(set(current_matches))

        # --- check des matches verticaux. ---
        # TODO : copié-collé de gros bourrin avec le check horizontal.
        # À mon avis y'a moyen de faire mieux.
        # TODO : et ce serait tellement classe d'avoir les tiles
        # indexées par ligne ET par colonne. Comme ça j'aurais pas besoin
        # d'itérer sur x et y comme un pauvre.
        for x_start in range(self.game_w):
            for y_start in range(self.game_h):
                tile_start = self.tiles[y_start][x_start]
                # TODO : mettre ça dans une fonction parce que là c'est
                # trop de code imbriqué.
                current_matches = []
                current_fruit_type = tile_start.fruit
                if not tile_start.has_vertical_match and current_fruit_type is not None:
                    tile_cur = tile_start
                    while tile_cur is not None and tile_cur.fruit == current_fruit_type:
                        current_matches.append(tile_cur)
                        tile_cur = tile_cur.adjacencies[DIR_DOWN]
                    # print(tile_start.x, tile_start.y, len(current_matches))
                    if len(current_matches) >= 3:
                        current_matches[0].add_match("match_down")
                        for tile in current_matches[1:-1]:
                            tile.add_match("match_vertic")
                        current_matches[-1].add_match("match_up")
                        matched_tiles = matched_tiles.union(set(current_matches))

        # TODO : calculer les XP des matches.
        self.matched_tiles = list(matched_tiles)

    def destroy_matched_fruits(self):
        for tile in self.matched_tiles:
            tile.emptify()
            # On détruit les blocs adjacents aux matches.
            # J'aurais sûrement pas le temps de faire des blocs ayant
            # plusieurs points de vie (à détruire en plusieurs matchs)
            # Donc je pète le bloc direct.
            for adj_tile in tile.adjacencies[::2]:
                if adj_tile is not None and adj_tile.block_type == 0:
                    adj_tile.emptify()

    def go_deeper(self):
        self.deep_distance += 1
        # Les tiles doivent prendre ce qu'il y a en-dessous d'elles.
        # Encore des itérations stupides avec des x et y, car j'ai pas
        # indexé par colonne. C'est pas grave. On est des pauvres, on indexe pas, mais on n'a honte de rien.
        for x in range(self.game_w):
            tile_current = self.tiles[0][x]
            for _ in range(self.game_h - 1):
                tile_below = tile_current.adjacencies[DIR_DOWN]
                tile_current.get_content_from_other_tile(tile_below)
                tile_current = tile_below
            tile_below.set_random_content()
        # Il faut aussi déplacer les références de tiles du body du serpent.
        self.snake.update_scroll_to_deeper()
        # Et les références des tiles en cours de match.
        self.matched_tiles = [tile.adjacencies[DIR_UP] for tile in self.matched_tiles]
        self.matched_tiles = [tile for tile in self.matched_tiles if tile is not None]

    def update_x_forbids_with_movement(self):
        """
        Nom de fonction tout pourri, pas mieux.
        """
        if not self.x_forbids_go_deep:
            return
        new_x_forbids_go_deep = self.snake.check_scroll_deeper()
        self.x_forbids_go_deep = [
            x for x in self.x_forbids_go_deep if x in new_x_forbids_go_deep
        ]

    def go_back_home_if_possible(self):
        # Le serpent rentre à la maison.
        if self.applying_gravity or self.match_anim_time:
            message_to_player(
                ("Wait the end of the gravity and the matches", "before returning home")
            )
            return None
        else:
            message_to_player(("You return home",))
            self.fading_to_black = 1
            return ACTION_FADE_TO_BLACK

    def on_game_event(self, event_name):

        if event_name == "anim_fade_to_black":
            self.fading_to_black += 1
            if self.fading_to_black == 10:
                self.fading_to_black = 0
                self.start_game_run()
                return None
            else:
                return ACTION_FADE_TO_BLACK
        else:
            if self.fading_to_black:
                # On est en train de faire un fondu vers le noir.
                # Toutes les autres actions ne doivent pas être prises en compte.
                return None

        direction = DIR_FROM_EVENT.get(event_name)

        if direction is not None:

            if direction == DIR_UP and not self.snake.bodies:
                return self.go_back_home_if_possible()

            if (
                direction == DIR_DOWN
                and self.snake.tile_snake_head.y == self.game_h - 2
            ):
                self.x_forbids_go_deep = self.snake.check_scroll_deeper()
                if self.x_forbids_go_deep:
                    message_to_player(
                        (
                            ('Push the button "1" to rewind yourself.'),
                            ("If you go deeper, you will cut yourself !"),
                        )
                    )
                    return
                self.go_deeper()
                if not self.match_anim_time and not self.applying_gravity:
                    self.check_all_match()
                    if self.matched_tiles:
                        self.match_anim_time = 1
                        self.match_show_gamobj = 1
                        for tile in self.matched_tiles:
                            tile.render()
                        return ACTION_ANIM_MATCH
                    else:
                        # Pas de match suite à un scroll plus profond.
                        # On peut s'arrêter. Pas besoin de checker la gravité,
                        # quand on va plus profond on tombe forcément sur des objets et pas du vide.
                        return None

            else:

                move_result = self.snake.on_event_direction(direction)
                if move_result == Snake.MOVE_RESULT_FAIL_TOO_SHORT:
                    if not self.warned_about_snake_length:
                        message_to_player(
                            (
                                "You have reached your maximum length.",
                                "You should go home and restart a trip.",
                            )
                        )
                        self.warned_about_snake_length = True
                elif move_result == Snake.MOVE_RESULT_FAIL_STOMACH_FULL:
                    if not self.warned_about_stomach:
                        message_to_player(
                            (
                                "You ate too much fruits.",
                                "You should go home and restart a trip.",
                            )
                        )
                        self.warned_about_stomach = True

                self.update_x_forbids_with_movement()
                if not self.applying_gravity:
                    # On n'est pas déjà en train d'appliquer de la gravité.
                    # On en appliquera une (pas tout de suite, dans quelques ms).
                    self.applying_gravity = True
                    return ACTION_GRAVITY
                else:
                    return None

        elif event_name == "action_1":
            if self.snake.bodies:
                self.snake.rewind()
                self.update_x_forbids_with_movement()
                return None
            else:
                return self.go_back_home_if_possible()

        elif event_name == "action_2":
            return None

        elif event_name == "anim_match":
            # print("anim match", self.match_anim_time, self.match_show_gamobj)
            self.match_anim_time += 1
            self.match_show_gamobj = [0, 1, 2, 3, 2, 1, 0][self.match_anim_time]
            for tile in self.matched_tiles:
                tile.render()
            if self.match_anim_time == 6:
                self.match_anim_time = 0
                # Animation du match terminé. On détruit les fruits
                self.destroy_matched_fruits()
                # Et du coup, faut revérifier la gravité.
                self.applying_gravity = True
                return ACTION_GRAVITY
            else:
                return ACTION_ANIM_MATCH

        elif event_name == "apply_gravity":

            gravities_to_apply = self.check_gravity_all_area()
            if gravities_to_apply is not None:
                for gravity_falls in gravities_to_apply:
                    self.apply_gravity(gravity_falls)
                return ACTION_GRAVITY
            else:
                self.applying_gravity = False
                # La gravité est finie. Maintenant, il faut vérifier
                # si on doit faire des matches.
                if self.match_anim_time:
                    # Ah zut alors. La gravité est finie mais on a encore
                    # des matchs en cours. (Ça peut arriver si le serpent
                    # fait tomber des fruits pendant qu'il y a un autre
                    # match).
                    # Dans ce cas, on fait rien dans l'immédiat.
                    # La vérif des match se refera à la fin de l'enchainement:
                    # vérif des match en cours, application de gravité.
                    return None
                else:
                    self.check_all_match()
                    if self.matched_tiles:
                        self.match_anim_time = 1
                        self.match_show_gamobj = 1
                        for tile in self.matched_tiles:
                            tile.render()
                        return ACTION_ANIM_MATCH
                    else:
                        # On a fini la gravité, et on vient de vérifier
                        # qu'il n'y a plus de match à faire.
                        # on peut s'arrêter là.
                        return None

