from django.test import TestCase
from django.test.client import Client

from stats.mongoModels import Kill, EndGame, Performance, CPU, Activity, Framerate, Location
from stats.mongoModels import MyQuerySet
from stats import statsTools

from mongoengine import Document, StringField, FloatField

import json

import datetime

####### FIXTURES #######
class Post(Document):
    nom   = StringField(max_length=255)
    tag   = StringField(max_length=255)
    value = FloatField()

    meta = {
        'queryset_class': MyQuerySet
    }

def testAttr(testClass, obj, data):
    for key, val in data.iteritems():
        attr = key

        if key == "map":
            attr = "mapName"

        if key.find("_upgrade") >= 0:
            val = json.loads(val)

        testClass.assertEqual(val, getattr(obj, attr), msg=("[key]: %s, [left] %s, [right] %s" % (key, val, getattr(obj, attr)) ) )

def testDict(testClass, d1, d2):
    print d1
    print d2
    for k, v in d1.iteritems():
        testClass.assertEquals(d1[k], d2[k])

    for k, v in d2.iteritems():
        testClass.assertEquals(d1[k], d2[k])

####### STATSTOOLS TEST #######
class StatsToolsTest(TestCase):
    def test_quantiles(self):
        s1 = [1, 3, 7, 8, 9]
        s2 = [2, 6, 9, 22, 11, 10.3]
        s3 = [1, 2, 7, 3, 5, 8, 8, 2, 98, 56, 23]

        self.assertEquals( statsTools.quantiles(2, s1), [7])
        self.assertEquals( statsTools.quantiles(3, s1), [3, 8])
        self.assertEquals( statsTools.quantiles(6, s2), [6, 9, 10.3, 11, 22])
        self.assertEquals( statsTools.quantiles(7, s2), [2, 6, 9, 10.3, 11, 22])
        self.assertEquals( statsTools.quantiles(2, s2), [10.3])
        self.assertEquals( statsTools.quantiles(2, s3), [7])
        self.assertEquals( statsTools.quantiles(2, s3)[0], statsTools.quantiles(4, s3)[1])

####### MYQUERYSET TEST #######
class MyQuerySetTest(TestCase):

    def test_count(self):
        Post.drop_collection()

        post1 = Post()
        post1.nom = "Jean"
        post1.tag = "son"
        post1.save()

        post2 = Post()
        post2.nom = "Marie"
        post2.tag = "daughter"
        post2.save()

        post3 = Post()
        post3.nom = "Paul"
        post3.tag = "son"
        post3.save()

        r = Post.objects.all().fieldCount('tag')

        for item in r:
            if item['tag'] == "son":
                self.assertEqual(item['tag__count'], 2)

            if item['tag'] == "daughter":
                self.assertEqual(item['tag__count'], 1)

    def test_average(self):
        Post.drop_collection()

        post1 = Post()
        post1.nom = "Jean"
        post1.tag = "son"
        post1.value = 2
        post1.save()

        post2 = Post()
        post2.nom = "Marie"
        post2.tag = "daughter"
        post2.value = 2
        post2.save()

        post3 = Post()
        post3.nom = "Paul"
        post3.tag = "son"
        post3.value = 4
        post3.save()

        r = Post.objects.all().fieldAverage('tag', 'value')

        for item in r:
            if item['tag'] == "son":
                self.assertEqual(item['value__average'], 3)

            if item['tag'] == "daughter":
                self.assertEqual(item['value__average'], 2)


