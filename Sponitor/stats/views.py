from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Count, Avg
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib.auth.decorators import login_required

from mongoengine.queryset import Q

from stats.mongoModels import Kill, EndGame, Performance, CPU, Framerate
from stats.helpers import findCategory, quantiles

import json, math, datetime

def home(request):
    return render_to_response('welcome.html')

@login_required(login_url='/login/')
def webapp(request):
    return render_to_response('webapp.html')

@login_required(login_url='/login/')
def flush(request):
    cache.clear()
    return HttpResponse('flushed')

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def winPie(request):
    GET = request.GET
    endGameQuery = EndGame.objects.all()
    
    endGameQuery = filterByMapAndVersion(endGameQuery, GET)
    endGameQuery = filterByLocation(endGameQuery, GET)
        
    t1 = endGameQuery.clone().filter(winner=1).count()
    t2 = endGameQuery.clone().filter(winner=2).count()
    data = { 
        'data' : [
            ['Marines', t1],
            ['Aliens', t2]
        ],
        'colors' : [
            '#3366cc',
            '#dc3912'
        ]
    }
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 *60 *2)
def lifetime(request):
    GET = request.GET
    killQuery = Kill.objects.all()
        
    killQuery = filterByMapAndVersion(killQuery, GET)
        
    #killQuery = killQuery.values('target_type').annotate(Count('target_type')) \
    #    .annotate(lifetime_avg=Avg('target_lifetime')) \
    #    .values('target_type', 'lifetime_avg') \
    #    .order_by('lifetime_avg')

    killQuery = killQuery.scalar('target_type', 'target_lifetime').fieldAverage('target_type', 'target_lifetime')
    
    dataJSON = json.dumps(list(killQuery))    
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 *60 *2)
def startlocationCount(request):
    GET = request.GET
    endQuery1 = EndGame.objects.all()
        
    endQuery1 = filterByMapAndVersion(endQuery1, GET)
        
    endQuery1 = endQuery1.scalar('start_location1').fieldCount('start_location1')

    endQuery2 = EndGame.objects.all()
        
    endQuery2 = filterByMapAndVersion(endQuery2, GET)
        
    endQuery2 = endQuery2.scalar('start_location2').fieldCount('start_location2')

    data = {
        'type1' : list(endQuery1),
        'type2' : list(endQuery2)
    } 
    
    dataJSON = json.dumps(data)    
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def resolution(request):
    cpuQuery = CPU.objects.all().scalar('res').fieldCount('res')
    r = [ [row['res'], row['res__count']]for row in list(cpuQuery)]
    r = sorted(r, key=lambda x: -x[1])
    
    data = []
    for d in r:
        if d[1] > 20:
            data.append(d)
    data = {
        'data': data
    }
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def winBar(request):
    GET = request.GET
    endGameQuery = EndGame.objects.all()
    
    # set data config
    if 'delta' in GET:
        delta = int(GET['delta'])
    else:
        delta = 10
    
    if 'offset' in GET:
        offset = int(GET['offset'])
    else:    
        offset = 5
        
    iMax = math.floor((90 - offset) / delta)
    unit = 'min'
    
    endGameQuery = filterByMapAndVersion(endGameQuery, GET)
    endGameQuery = filterByLocation(endGameQuery, GET)
    
    q1 = endGameQuery.clone().filter(winner=1)
    q2 = endGameQuery.clone().filter(winner=2)
    average = endGameQuery.clone().average('length')
    
    data1 = {} 
    for g in q1:
        l = g.length
        i,cat = findCategory(l / 60, delta, iMax, unit,offset)
        if i >= 0:
            if not data1.has_key(i):
                data1[i] = {'cat': cat, 'count':0}
            data1[i]['count'] += 1
    data1 = [ [key, val] for key, val in data1.items()]
    
    data2 = {}
    for g in q2:
        l = g.length
        i,cat = findCategory(l / 60, delta, iMax, unit,offset)
        if i >= 0:
            if not data2.has_key(i):
                data2[i] = {'cat': cat, 'count':0}
            data2[i]['count'] += 1
    data2 = [ [key, val] for key, val in data2.items()]

    data = []
    for ii in range( min(len(data1),len(data2)) ):
        data.append([
            data1[ii][1]['cat'],
            data1[ii][1]['count'],
            data2[ii][1]['count']
        ])
    
    data = {
        'data': data,
        'average': int(average),
        'order': ['Marines','Aliens'],
        'colors' : [
                '#3366cc',
                '#dc3912'
        ]        
    }
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def winDistanceBar(request):
    GET = request.GET
    endGameQuery = EndGame.objects.all()
    
    # set data config
    if 'delta' in GET:
        delta = int(GET['delta'])
    else:
        delta = 50
    
    if 'offset' in GET:
        offset = int(GET['offset'])
    else:    
        offset = 0
        
    iMax = math.floor((350 - offset) / delta)
    unit = 'm'
    
    endGameQuery = filterByMapAndVersion(endGameQuery, GET)
    endGameQuery = filterByLocation(endGameQuery, GET)
    
    q1 = endGameQuery.clone().filter(winner=1)
    q2 = endGameQuery.clone().filter(winner=2)
    
    data1 = {}
    for g in q1:
        l = g.start_path_distance
        i,cat = findCategory(l , delta, iMax, unit,offset)
        if i >= 0:
            if not data1.has_key(i):
                data1[i] = {'cat': cat, 'count':0}
            data1[i]['count'] += 1
    data1 = [ [key, val] for key, val in data1.items()]
    
    data2 = {}
    for g in q2:
        l = g.start_path_distance
        i,cat = findCategory(l , delta, iMax, unit,offset)
        if i >= 0:
            if not data2.has_key(i):
                data2[i] = {'cat': cat, 'count':0}
            data2[i]['count'] += 1
    data2 = [ [key, val] for key, val in data2.items()]

    data = []
    for ii in range( min(len(data1),len(data2)) ):
        data.append([
            data1[ii][1]['cat'],
            data1[ii][1]['count'],
            data2[ii][1]['count']
        ])
    
    data = {
        'data': data,
        'order': ['Marines','Aliens'],
        'colors' : [
                '#3366cc',
                '#dc3912'
        ]        
    }
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def killPie(request):
    GET = request.GET
    killQuery = Kill.objects.all()
    
    killQuery = filterByMapAndVersion(killQuery, GET)
    
    t1 = killQuery.clone().filter(attacker_team=1)
    t2 = killQuery.clone().filter(attacker_team=2)

    if 'type1' in GET and 'type2' in GET:
        t1.filter(attacker_type=GET['type1'], target_type=GET['type2'])
        t2.filter(attacker_type=GET['type2'], target_type=GET['type1'])

    if 'weapon1' in GET and 'weapon2' in GET:
        t1.filter(attacker_weapon=GET['weapon1'], target_weapon=GET['weapon2'])
        t2.filter(attacker_weapon=GET['weapon2'], target_weapon=GET['weapon1'])

    if 'weaponlevel1' in GET:
        t1.filter(attacker_weaponlevel=GET['weaponlevel1'])
        t2.filter(target_weaponlevel=GET['weaponlevel1'])

    if 'weaponlevel2' in GET:
        t2.filter(attacker_weaponlevel=GET['weaponlevel2'])
        t1.filter(target_weaponlevel=GET['weaponlevel2'])

    if 'armorlevel1' in GET:
        t1.filter(attacker_armorlevel=GET['armorlevel1'])
        t2.filter(target_armorlevel=GET['armorlevel1'])

    if 'armorlevel2' in GET:
        t2.filter(attacker_armorlevel=GET['armorlevel2'])
        t1.filter(target_armorlevel=GET['armorlevel2'])

    if 'upgrade1' in GET:
        try:
            upgrades = json.loads(GET['upgrades'])

            for u in upgrades:
                t1.filter(attacker_upgrade__all=u)
                t2.filter(target_upgrade__all=u)
        except:
            t1.filter(attacker_upgrade__all=GET['upgrade1'])
            t2.filter(target_upgrade__all=GET['upgrade1'])

    if 'upgrade2' in GET:
        try:
            upgrades = json.loads(GET['upgrade2'])

            for u in upgrades:
                t2.filter(attacker_upgrade__all=u)
                t1.filter(target_upgrade__all=u)
        except:
            t2.filter(attacker_upgrade__all=GET['upgrade2'])
            t1.filter(target_upgrade__all=GET['upgrade2'])

    data = { 
        'data' : [
            ['Marines', t1.count()],
            ['Aliens', t2.count()]
        ],
        'colors' : [
            '#3366cc',
            '#dc3912'
        ]
    }
    
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def killWeaponPie(request):
    GET = request.GET
    killQuery = Kill.objects.all()
    
    # Need a duel
    if not ('type1' in GET and 'type2' in GET):
        return HttpResponse('[]')
    
    killQuery = filterByMapAndVersion(killQuery, GET)
        
    q1 = killQuery.clone().filter(attacker_type=GET['type1'],target_type=GET['type2']).fieldCount(['attacker_weapon', 'target_weapon'])
    q2 = killQuery.clone().filter(attacker_type=GET['type2'],target_type=GET['type1']).fieldCount(['attacker_weapon', 'target_weapon'])

    duelList = {}
    for duel in q1:
        print duel
        duelName = duel['attacker_weapon'] + ' vs ' + duel['target_weapon']
        type1Name = GET['type1'] + ' - ' + duel['attacker_weapon']
        duelList[ duelName ] = [ { 'label' : type1Name, 'data' : duel['attacker_weapon__count']}]
    for duel in q2:
        duelName = duel['target_weapon'] + ' vs ' + duel['attacker_weapon']
        type2Name = GET['type2'] + ' - ' + duel['attacker_weapon']
        if not duelList.has_key( duelName ):
            duelList[ duelName ] = []
        duelList[ duelName ].append( { 'label' : type2Name, 'data' : duel['attacker_weapon__count']} )
    

    duelList = [{'name' : key, 'statistics' : val } for key, val in duelList.items()]
    
    
    def sortKey(x):
        if len(x['statistics']) > 0 and x['statistics'][0].has_key('data'):
            a = x['statistics'][0]['data']
        else:
            a = 0
            
        if len(x['statistics']) > 1 and x['statistics'][1].has_key('data'):
            b = x['statistics'][1]['data']
        else:
            b = 0
        
        a = a * 10000 / (a + b) # need precision for comparing division
        b = b * 10000 / (a + b)
        return max(a,b)
    duelList = sorted(duelList, key=sortKey)
    
    data = []
    for row in duelList:
        if len( row['statistics'] ) > 1:
            data.append( [row['name'],row['statistics'][0]['data'],row['statistics'][1]['data']] )
    
    data = {
        'data': data,
        'colors': [
            '#3366cc',
            '#dc3912'
        ],
        'order': [
            'Type1',
            'Type2'
        ]
    }  
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def playerPerformance(request):
    versions = list(Framerate.objects.all().distinct('version'))
    def safeInt(x):
        try:
            return int(x)
        except:
            return 0
    versions = [ v for v in versions if safeInt(v) >= 208 ]

    data = []
    for version in versions:
        query = Framerate.objects.all().filter(version=version)
        f = [ row.average for row in query]
        avg = query.average('average')
        percentiles = quantiles(100, f)

        if len(percentiles) < 99:
            continue

        data.append([
            version,
            avg,
            percentiles[49],
            percentiles[24],
            percentiles[74],
            percentiles[9],
            percentiles[89],
            percentiles[0],
            percentiles[98]
        ])

        data.sort(key=lambda x: x[0])

    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)
        
