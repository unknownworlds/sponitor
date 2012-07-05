# Import data to MySQL database from JSON provided by the Google App Engine
from stats.models import EndGame, CPU, Performance, Kill

import json
import datetime

def importEndGame(path):
    mFile = open(path, 'r')
    data = json.loads(mFile.read())
    
    for line in data:
        if 'start_path_distance' in line:
            distance = line['start_path_distance']
        else:
            distance = -1
        eg = EndGame(version = str(line['version']), 
                     winner = line['winner'],
                     length = line['length'],
                     mapName = line['map'],
                     start_path_distance = distance,
                     date = datetime.datetime.fromtimestamp(line['date']/1000))
        eg.save()
        
def importCPU(path):
    mFile = open(path, 'r')
    data = json.loads(mFile.read())
    
    for line in data:
        cpu = CPU(cpuspeed = line['cpuspeed'], 
                  cpucores = line['cpucores'],
                  cpubits = line['cpubits'],
                  cpumem = line['cpumem'],
                  gpu = line['gpu'],
                  gpuver = line['gpuver'],
                  gpumem = line['gpumem'],
                  res = line['res'],
                  quality = line['quality'],
                  address = line['address'],
                  date = datetime.datetime.fromtimestamp(line['date']/1000))
        cpu.save()

def importKill(path):
    mFile = open(path, 'r')
    data = json.loads(mFile.read())
    
    for line in data:
        kill = Kill(version = str(line['version']), 
                    attacker_type = line['attacker_type'],
                    attacker_team = line['attacker_team'],
                    attacker_weapon = line['attacker_weapon'],
                    attackerx = line['attackerx'],
                    attackery = line['attackery'],
                    attackerz = line['attackerz'],
                    target_type = line['target_type'],
                    target_team = line['target_team'],
                    target_weapon = line['target_weapon'],
                    targetx = line['targetx'],
                    targety = line['targety'],
                    targetz = line['targetz'],
                    target_lifetime = line['target_lifetime'],
                    mapName = line['map'],
                    date = datetime.datetime.fromtimestamp(line['date']/1000))
        kill.save()

def importPerformance(path):
    mFile = open(path, 'r')
    data = json.loads(mFile.read())
    
    for line in data:
        perf = Performance(version = str(line['version']), 
                           mapName = line['map'],
                           serveravg = line['serveravg'],
                           ents = line['ents'],
                           clientmin = line['clientmin'],
                           clientmax = line['clientmax'],
                           clientavg = line['clientavg'],
                           date = datetime.datetime.fromtimestamp(line['date']/1000))
        perf.save()