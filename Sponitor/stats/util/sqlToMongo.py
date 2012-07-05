from django.core.management import setup_environ
from Sponitor import settings
setup_environ(settings)

from django.contrib.auth.models import User as DjangoUser
from mongoengine.django.auth import User as MongoUser
import argparse

from Sponitor.stats import models as sql, mongoModels as mongo

parser = argparse.ArgumentParser(description='Convert django model from SQL model to MongoDB model')
parser.add_argument('--all', dest='all', action='store_true', help='convert every models')
parser.add_argument('--models', '-m', dest='models', nargs='*', help='convert specified models')
arguments = parser.parse_args()

i = 0
# User
if arguments.all or 'User' in arguments.models:
    for sqlRow in DjangoUser.objects.all():
        mongoRow = MongoUser()

        mongoRow.username = sqlRow.username
        mongoRow.first_name = sqlRow.first_name
        mongoRow.last_name = sqlRow.last_name
        mongoRow.email = sqlRow.email
        mongoRow.password = sqlRow.password
        mongoRow.is_staff = sqlRow.is_staff
        mongoRow.is_active = sqlRow.is_active
        mongoRow.is_superuser = sqlRow.is_superuser
        mongoRow.last_login = sqlRow.last_login
        mongoRow.date_joined = sqlRow.date_joined

        mongoRow.save()

        i += 1
        print "User" + str(i)


i = 0
# EndGame
if arguments.all or 'EndGame' in arguments.models:
    for sqlRow in sql.EndGame.objects.all():
        mongoRow = mongo.EndGame()

        mongoRow.version = sqlRow.version
        mongoRow.winner = sqlRow.winner
        mongoRow.length = sqlRow.length
        mongoRow.mapName = sqlRow.mapName
        mongoRow.start_location1 = sqlRow.start_location1
        mongoRow.start_location2 = sqlRow.start_location2
        mongoRow.start_path_distance = sqlRow.start_path_distance
        mongoRow.start_hive_tech = sqlRow.start_hive_tech
        mongoRow.date = sqlRow.date

        mongoRow.save()

        i += 1
        print "EndGame" + str(i)

i = 0
# CPU
if arguments.all or 'CPU' in arguments.models:
    for sqlRow in sql.CPU.objects.all():
        mongoRow = mongo.CPU()

        mongoRow.cpuspeed = sqlRow.cpuspeed
        mongoRow.cpucores = sqlRow.cpucores
        mongoRow.cpubits  = sqlRow.cpubits
        mongoRow.cpumem   = sqlRow.cpumem
        mongoRow.gpu      = sqlRow.gpu
        mongoRow.gpuver   = sqlRow.gpuver
        mongoRow.gpumem   = sqlRow.gpumem
        mongoRow.res      = sqlRow.res
        mongoRow.quality  = sqlRow.quality
        mongoRow.address  = sqlRow.address
        mongoRow.date     = sqlRow.date

        mongoRow.save()

        i += 1
        print "CPU" + str(i)

i = 0
# Framerate
if arguments.all or 'Framerate' in arguments.models:
    for sqlRow in sql.Framerate.objects.all():
        mongoRow = mongo.Framerate()

        mongoRow.version    = sqlRow.version  
        mongoRow.address    = sqlRow.address
        mongoRow.average    = sqlRow.average
        mongoRow.count      = sqlRow.count
        mongoRow.createDate = sqlRow.createDate
        mongoRow.updateDate = sqlRow.updateDate

        mongoRow.save()

        i += 1
        print "Framerate" + str(i)

i = 0
# Activity
if arguments.all or 'Activity' in arguments.models:
    for sqlRow in sql.Activity.objects.all():
        mongoRow = mongo.Activity()

        mongoRow.day              = sqlRow.day
        mongoRow.killCount        = sqlRow.killCount
        mongoRow.cpuCount         = sqlRow.cpuCount
        mongoRow.endGameCount     = sqlRow.endGameCount
        mongoRow.performanceCount = sqlRow.performanceCount

        mongoRow.save()

        i += 1
        print "Activity" + str(i)

i = 0
# Kill
if arguments.all or 'Kill' in arguments.models:
    for sqlRow in sql.Kill.objects.all():
        mongoRow = mongo.Kill()

        mongoRow.version         = sqlRow.version  
        mongoRow.mapName         = sqlRow.mapName
        mongoRow.attacker_type   = sqlRow.attacker_type
        mongoRow.attacker_team   = sqlRow.attacker_team
        mongoRow.attacker_weapon = sqlRow.attacker_weapon
        mongoRow.attackerx       = sqlRow.attackerx
        mongoRow.attackery       = sqlRow.attackery
        mongoRow.attackerz       = sqlRow.attackerz
        mongoRow.target_type     = sqlRow.target_type
        mongoRow.target_team     = sqlRow.target_team
        mongoRow.target_weapon   = sqlRow.target_weapon
        mongoRow.targetx         = sqlRow.targetx
        mongoRow.targety         = sqlRow.targety
        mongoRow.targetz         = sqlRow.targetz
        mongoRow.target_lifetime = sqlRow.target_lifetime
        mongoRow.date            = sqlRow.date

        mongoRow.save()

        i += 1
        print "Kill" + str(i)

i = 0
# Performance
if arguments.all or 'Performance' in arguments.models:
    for sqlRow in sql.Performance.objects.all():
        if i == 0:
            print "start the loop"
        mongoRow = mongo.Performance()

        mongoRow.version   = sqlRow.version  
        mongoRow.mapName   = sqlRow.mapName
        mongoRow.address   = sqlRow.address
        mongoRow.serveravg = sqlRow.serveravg
        mongoRow.ents      = sqlRow.ents
        mongoRow.clientmin = sqlRow.clientmin
        mongoRow.clientmax = sqlRow.clientmax
        mongoRow.clientavg = sqlRow.clientavg
        mongoRow.date      = sqlRow.date

        mongoRow.save()

        i += 1
        if i % 1000 == 0:
            print "Performance" + str(i)

print "-- end conversion --"



