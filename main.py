#!/usr/bin/env python3

import fileinput
import json

sector_list = []
# dict.fromkeys(['PID', 'WORKER', 'STAGE', 'STATE', 'TIME'])
file_name = 'test.txt'
number = 1
workers = []
abnormal_count = 0
freezePC2_count = 0
workerPC1count = 2
workerPC1current_count = 0
workerPC1summary_sectors = 0
dict_blanc = ['#PID', '#WORKER', '#STAGE', '#STATE', '#TIME']
worker_phase_list = []
json_ready = []

with open(file_name, mode='r', encoding='utf8') as file:
#with fileinput.input() as file:
    for line in file:
        sector_list.append(dict(zip(dict_blanc, line[:-1].split(' '))))

# print(f'{sector_list}')
for sector in sector_list:
    workers.append(sector['#WORKER'])
workerslist = list(set(workers))
workerslist.sort()
for worker in workerslist:
    worker_phase_list.append(f'{worker}_TOTAL')
    worker_phase_list.append(f'{worker}_PC1')
    worker_phase_list.append(f'{worker}_PC2')
# print(f"{worker_phase_list}")
workers_sectors_number = {worker: 0 for worker in worker_phase_list}

for sector in sector_list:
    for worker in workerslist:
        if sector['#WORKER'] == worker:
            workers_sectors_number[f"{worker}_TOTAL"] += 1
            if sector['#STAGE'] == "PC1":
                workers_sectors_number[f"{worker}_PC1"] += 1
            if sector['#STAGE'] == "PC2":
                workers_sectors_number[f"{worker}_PC2"] += 1
    if sector['#STAGE'] == 'abnormal':
        abnormal_count += 1
    if len(sector['#TIME']) > 8 and sector['#STAGE'] == 'PC2':
        # print(sector['#TIME'], sector['#STAGE'], sector['#PID'])
        freezePC2_count += 1

for key in workers_sectors_number:
    if workers_sectors_number[key] > 0 and "PC1" in key:
        workerPC1current_count += 1
        workerPC1summary_sectors += workers_sectors_number[key]

if workerPC1summary_sectors < 10 * workerPC1current_count:
    pass
if workerPC1current_count < workerPC1count:
    pass
# print(f'abnormal_count = {abnormal_count}, freezePC2_count = {freezePC2_count}')
# print(f'{workers_sectors_number}')
# print(f'workerPC1summary_sectors {workerPC1summary_sectors} workerPC1current_count {10*workerPC1current_count}')


# [{"{#UNIT.NAME}":"console-screen.service",
for keys in workers_sectors_number:
    json_ready.append({'\x7B#NAME\x7D': keys, '\x7B#VALUE\x7D': workers_sectors_number[keys]})

#print(json_ready)
json_object = json.dumps(json_ready, indent=1)
print(json_object)

#[f"\x7B#{worker}_TOTAL\x7D"