######## API TEST #######
class APITest(TestCase):

    def setUp(self):
        self.address = '127.0.0.1'
        self.client  = Client(REMOTE_ADDR=self.address)

    def test_endgame(self): 
        endgame = {
            'version' : '200', 
            'winner' : 1, 
            'length' : 1254,
            'start_location1' : 'foo',
            'start_location2' : 'bar',
            'start_path_distance' : 383,
            'start_hive_tech' : 'wut',
            'map' : 'ns2_python'
        }

        before = (EndGame.objects.all().count(), Activity.getTodayActivity().endGameCount)
        self.client.post('/endgame', endgame)
        after = (EndGame.objects.all().count(), Activity.getTodayActivity().endGameCount)

        self.assertEqual(before[0] + 1, after[0])
        self.assertEqual(before[1] + 1, after[1])
        testAttr(self, EndGame.objects.all().order_by('-date')[0], endgame)

    def test_performance(self):
        perf = {
            'version' : '200', 
            'map' : 'ns2_python',
            'serveravg' : 43,
            'ents' : 342,
            'clientmin' : 12,
            'clientmax' : 45,
            'clientavg' : 32
        }
        address = self.address

        before = (
            Performance.objects.all().count(), 
            Activity.getTodayActivity().performanceCount,
            Framerate.getFramerate(perf['version'], address).average
        )
        self.client.post('/performance', perf)
        after = (
            Performance.objects.all().count(), 
            Activity.getTodayActivity().performanceCount,
            Framerate.getFramerate(perf['version'], address).average
        )

        count = Framerate.getFramerate(perf['version'], address).count
        testAttr(self, Performance.objects.all().order_by('-date')[0], perf)
        self.assertEqual(before[0] + 1, after[0])
        self.assertEqual(before[1] + 1, after[1])
        self.assertEqual(before[2] * (count-1) + perf['clientavg'] / count, after[2])
        

    def test_kill(self):
        kill = {
            'version' : '200',
            'map' : 'ns2_python',
            'attacker_type' : 'Marine',
            'attacker_team' : 1,
            'attacker_weapon' : 'Bite',
            'attackerx' : 4.3,
            'attackery' : 45.21,
            'attackerz' : 3.12,
            'attacker_weaponlevel' : 2,
            'attacker_armorlevel' : 4,
            'attacker_upgrade' : json.dumps(['Carapace', 'Aura']),
            'target_type' : 'Onos',
            'target_team' : 2,
            'target_weapon' : 'Gun',
            'target_weaponlevel' : 3,
            'target_armorlevel' : 0,
            'target_upgrade' : json.dumps(['Speed']),
            'targetx' : 2,
            'targety' : 8,
            'targetz' : 34,
            'target_lifetime' : 234
        }

        before = (Kill.objects.all().count(), Activity.getTodayActivity().killCount)
        self.client.post('/kill', kill)
        after = (Kill.objects.all().count(), Activity.getTodayActivity().killCount)

        self.assertEqual(before[0] + 1, after[0])
        self.assertEqual(before[1] + 1, after[1])
        testAttr(self, Kill.objects.all().order_by('-date')[0], kill)

    def test_location(self):
        location = {
            'version' : '200',
            'map' : 'ns2_python',
            'message' : 'This is an awesome info',
            'x' : 3.4,
            'y' : 9.0,
            'z' : 34.897
        }

        before = Location.objects.all().count()
        self.client.post('/location', location)
        after = Location.objects.all().count()

        self.assertEqual(before + 1, after)
        testAttr(self, Location.objects.all()[0], location)

        locationsJSON = self.client.get('/location', {'version' : '200', 'map' : 'ns2_python'}).content
        location_bis = json.loads(locationsJSON)[0]
        testDict(self, location, location_bis)

    def test_cpu(self):
        cpu = {
            'cpuspeed' : 54,
            'cpucores' : 3,
            'cpubits' : 32,
            'cpumem' : 1024,
            'gpu' : 'Nvidia truc',
            'gpuver' : '2',
            'gpumem' : 192,
            'res' : '640x480',
            'quality' : 2
        }

        before = (CPU.objects.all().count(), Activity.getTodayActivity().cpuCount)
        self.client.post('/cpu', cpu)
        after = (CPU.objects.all().count(), Activity.getTodayActivity().cpuCount)

        self.assertEqual(before[0] + 1, after[0])
        self.assertEqual(before[1] + 1, after[1])      
        testAttr(self, CPU.objects.all().order_by('-date')[0], cpu)

    def test_activity(self):
        todayActivity = Activity.getTodayActivity()
        kill = todayActivity.killCount
        perf = todayActivity.performanceCount
        endgame = todayActivity.endGameCount
        cpu = todayActivity.cpuCount

        for _ in range(2):
            Activity.getTodayActivity().increment('kill').save()
        for _ in range(5):
            Activity.getTodayActivity().increment('performance').save()
        for _ in range(2):
            Activity.getTodayActivity().increment('endGame').save()
        for _ in range(3):
            Activity.getTodayActivity().increment('cpu').save()

        Activity.getTodayActivity().increment('cpu').increment('kill').save()

        activity = Activity.getTodayActivity()

        self.assertEqual(activity.day, datetime.date.today())
        self.assertEqual(activity.killCount, kill + 3)
        self.assertEqual(activity.performanceCount, perf + 5)
        self.assertEqual(activity.endGameCount, endgame + 2)
        self.assertEqual(activity.cpuCount, cpu + 4)

    def test_framerate(self):
        ver = "192"
        addr = "127.0.0.1"
        fps = { 'average' : 23.0, 'minimum' : 2.0, 'maximum' : 48.0 }
        fps1 = { 'average' : 40.0, 'minimum' : 7.0, 'maximum' : 62.0 }
        fps2 = { 'average' : 50.0, 'minimum' : 11.0, 'maximum' : 76.0 }
        fps3 = { 'average' : 32.0, 'minimum' : 4.0, 'maximum' : 53.0 }
        initAvg =  Framerate.getFramerate(ver, addr).average
        initMin =  Framerate.getFramerate(ver, addr).minimum
        initMax =  Framerate.getFramerate(ver, addr).maximum
        initCount = Framerate.getFramerate(ver, addr).count

        Framerate.getFramerate(ver, addr).addFPS(fps).save()

        framerate = Framerate.objects.create(version="208", address="192.168.0.1")
        framerate.addFPS(fps1)
        framerate.addFPS(fps2)
        framerate.addFPS(fps3)

        self.assertEqual(framerate.average, (40.0+50.0+32.0) / 3)
        self.assertEqual(framerate.minimum, (7.0+11.00+4.0) / 3)
        self.assertEqual(framerate.maximum, (62.0+76.0+53.0) / 3)
        self.assertEqual(
            Framerate.getFramerate(ver, addr).average, 
            (initCount * initAvg + fps['average']) / (initCount + 1) 
        )
        self.assertEqual(
            Framerate.getFramerate(ver, addr).minimum, 
            (initCount * initMin + fps['minimum']) / (initCount + 1) 
        )
        self.assertEqual(
            Framerate.getFramerate(ver, addr).maximum, 
            (initCount * initMax + fps['maximum']) / (initCount + 1) 
        )




