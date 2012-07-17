# Rebuild Framerate data from Performance data

from django.core.management import setup_environ
from Sponitor import settings
setup_environ(settings)

from stats.mongoModels import Performance, Framerate

import argparse

parser = argparse.ArgumentParser(description='Rebuild Framerate data from Performance data.')
parser.add_argument('--versions', dest='versions', nargs='+', type=str, action='store', help='choose versions to rebuild')
versions = parser.parse_args().versions

print "Versions: " + str(versions)

count = 0

Framerate.objects.all().filter(version__in=versions).delete()
print "Old framerate are deleted."

for perf in Performance.objects.all().filter(version__in=versions):
	fps = { 'average' : perf.clientavg, 'minimum' : perf.clientmin, 'maximum' : perf.clientmax }
	Framerate.getFramerate(perf.version, perf.address).addFPS(fps).save()
	
	count += 1
	if count % 1000 == 0:
		print "Process %i raws." % count
		print "Last versions: " + perf.version
