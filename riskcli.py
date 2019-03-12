#!/usr/bin/env python3

import traceback
from itertools import cycle
from random import randint, shuffle
import readline


def roll(num_dice):
    return sorted([randint(1, 6) for _ in range(num_dice)], reverse=True)


AFGHANISTAN = 'Afghanistan'
AFRICA = 'Africa'
ALASKA = 'Alaska'
ALBERTA = 'Alberta'
ARGENTINA = 'Argentina'
ASIA = 'Asia'
AUSTRALIA = 'Australia'
BRAZIL = 'Brazil'
CENT_AM = 'Central America'
CHINA = 'China'
CONGO = 'Congo'
E_AFRICA = 'East Africa'
E_AUST = 'Eastern Australia'
E_US = 'Eastern United States'
EGYPT = 'Egypt'
EUROPE = 'Europe'
GREAT_BRITAIN = 'Great Britain'
GREENLAND = 'Greenland'
ICELAND = 'Iceland'
INDIA = 'India'
INDONESIA = 'Indonesia'
IRKUTSK = 'Irkutsk'
JAPAN = 'Japan'
KAMCHATKA = 'Kamchatka'
MADAGASCAR = 'Madagascar'
MIDDLE_EAST = 'Middle East'
MONGOLIA = 'Mongolia'
N_AFRICA = 'North Africa'
N_EURO = 'Northern Europe'
NW_TERR = 'Northwest Territory'
NEW_GUINEA = 'New Guinea'
NORTH_AMERICA = 'North America'
ONTARIO = 'Ontario'
PERU = 'Peru'
QUEBEC = 'Quebec'
S_AFRICA = 'South Africa'
S_EURO = 'Southern Europe'
SCAND = 'Scandinavia'
SIAM = 'Siam'
SIBERIA = 'Siberia'
SOUTH_AMERICA = 'South America'
UKRAINE = 'Ukraine'
URAL = 'Ural'
VENEZ = 'Venezuela'
W_AUST = 'Western Australia'
W_EURO = 'Western Europe'
W_US = 'Western United States'
YAKUTSK = 'Yakutsk'


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.territories = []

    def count_all_armies(self):
        count = 0
        for t in self.territories:
            count += t.num_armies


class Territory:
    def __init__(self, name, neighbors_by_name):
        self.name = name
        self.neighbors = []
        self.continent = None
        self.owner = None
        self.num_armies = 0
        self.neighbors_by_name = neighbors_by_name


class Continent:
    def __init__(self, name, bonus, territories_by_name):
        self.name = name
        self.bonus = bonus
        self.territories = []
        self.territories_by_name = territories_by_name


class Map:
    def __init__(self, territories, continents):
        self.territories = territories
        self.continents = continents

        self.t_by_name = {}
        for t in self.territories:
            self.t_by_name[t.name] = t

        for t in self.territories:
            for nname in t.neighbors_by_name:
                t.neighbors.append(self.t_by_name[nname])
                self.t_by_name[nname].neighbors.append(t)

        for c in self.continents:
            for tname in c.territories_by_name:
                c.territories.append(self.t_by_name[tname])
                self.t_by_name[tname].continent = c

        self.c_by_name = {}
        for c in self.continents:
            self.c_by_name[c.name] = c


class Game:
    def __init__(self, players, game_map):
        self.players = players
        self.game_map = game_map
        self.turns = []
        self.next_player = players[0]

    def get_most_recent_turn(self):
        if not self.turns:
            return None
        return self.turns[-1]


