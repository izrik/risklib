#!/usr/bin/env python3

import csv

territories = {}

with open('territories.csv') as csvfile:
    reader = csv.reader(csvfile)
    first = True
    for row in reader:
        if first:
            names = row
            first = False
        else:
            tname = row[0]
            territories[tname] = set()
            fcolumn = True
            for cell, other in zip(row, names):
                if fcolumn:
                    fcolumn = False
                    continue
                if other and cell and cell.strip() and cell != '-':
                    territories[tname].add(other)

# for name in territories:
#     for other in territories[name]:
#         territories[other].add(name)

for name in territories:
    # neighbor_list = ', '.join(f'\'{_}\'' for _ in territories[name])
    # print(f"        Territory('{name}', neighbors_by_name=[{neighbor_list}]),")
