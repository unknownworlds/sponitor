from django.http import HttpResponse
from stats.mongoModels import Kill, EndGame, Performance, CPU, Activity, Framerate

import datetime, json

def endgame(request):
    if not request.method == 'POST':
        return HttpResponse('See the documentation')
    
    POST = request.POST
    if not 'version' in POST and \
           'winner' in POST and \
           'length' in POST and \
           'start_location1' in POST and \
           'start_location2' in POST and \
           'start_path_distance' in POST and \
           'start_hive_tech' in POST and \
           'map' in POST: 
        return HttpResponse('See the documentation')
    
    eg = EndGame()
    eg.version = POST['version']
    eg.winner = int(POST['winner'])
    eg.length = float(POST['length'])
    eg.mapName = POST['map']
    eg.start_location1 = POST['start_location1']
    eg.start_location2 = POST['start_location2']
    eg.start_path_distance = float(POST['start_path_distance'])
    eg.start_hive_tech = POST['start_hive_tech']
    eg.date = datetime.datetime.now()
    eg.save()

    Activity.getTodayActivity().increment('endGame').save()

    return HttpResponse('saved')

def cpu(request):
    if not request.method == 'POST':
        return HttpResponse('See the documentation')
    
    POST = request.POST
    if not 'cpuspeed' in POST and \
           'cpucores' in POST and  \
           'cpubits' in POST and \
           'cpumem' in POST and \
           'gpu' in POST and \
           'gpuver' in POST and \
           'gpumem' in POST and \
           'res' in POST and \
           'quality' in POST:
        return HttpResponse('See the documentation')
    
    cpu = CPU()
    cpu.cpuspeed = int(POST['cpuspeed'])
    cpu.cpucores = int(POST['cpucores'])
    cpu.cpubits = int(POST['cpubits'])
    cpu.cpumem = float(POST['cpumem'])
    cpu.gpu = POST['gpu']
    cpu.gpuver = POST['gpuver']
    cpu.gpumem = float(POST['gpumem'])
    cpu.res = POST['res']
    cpu.quality = int(POST['quality'])
    cpu.address = request.META['REMOTE_ADDR']
    cpu.date = datetime.datetime.now()
    cpu.save()

    Activity.getTodayActivity().increment('cpu').save()

    return HttpResponse('saved')
    
def kill(request):
    if not request.method == 'POST':
        return HttpResponse('See the documentation')
    
    POST = request.POST
    if not 'version' in POST and \
           'map' in POST and  \
           'attacker_type' in POST and \
           'attacker_team' in POST and \
           'attacker_weapon' in POST and \
           'attackerx' in POST and \
           'attackery' in POST and \
           'attackerz' in POST and \
           'target_type' in POST and \
           'target_team' in POST and \
           'target_weapon' in POST and \
           'targetx' in POST and \
           'targety' in POST and \
           'targetz' in POST and \
           'target_lifetime' in POST:
        return HttpResponse('See the documentation')
    
    kill = Kill()
    kill.version = POST['version']
    kill.mapName = POST['map']
    kill.attacker_type = POST['attacker_type']
    kill.attacker_team = int(POST['attacker_team'])
    kill.attacker_weapon = POST['attacker_weapon']
    kill.attackerx = float(POST['attackerx'])
    kill.attackery = float(POST['attackery'])
    kill.attackerz = float(POST['attackerz'])
    kill.target_type = POST['target_type']
    kill.target_team = int(POST['target_team'])
    kill.target_weapon = POST['target_weapon']
    kill.targetx = float(POST['targetx'])
    kill.targety = float(POST['targety'])
    kill.targetz = float(POST['targetz'])
    kill.target_lifetime = float(POST['target_lifetime'])
    kill.date = datetime.datetime.now()

    if 'target_weaponlevel' in POST:
      kill.target_weaponlevel = POST['target_weaponlevel']
    if 'target_armorlevel' in POST:
      kill.target_armorlevel = POST['target_armorlevel']
    if 'attacker_weaponlevel' in POST:
      kill.attacker_weaponlevel = POST['attacker_weaponlevel']
    if 'attacker_armorlevel' in POST:
      kill.attacker_armorlevel = POST['attacker_armorlevel']

    if 'attacker_upgrade' in POST:
        if type(POST['attacker_upgrade']) is unicode or type(POST['attacker_upgrade']) is str:
            kill.attacker_upgrade = json.loads(POST['attacker_upgrade'])
        else:
            kill.attacker_upgrade = POST['attacker_upgrade']

    if 'target_upgrade' in POST:
        if type(POST['target_upgrade']) is unicode or type(POST['target_upgrade']) is str:
            kill.target_upgrade = json.loads(POST['target_upgrade'])
        else:
            kill.target_upgrade = POST['target_upgrade']


    kill.save()

    Activity.getTodayActivity().increment('kill').save()

    return HttpResponse('saved')

def performance(request):
    if not request.method == 'POST':
        return HttpResponse('See the documentation')
    
    POST = request.POST
    if not 'version' in POST and \
           'map' in POST and  \
           'serveravg' in POST and \
           'ents' in POST and \
           'clientmin' in POST and \
           'clientmax' in POST and \
           'clientavg' in POST:
        return HttpResponse('See the documentation')
    
    perf = Performance()
    perf.version = POST['version']
    perf.mapName = POST['map']
    perf.address = request.META['REMOTE_ADDR']
    perf.serveravg = float(POST['serveravg'])
    perf.ents = int(POST['ents'])
    perf.clientmin = float(POST['clientmin'])
    perf.clientmax = float(POST['clientmax'])
    perf.clientavg = float(POST['clientavg'])
    perf.date = datetime.datetime.now()
    perf.save()

    Activity.getTodayActivity().increment('performance').save()

    fps = { 'average' : perf.clientavg, 'minimum' : perf.clientmin, 'maximum' : perf.clientmax }
    Framerate.getFramerate(perf.version, perf.address).addFPS(fps).save()


    return HttpResponse('saved')