@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def gpu(request):
    cpuQuery = CPU.objects.all()
    nvidia = cpuQuery.clone().filter(gpu__startswith = 'NVIDIA').count()
    ati = cpuQuery.clone().filter(Q(gpu__startswith = 'AMD') | Q(gpu__startswith = 'ATI') ).count()
    
    data = { 
        'data' : [
            ['Nvidia', nvidia],
            ['ATI', ati]
        ],
        'colors' : [
            '#18ba39',
            '#dc3912'
        ]
    }
    
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def cpucore(request):
    cpuQuery = CPU.objects.all().scalar('cpucores').fieldCount('cpucores')
    
    data = { 
        'data' : [ [str(c['cpucores']), c['cpucores__count']] for c in cpuQuery]
    }
    
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def cpuspeed(request):
    cpuQuery = CPU.objects.all().scalar('cpuspeed')
    data = {}
    for c in cpuQuery:
        i,cat = findCategory(c * 1.0 / 1000,0.5,6,'GHz')
        if not data.has_key(cat):
            data[cat] = 0
        data[cat] += 1
    
    data = { 
        'data' : [ [str(key), val] for key, val in data.items()]
    }
    
    dataJSON = json.dumps(data)
    return HttpResponse(dataJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def typeList(request):
    types = list(Kill.objects.all().distinct('attacker_type'))
    types = [{'name': t} for t in types]
    typesJSON = json.dumps(types)
    return HttpResponse(typesJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def startLocation1List(request):
    GET = request.GET
    
    query = EndGame.objects.all().filter(start_location1__ne=None)
    query = filterByMapAndVersion(query, GET)
    
    locations = list( query.distinct('start_location1') )
    
    locations = [{'name': t} for t in locations]
    locationsJSON = json.dumps(locations)
    return HttpResponse(locationsJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def startLocation2List(request):
    GET = request.GET
    
    query = EndGame.objects.all().filter(start_location2__ne=None)
    query = filterByMapAndVersion(query, GET)
    
    locations = list( query.distinct('start_location2') )
    
    locations = [{'name': t} for t in locations]
    locationsJSON = json.dumps(locations)
    return HttpResponse(locationsJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def weaponList(request):
    GET = request.GET
    killQuery = Kill.objects.all()
    
    # GET filtering
    if 'type' in GET:
        killQuery = killQuery.filter(attacker_type=GET['type'])
        
    weapons = list(killQuery.distinct('attacker_weapon'))
    weapons = [w[0] for w in weapons]
    weaponsJSON = json.dumps(weapons)
    return HttpResponse(weaponsJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def mapList(request):
    types = list(EndGame.objects.all().distinct('mapName'))
    types = [ { 'name': t} for t in types]
    typesJSON = json.dumps(types)
    return HttpResponse(typesJSON)

@login_required(login_url='/login/')
@cache_page(60 * 60 * 2)
def versionList(request):
    types = list(EndGame.objects.all().distinct('version'))
    types = [ { 'name': t} for t in types if t.isdigit() ]
    types.sort(key=lambda t: int(t['name']))
    typesJSON = json.dumps(types)
    return HttpResponse(typesJSON)

def filterByMapAndVersion(query, GET):
    
    if 'version' in GET:
        versions = json.loads( GET['version'] )
        
        if not isinstance(versions, list):
            versions = [ versions ]
        
        versions = map(str, versions)        
        query = query.filter(version__in=versions)
        
    if 'map' in GET:
        maps = json.loads( GET['map'] )
        
        if not isinstance(maps, list):
            maps = [ maps ]
        
        maps = map(str, maps)
        query = query.filter(mapName__in=maps)
        
    return query

def filterByLocation(query, GET):
    
    if 'location1' in GET:
        location1 = GET['location1']              
        query = query.filter(start_location1=location1)

    if 'location2' in GET:
        location2 = GET['location2']
        query = query.filter(start_location2=location2)
        
    return query