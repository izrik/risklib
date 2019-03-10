#!/usr/bin/env python3

import traceback
from random import randint
import readline


def roll(num_dice):
    return sorted([randint(1, 6) for _ in range(num_dice)], reverse=True)


def repl():
    prompt = '> '
    while True:
        try:
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


if __name__ == '__main__':
    repl()