def gen_default_map():
    return Map(
        territories=[
            Territory(ALASKA, neighbors_by_name=[KAMCHATKA, NW_TERR, ALBERTA]),
            Territory(NW_TERR,
                      neighbors_by_name=[ONTARIO, ALBERTA, GREENLAND]),
            Territory(GREENLAND, neighbors_by_name=[ONTARIO, ICELAND, QUEBEC]),
            Territory(ALBERTA, neighbors_by_name=[ONTARIO, W_US]),
            Territory(ONTARIO, neighbors_by_name=[E_US, QUEBEC, W_US]),
            Territory(QUEBEC, neighbors_by_name=[E_US]),
            Territory(W_US, neighbors_by_name=[E_US, CENT_AM]),
            Territory(E_US, neighbors_by_name=[CENT_AM]),
            Territory(CENT_AM, neighbors_by_name=[VENEZ]),
            Territory(VENEZ, neighbors_by_name=[BRAZIL, PERU]),
            Territory(BRAZIL, neighbors_by_name=[PERU, ARGENTINA, N_AFRICA]),
            Territory(PERU, neighbors_by_name=[ARGENTINA]),
            Territory(ARGENTINA, neighbors_by_name=[]),
            Territory(ICELAND, neighbors_by_name=[SCAND, GREAT_BRITAIN]),
            Territory(SCAND,
                      neighbors_by_name=[GREAT_BRITAIN, UKRAINE, N_EURO]),
            Territory(GREAT_BRITAIN, neighbors_by_name=[W_EURO, N_EURO]),
            Territory(W_EURO, neighbors_by_name=[S_EURO, N_AFRICA, N_EURO]),
            Territory(N_EURO, neighbors_by_name=[UKRAINE, S_EURO]),
            Territory(S_EURO, neighbors_by_name=[MIDDLE_EAST, EGYPT, UKRAINE,
                                                 N_AFRICA]),
            Territory(UKRAINE, neighbors_by_name=[MIDDLE_EAST, AFGHANISTAN,
                                                  URAL]),
            Territory(N_AFRICA, neighbors_by_name=[E_AFRICA, EGYPT, CONGO]),
            Territory(EGYPT, neighbors_by_name=[E_AFRICA, MIDDLE_EAST]),
            Territory(E_AFRICA,
                      neighbors_by_name=[S_AFRICA, CONGO, MADAGASCAR]),
            Territory(CONGO, neighbors_by_name=[S_AFRICA]),
            Territory(S_AFRICA, neighbors_by_name=[MADAGASCAR]),
            Territory(MADAGASCAR, neighbors_by_name=[]),
            Territory(MIDDLE_EAST, neighbors_by_name=[AFGHANISTAN, INDIA]),
            Territory(AFGHANISTAN, neighbors_by_name=[URAL, CHINA, INDIA]),
            Territory(URAL, neighbors_by_name=[SIBERIA, CHINA]),
            Territory(SIBERIA, neighbors_by_name=[MONGOLIA, CHINA, IRKUTSK,
                                                  YAKUTSK]),
            Territory(YAKUTSK, neighbors_by_name=[KAMCHATKA, IRKUTSK]),
            Territory(IRKUTSK, neighbors_by_name=[KAMCHATKA, MONGOLIA]),
            Territory(KAMCHATKA, neighbors_by_name=[MONGOLIA, JAPAN]),
            Territory(INDIA, neighbors_by_name=[SIAM, CHINA]),
            Territory(CHINA, neighbors_by_name=[MONGOLIA, SIAM]),
            Territory(MONGOLIA, neighbors_by_name=[JAPAN]),
            Territory(JAPAN, neighbors_by_name=[]),
            Territory(SIAM, neighbors_by_name=[INDONESIA]),
            Territory(INDONESIA, neighbors_by_name=[NEW_GUINEA, W_AUST]),
            Territory(NEW_GUINEA, neighbors_by_name=[W_AUST, E_AUST]),
            Territory(W_AUST, neighbors_by_name=[E_AUST]),
            Territory(E_AUST, neighbors_by_name=[])],
        continents=[
            Continent(NORTH_AMERICA, 5, [ALASKA, NW_TERR, GREENLAND, ALBERTA,
                                         ONTARIO, QUEBEC, W_US, E_US,
                                         CENT_AM]),
            Continent(SOUTH_AMERICA, 2, [VENEZ, BRAZIL, PERU, ARGENTINA]),
            Continent(EUROPE, 5,
                      [ICELAND, SCAND, GREAT_BRITAIN, W_EURO, N_EURO,
                       S_EURO, UKRAINE]),
            Continent(AFRICA, 3, [N_AFRICA, EGYPT, E_AFRICA, CONGO, S_AFRICA,
                                  MADAGASCAR]),
            Continent(ASIA, 7,
                      [MIDDLE_EAST, AFGHANISTAN, URAL, SIBERIA, YAKUTSK,
                       IRKUTSK, KAMCHATKA, INDIA, CHINA, MONGOLIA, JAPAN,
                       SIAM]),
            Continent(AUSTRALIA, 2, [INDONESIA, NEW_GUINEA, W_AUST, E_AUST])])


