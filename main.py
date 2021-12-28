import os
import time
import fileinput

sector_list = []
# dict.fromkeys(['PID', 'WORKER', 'STAGE', 'STATE', 'TIME'])
file_name = 'test.txt'
number = 1
workers = []
abnormal_count = 0
freezePC2_count = 0

#with open(file_name, mode='r', encoding='utf8') as file:
with fileinput.input() as file:
    for line in file:
        sector_list.append(dict(zip(['#PID', '#WORKER', '#STAGE', '#STATE', '#TIME'], line[:-1].split(' '))))

print(f'{sector_list}')
for sector in sector_list:
    workers.append(sector['#WORKER'])
    workerslist = list(set(workers))
    workerslist.sort()
workers_sectors_number = dict.fromkeys(workerslist, 0)
print(f'{workerslist}')
print(f'{workers_sectors_number}')

for sector in sector_list:
    for worker in workerslist:
        if sector['#WORKER'] == worker:
            workers_sectors_number[f'{worker}'] += 1
    if sector['#STAGE'] == 'abnormal':
        abnormal_count += 1
    if len(sector['#TIME']) > 8 and sector['#STAGE'] == 'PC2':
        print(sector['#TIME'], sector['#STAGE'], sector['#PID'])
        freezePC2_count += 1

print(f'abnormal_count = {abnormal_count}, freezePC2_count = {freezePC2_count}')
print(f'{workers_sectors_number}')
