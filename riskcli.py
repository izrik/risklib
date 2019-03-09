#!/usr/bin/env python3

import argparse
import traceback
from random import randint
import readline


def roll(num_dice):
    return sorted([randint(1, 6) for _ in range(num_dice)], reverse=True)


def repl():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()

    roll_s = subs.add_parser('roll')
    roll_s.add_argument('num_dice', nargs='?', default=3, type=int)
    roll_s.set_defaults(func=cmd_roll)

    attack_s = subs.add_parser('attack')
    attack_s.add_argument('attacker', nargs='?', default=3, type=int)
    attack_s.add_argument('defender', nargs='?', default=2, type=int)
    attack_s.set_defaults(func=cmd_attack)

    prompt = '> '
    while True:
        try:
            input_s = input(prompt)
            args = parser.parse_args(input_s.split())
            if 'func' in args and args.func:
                args.func(args)
            else:
                parser.print_help()
        except EOFError:
            print('')
            break
        except KeyboardInterrupt:
            print('')
            continue
        except (Exception, SystemExit, argparse.ArgumentError) as ex:
            print('Caught the following exception:')
            tb = traceback.format_exception(type(ex), ex, ex.__traceback__)
            for line in tb:
                print('  ' + line, end='')


def cmd_roll(args):
    print('    ' + str(roll(args.num_dice)))


def cmd_attack(args):
    attacker = roll(args.attacker)
    defender = roll(args.defender)

    print(f'    attacker: {attacker}')
    print(f'    defender: {defender}')

    attacker_loses = 0
    defender_loses = 0

    def cmp_(a, d):
        nonlocal attacker_loses
        nonlocal defender_loses
        if d >= a:
            attacker_loses += 1
        else:
            defender_loses += 1
        return [a,d]

    x = list(map(cmp_, attacker, defender))
    # print(f'x: {x}')

    if attacker_loses > 0:
        print(f'    attacker loses {attacker_loses}')
    if defender_loses > 0:
        print(f'    defender loses {defender_loses}')


if __name__ == '__main__':
    repl()
