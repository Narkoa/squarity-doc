# https://raw.githubusercontent.com/darkrecher/squarity-doc/master/jeux/joyeux_anniv/jeu_anniv.png
# http://squarity.fr/#fetchez_githubgist_darkrecher/4ead81bdbfab7ca944026b0ea4fc31b8/raw/jeu-anniv-2


"""
{
    "tile_size": 32,
    "img_coords": {
        "light": [32, 89],
        "player_off": [0, 89],
        "player_on": [448, 43],
        " ": [64, 89],
        "/": [96, 89],
        ":": [128, 89],
        ".": [160, 89],
        "|": [192, 89],
        "[": [224, 89],
        "]": [256, 89],
        "{": [288, 89],
        "}": [320, 89],
        "_": [352, 89],
        "-": [384, 89],
        "(": [416, 89],
        ")": [448, 89],
        "A": [0, 0],
        "B": [32, 0],
        "C": [64, 0],
        "D": [96, 0],
        "E": [128, 0],
        "F": [160, 0],
        "G": [192, 0],
        "H": [224, 0],
        "I": [256, 0],
        "J": [288, 0],
        "K": [320, 0],
        "L": [350, 0],
        "M": [384, 0],
        "N": [0, 43],
        "O": [32, 43],
        "P": [64, 43],
        "Q": [96, 43],
        "R": [128, 43],
        "S": [160, 43],
        "T": [192, 43],
        "U": [224, 43],
        "V": [255, 43],
        "W": [288, 43],
        "X": [322, 43],
        "Y": [352, 43],
        "Z": [384, 43]
    }
}
"""

"""
-------------------------------------
--- LES MOTS-MÊLÉS D'ANNIVERSAIRE ---
-------------------------------------

(Parce que j'ai créé ce jeu pour l'anniv' d'un pote).

 - Placez le personnage sur la première lettre du mot que vous voulez former.
 - Appuyez sur le bouton "1" pour activer la récupération de lettres.
 - Déplacez-vous sur les lettres du mot.
 - Re-appuyez sur le bouton "1".
 - Si le mot est correct, il apparaît en haut de l'aire de jeu.

La liste des mots à trouver s'affiche en bas, dans la fenêtre de log.

Appuyez sur le bouton "2" pour re-afficher cette liste.

Vous pouvez très facilement modifier la grille de lettre, et les mots à trouver.
C'est au début du code source, c'est à dire juste en-dessous de ce texte.

Pour info, la police de caractère provient de ce site :
https://www.1001fonts.com/vtks-white-page-font.html (54 pts)

"""

LEVEL_MAP = (
    "  |               ] ",
    "                 )  ",
    "     }              ",
    " (        _-        ",
    "                    ",
    "     GROUCHEUKZ     ",
    "}    SCHLRFMKIR     ",
    "| *  OETUORLUGE    |",
    ")    CTNESEUISR    ]",
    "}(   ANNIVERSAI    [|",
    "]|)|            ] ]}",
    "}( [))|     |](|[[((",
    "(})])[)|(| |[])] [  ",
    "))[ })[(}(]|([[ (| )",
)

WORDS_TO_FIND = [
    "REVIENT", "CHOUCROUTE", "ROSES",
    "SERF", "ANNIVERSAIRE", "SCHLUCHE",
    "HOHOHOHOHO",
]

