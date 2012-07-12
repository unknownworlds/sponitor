from mongoengine import Document, StringField, IntField, FloatField, DateTimeField, ListField
from mongoengine.queryset import QuerySet
from mongoengine.connection import get_db

import datetime

class MyQuerySet(QuerySet):
    def fieldCount(self, key):
        collection_name = self._document._meta.get('collection')

        collection = get_db()[collection_name]

        if isinstance(key, str):
            keys = [key]
        else:
            keys = key

        init = {
            'count' : 0
        }

        red = '''
            function(doc, prev) {
                prev.count += 1;
            }
        '''

        fin = '''
            function(doc) {
                doc.%s__count = doc.count;
            }
        ''' % keys[0]

        return collection.group(keys, self._query, init, red, fin)

    def fieldAverage(self, key, field):
        collection_name = self._document._meta.get('collection')

        collection = get_db()[collection_name]

        init = {
            'total' : 0,
            'count' : 0
        }

        red = '''
            function(doc, prev) {
                prev.total += doc.%s;
                prev.count += 1;
            }
        ''' % field

        fin = '''
            function(doc) {
                doc.%s__average = (1.0 * doc.total) / (1.0 * doc.count);
            }
        ''' % field

        if isinstance(key, str):
            keys = [key]
        else:
            keys = key

        return collection.group(keys, self._query, init, red, fin)



class EndGame(Document):
    version             = StringField(max_length=255)
    winner              = IntField()
    length              = FloatField()
    mapName             = StringField(max_length=255)
    start_location1     = StringField(max_length=255)
    start_location2     = StringField(max_length=255)
    start_path_distance = FloatField()
    start_hive_tech     = StringField(max_length=255)
    date                = DateTimeField()

    meta = {
        'indexes' : ['version', 'winner', 'length', 'mapName', 'start_location1', 'start_location2', 'start_hive_tech'],
        'queryset_class': MyQuerySet
    }
    
class CPU(Document):
    cpuspeed = IntField()
    cpucores = IntField()
    cpubits  = IntField()
    cpumem   = FloatField()
    gpu      = StringField(max_length=255)
    gpuver   = StringField(max_length=255)
    gpumem   = FloatField()
    res      = StringField(max_length=255)
    quality  = IntField()    
    address  = StringField(max_length=255)
    date     = DateTimeField()

    meta = {
        'indexes' : ['cpubits', 'quality'],
        'queryset_class': MyQuerySet
    }
    
class Kill(Document):
    version              = StringField(max_length=255)
    mapName              = StringField(max_length=255)
    attacker_type        = StringField(max_length=255)
    attacker_team        = IntField()
    attacker_weapon      = StringField(max_length=255)
    attacker_weaponlevel = IntField()
    attacker_armorlevel  = IntField()
    attacker_upgrade     = ListField(field=StringField())
    attackerx            = FloatField()
    attackery            = FloatField()
    attackerz            = FloatField()
    target_type          = StringField(max_length=255)
    target_team          = IntField()
    target_weapon        = StringField(max_length=255)
    target_weaponlevel   = IntField()
    target_armorlevel    = IntField()
    target_upgrade       = ListField(field=StringField())
    targetx              = FloatField()
    targety              = FloatField()
    targetz              = FloatField()
    target_lifetime      = FloatField()
    date                 = DateTimeField()

    meta = {
        'indexes' : ['version', 'mapName', 'attacker_type', 'attacker_team', 'attacker_weapon', 'target_type', 'target_team', 'target_weapon', 'target_lifetime'],
        'queryset_class': MyQuerySet
    }
    
class Performance(Document):
    version   = StringField(max_length=255)
    mapName   = StringField(max_length=255) 
    address   = StringField(max_length=255)   
    serveravg = FloatField()    
    ents      = IntField()
    clientmin = FloatField()
    clientmax = FloatField()
    clientavg = FloatField()    
    date      = DateTimeField()

    meta = {
        'indexes' : ['version', 'mapName', 'serveravg', 'ents', 'clientavg'],
        'queryset_class': MyQuerySet
    }

class Framerate(Document):
    version    = StringField(max_length=255)
    address    = StringField(max_length=255)
    average    = FloatField(default=0)
    minimum    = FloatField(default=0)
    maximum    = FloatField(default=0)
    count      = IntField(default=0)
    createDate = DateTimeField()
    updateDate = DateTimeField()

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.createDate = datetime.datetime.now()

    meta = {
        'indexes' : [
            'average', 
            {
                'fields' : ('version', 'address'),
                'unique' : True
            }
        ],
        'queryset_class': MyQuerySet
    }

    def save(self, updateDate = True):
        if updateDate:
            self.updateDate = datetime.datetime.now()
            
        super(Framerate, self).save()

    def addFPS(self, fps):
        self.average = (self.average * self.count + fps['average']) / (self.count + 1)
        self.minimum = (self.minimum * self.count + fps['minimum']) / (self.count + 1)
        self.maximum = (self.maximum * self.count + fps['maximum']) / (self.count + 1)
        self.count += 1

        return self


    @classmethod
    def getFramerate(cls, ver, addr):
        try:
            framerate = cls.objects.get(version=ver, address=addr)
        except Framerate.DoesNotExist:
            framerate = cls.objects.create(version=ver, address=addr)

        return framerate

class Activity(Document):
    day              = DateTimeField()
    killCount        = IntField(default=0)
    cpuCount         = IntField(default=0)
    endGameCount     = IntField(default=0)
    performanceCount = IntField(default=0)

    meta = {
        'indexes' : [{ 
            'fields' : ('day',), 
            'unique' : True
        }],
        'queryset_class': MyQuerySet
    }

    def __init__(self, *args, **kwargs):
        super(Activity, self).__init__(*args, **kwargs)
        self.day = datetime.date.today()

    def increment(self, field):
        attr = field + 'Count'
        setattr(self, attr, getattr(self, attr) + 1)

        return self

    @classmethod
    def getTodayActivity(cls):
        try:
            activity = cls.objects.get(day=datetime.date.today())
        except Activity.DoesNotExist:
            activity = cls.objects.create()

        return activity

class Location(Document):
    version     = StringField(max_length=255)
    mapName     = StringField(max_length=255)
    x           = FloatField()
    y           = FloatField()
    z           = FloatField()
    message     = StringField()

    meta = {
        'indexes' : ['version', 'mapName'],
        'queryset_class': MyQuerySet
    }




