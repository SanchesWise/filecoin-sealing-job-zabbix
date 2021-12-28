#!/usr/bin/env python3
import os
import time
import fileinput
from itertools import count

sector_list = []
# dict.fromkeys(['PID', 'WORKER', 'STAGE', 'STATE', 'TIME'])
file_name = 'test.txt'
number = 1
workers = []
abnormal_count = 0
freezePC2_count = 0
workerPC1count = 2
workerPC1current_count=0
workerPC1summary_sectors =0

with open(file_name, mode='r', encoding='utf8') as file:
    # with fileinput.input() as file:
    for line in file:
        sector_list.append(dict(zip(['#PID', '#WORKER', '#STAGE', '#STATE', '#TIME'], line[:-1].split(' '))))

print(f'{sector_list}')
for sector in sector_list:
    workers.append(sector['#WORKER'])
workerslist = list(set(workers))
workerslist.sort()
workers_sectors_number = {worker: [0, 0] for worker in workerslist}
print(f'{workerslist}')
print(f'{workers_sectors_number}')

for sector in sector_list:
    for worker in workerslist:
        if sector['#WORKER'] == worker:
            workers_sectors_number[worker][0] += 1
            if sector['#STAGE'] == "PC1":
                workers_sectors_number[worker][1] += 1

    if sector['#STAGE'] == 'abnormal':
        abnormal_count += 1
    if len(sector['#TIME']) > 8 and sector['#STAGE'] == 'PC2':
        print(sector['#TIME'], sector['#STAGE'], sector['#PID'])
        freezePC2_count += 1

for keys in workers_sectors_number:
    if workers_sectors_number[keys][1] > 0:
        workerPC1current_count += 1
        workerPC1summary_sectors += workers_sectors_number[keys][1]

if workerPC1summary_sectors < 10*workerPC1current_count:
    pass
if workerPC1current_count < workerPC1count:
    pass
print(f'abnormal_count = {abnormal_count}, freezePC2_count = {freezePC2_count}')
print(f'{workers_sectors_number}')
print(f'workerPC1summary_sectors {workerPC1summary_sectors} workerPC1current_count {10*workerPC1current_count}')
massiv = str(workers_sectors_number)
massiv =
print(f'{massiv}')