class GameModel():

    def __init__(self):
        self.w = 20
        self.h = 14
        self.words_to_find = list(WORDS_TO_FIND)
        self.tiles = []
        self.current_message = ""
        self.lit_positions = []
        self.y_limit_text = 3
        self.message_pos_y = 0
        self.letter_enabled = False
        self.current_gamobj_player = self.get_gamobj_player()

        for y, map_line in enumerate(LEVEL_MAP):
            current_line = []
            for x, map_char in enumerate(map_line):

                if map_char == "*":
                    self.player_x = x
                    self.player_y = y
                    map_char = self.current_gamobj_player
                if map_char == "_":
                    # La position du gâteau d'anniversaire définit la zone
                    # dans l'aire de jeu où les mots trouvés s'affichent.
                    self.y_limit_text = y
                if map_char == " ":
                    current_line.append([map_char])
                else:
                    current_line.append([" ", map_char])

            self.tiles.append(current_line)
        self.print_words_to_find()

    def get_gamobj_player(self):
        if self.letter_enabled:
            return "player_on"
        else:
            return "player_off"

    def export_all_tiles(self):
        return self.tiles

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def is_a_letter(self, gamobj):
        return len(gamobj) == 1 and gamobj.isupper()

    def coord_move(self, x, y, direction):
        if direction == "R":
            x += 1
        elif direction == "L":
            x -= 1
        if direction == "D":
            y += 1
        if direction == "U":
            y -= 1
        return (x, y)

    def check_move(self, dest_x, dest_y):
        if not (0 <= dest_x < self.w and 0 <= dest_y < self.h):
            return False
        return True

    def add_message_on_area(self, message, y_msg):
        line = self.tiles[y_msg]
        for x, gamobjs in enumerate(line):
            filtered_gamobs = filter(lambda gobj:not self.is_a_letter(gobj), gamobjs)
            line[x][:] = filtered_gamobs
        offset_center = max(0, (self.w-len(message)) // 2)
        for x, message_char in enumerate(message[:self.w], offset_center):
            line[x].append(message_char)

    def add_letter_to_word(self, x, y):
        if self.player_y < self.y_limit_text:
            return
        tile_with_letter = self.get_tile(x, y)
        for gamobj in tile_with_letter:
            if self.is_a_letter(gamobj):
                self.current_message += gamobj
                self.lit_positions.append((x, y))
                tile_with_letter.append("light")
                return

    def print_words_to_find(self):
        if self.words_to_find:
            print("Liste des mots à trouver :")
            print(", ".join(self.words_to_find))
        else:
            print("Vous avez trouvé tous les mots. Félicitations!")

    def add_some_beers(self):
        print("Voilà des bières (pour manger avec le gâteau).")
        for x in range(0, self.w, 2):
            tile = self.get_tile(x, self.y_limit_text)
            if len(tile) == 1:
                tile.append("{")

    def on_action_1(self):
        tile_player = self.get_tile(self.player_x, self.player_y)
        tile_player.remove(self.current_gamobj_player)

        self.letter_enabled = not self.letter_enabled
        self.current_gamobj_player = self.get_gamobj_player()
        tile_player.append(self.current_gamobj_player)

        if self.letter_enabled:

            self.add_letter_to_word(self.player_x, self.player_y)

        else:

            if self.current_message:

                if self.current_message in self.words_to_find:
                    print("Bravo !")
                    self.add_message_on_area(self.current_message, self.message_pos_y)
                    self.message_pos_y += 1
                    if self.message_pos_y >= self.y_limit_text:
                        self.message_pos_y = 0
                    self.words_to_find.remove(self.current_message)
                    self.print_words_to_find()
                    if not self.words_to_find:
                        self.add_some_beers()
                else:
                    print("'%s'... Ce mot n'est pas dans la liste." % self.current_message)

                self.current_message = ""
                for pos_lit_x, pos_lit_y in self.lit_positions:
                    gamobjs_with_light = self.get_tile(pos_lit_x, pos_lit_y)
                    gamobjs_with_light[:] = filter(lambda gobj:gobj != "light", gamobjs_with_light)
                self.lit_positions = []

    def on_game_event(self, event_name):

        if event_name == "action_1":
            self.on_action_1()
            return
        if event_name == "action_2":
            self.print_words_to_find()
            return

        player_dest_x, player_dest_y = self.coord_move(
            self.player_x,
            self.player_y,
            event_name
        )
        if not self.check_move(player_dest_x, player_dest_y):
            return

        tile_start_player = self.get_tile(self.player_x, self.player_y)
        tile_dest_player = self.get_tile(player_dest_x, player_dest_y)

        tile_start_player.remove(self.current_gamobj_player)
        tile_dest_player.append(self.current_gamobj_player)
        self.player_x = player_dest_x
        self.player_y = player_dest_y

        if self.letter_enabled:
            self.add_letter_to_word(player_dest_x, player_dest_y)
