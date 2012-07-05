from django.test.simple import DjangoTestSuiteRunner
from Sponitor import settings
from mongoengine.connection import connect, disconnect, get_connection


class MongoTestRunner(DjangoTestSuiteRunner):

    mongo_name = 'test_stats'

    def setup_databases(self, **kwargs):
    	#db_name = super(MongoTestRunner,self).setup_databases(**kwargs)

        disconnect()
        connect(self.mongo_name)
        print 'MongoTestRunner: setup %s' % (self.mongo_name)
        #return db_name
        return

    def teardown_databases(self, db_name, **kwargs):
    	#super(MongoTestRunner,self).teardown_databases(db_name, **kwargs)
        print 'MongoTestRunner: teardown %s' % (self.mongo_name)
        c = get_connection()
        c.drop_database(self.mongo_name)
        disconnect()