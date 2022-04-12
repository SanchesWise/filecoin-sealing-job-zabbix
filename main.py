#!/usr/bin/env python3

import fileinput
import json
import os
import subprocess
from datetime import datetime

sector_list = []
# dict.fromkeys(['PID', 'WORKER', 'STAGE', 'STATE', 'TIME'])
file_name = 'test.txt'
number = 1
workers = []
abnormal_count = 0
freezePC2_count = 0
workerPC1count = 2
workerPC1current_count = 0
workerGETcurrent_count = 0
workerPC1summary_sectors = 0
workerGETsummary_sectors = 0
dict_blanc = ['#PID', '#WORKER', '#STAGE', '#STATE', '#TIME']
worker_phase_list = []
json_ready = []

#with open(file_name, mode='r', encoding='utf8') as file:
with fileinput.input() as file:
    for line in file:
        CurrentLine = dict(zip(dict_blanc, line[:-1].split(' ')))
        #print(f'{CurrentLine}')
        try:
            if CurrentLine['#TIME']:
                sector_list.append(CurrentLine)
        except KeyError:
            command = (f'/usr/local/bin/lotus-miner sealing abort {CurrentLine["#PID"]} >> /var/log/filecoin-zabbix/pledge.log 2>&1')
            os.system(f'{command}')
            #print(f'{command}')


for sector in sector_list:
    workers.append(sector['#WORKER'])
workerslist = list(set(workers))
workerslist.sort()
for worker in workerslist:
    worker_phase_list.append(f'{worker}_TOTAL')
    worker_phase_list.append(f'{worker}_PC1')
    worker_phase_list.append(f'{worker}_PC2')
    worker_phase_list.append(f'{worker}_GET')
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
            if sector['#STAGE'] == "GET":
                workers_sectors_number[f"{worker}_GET"] += 1
    if sector['#STAGE'] == 'abnormal':
        abnormal_count += 1
    if len(sector['#TIME']) > 8 and sector['#STAGE'] == 'PC2':
        command = (
            f'/usr/local/bin/lotus-miner sealing abort {sector["#PID"]} >> /var/log/filecoin-zabbix/pledge.log 2>&1')
        os.system(f'{command}')
        freezePC2_count += 1

for key in workers_sectors_number:
    if workers_sectors_number[key] > 0 and "PC1" in key:
        workerPC1current_count += 1
        workerPC1summary_sectors += workers_sectors_number[key]
    if workers_sectors_number[key] > 0 and "GET" in key:
        workerGETcurrent_count += 1
        workerGETsummary_sectors += workers_sectors_number[key]

with open("/var/log/filecoin-zabbix/pledge.log", mode='a', encoding='utf8') as file:
    file.write(f'{datetime.today()}  Summary sectors in PC1 state: {workerPC1summary_sectors}\n')
    file.write(f'{datetime.today()}  Summary sectors in GET state: {workerGETsummary_sectors}\n')
    #StringCount = len(file.readlines())
    #file.write(f'{datetime.today()}  Log lenght: {StringCount}\n')
if workerPC1summary_sectors < 25 and workerGETsummary_sectors < 10:
    os.system("/usr/local/bin/lotus-miner sectors pledge >> /var/log/filecoin-zabbix/pledge.log 2>&1")
    #with open("/var/log/filecoin-zabbix/pledge.log", mode='a', encoding='utf8') as file:
        #file.write(f'{datetime.today()}  Summary sectors PC1 : {workerPC1summary_sectors}\n ')
        #os.system("/usr/local/bin/lotus-miner sectors pledge >> /var/log/filecoin-zabbix/pledge.log 2>&1")
        #status = subprocess.check_output(["/usr/local/bin/lotus-miner", "sectors", "pledge"], stderr=subprocess.STDOUT)
        #file.write(f'action : {status.decode("utf-8")}\n')



if workerPC1current_count < workerPC1count:
    pass
#print(f'{workers_sectors_number}')
#print(f'workerPC1summary_sectors {workerPC1summary_sectors} workerPC1current_count {10*workerPC1current_count}')
#print(workerPC1summary_sectors)

for keys in workers_sectors_number:
    json_ready.append({'name': keys, 'value': workers_sectors_number[keys]})
json_ready.append({'name': "FreezePC2_count", 'value': freezePC2_count})
#print(json_ready)
json_object = json.dumps(json_ready, indent=1)
print(f'{json_object}')

#[f"\x7B#{worker}_TOTAL\x7D" \x7B"data": \x7D