def print_info(game):
    if game is None:
        print('No game started. Type "start" to start a new game.')
        return
    print(f'It is {game.next_player.name}\'s turn.')


def repl():
    prompt = '> '
    game = None
    while True:
        try:
            print_info(game)
            input_s = input(prompt)
            if not input_s:
                continue
            input_s = input_s.strip()
            if not input_s:
                continue
            parts = input_s.split()
            command = parts[0]
            nparts = len(parts)
            if command in ['exit', 'quit']:
                break
            elif command == 'roll':
                num_dice = 1
                if nparts > 1:
                    num_dice = int(parts[1])
                cmd_roll(num_dice)
            elif command == 'attack':
                attacker = 3
                defender = 2
                if nparts > 1:
                    attacker = int(parts[1])
                if nparts > 2:
                    defender = int(parts[2])
                cmd_attack(attacker, defender)
            elif command == 'start':
                game = cmd_start()
            elif command == 'player':
                player = game.next_player
                if nparts > 1:
                    player_num = int(parts[1]) - 1
                    player = game.players[player_num]
                cmd_print_player(player, game)
            else:
                print(f'Unknown: "{command}"')
        except EOFError:
            print('')
            break
        except KeyboardInterrupt:
            print('')
            continue
        except Exception as ex:
            print('Caught the following exception:')
            tb = traceback.format_exception(type(ex), ex, ex.__traceback__)
            for line in tb:
                print('  ' + line, end='')


def cmd_roll(num_dice):
    print('    ' + str(roll(num_dice)))


def cmd_attack(attacker, defender):
    rattacker = roll(attacker)
    rdefender = roll(defender)

    print(f'    attacker: {rattacker}')
    print(f'    defender: {rdefender}')

    attacker_loses = 0
    defender_loses = 0

    def cmp_(a, d):
        nonlocal attacker_loses
        nonlocal defender_loses
        if d >= a:
            attacker_loses += 1
        else:
            defender_loses += 1
        return [a, d]

    list(map(cmp_, rattacker, rdefender))

    if attacker_loses > 0:
        print(f'    attacker loses {attacker_loses}')
    if defender_loses > 0:
        print(f'    defender loses {defender_loses}')


def cmd_start():
    game = Game(players=[Player('player1', 'red'),
                         Player('player2', 'black')],
                game_map=gen_default_map())

    print('The players, in order, are:')
    for i, player in enumerate(game.players):
        print(f'  {i + 1}. {player.name} ({player.color})')
    print('Territories will be assigned randomly.')
    terrs = list(game.game_map.territories)
    shuffle(terrs)
    for terr, player in zip(terrs, cycle(game.players)):
        player.territories.append(terr)
        terr.owner = player
        terr.num_armies = 1
    return game


def cmd_print_player(player, game):
    print(f'    {player.name}')
    print(f'    Color: {player.color}')
    # territory_list = ', '.join(f'{t.name} ({t.num_armies})'
    #                            for t in player.territories)
    # print(f'    Territories: {territory_list}')
    print(f'    Territories:')
    for c in game.game_map.continents:
        t_in_c = [t for t in c.territories if t.owner is player]
        if t_in_c:
            print(f'      {c.name}:')
            for t in t_in_c:
                print(f'        {t.name} ({t.num_armies})')
    print('')


if __name__ == '__main__':
    repl()
