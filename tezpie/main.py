import logging
import os
import sys
import getopt

from .config import Config
from .p2p import PeerPool
from .crypto import Identity

logger = logging.getLogger('tezpie')

def usage ():
	print ('usage: tezpie [options]\n')
	print ('Options:')
	print ('  -h, --help\t\t\tdisplay this help')
	print ('  -V, --version\t\t\tdisplay the software version')
	print ('  -D, --data=path\t\tspecify a custom data directory path (default: %s)' % Config.get('data_dir'))
	print ('  -v, --verbose=n\t\tset verbosity level to n=[1-5] (default: %s)' % str(Config.get('verbose')))
	#print ('  -d,--daemon\t\t\trun the software as daemon')
	#print ('  -c,--chain=chainname\t\tblock-chain', '['+(', '.join (map (lambda x: "'"+x+"'", config.CHAINS)))+']')
	#print ('  -s,--seed=host:port,[host:port]\tset a contractvm seed nodes list')


def start():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "VD:v:h", ["version", "data=", "verbose=", "help"])
	except getopt.GetoptError:
		usage()
		sys.exit ()

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage ()
			sys.exit ()

		elif opt in ("-V", "--version"):
			print (Config.get('version'))
			sys.exit ()

		elif opt in ("-D", "--data"):
			Config.set('data_dir', os.path.expanduser (arg))

		elif opt in ("-v", "--verbose"):
			Config.set('verbose', int(arg))


	logger.info ('tezpie is starting')
	logger.debug ('directory set to %s', Config.get('data_dir'))

	for d in ['', '/blocks/', '/chainstate/']:
		if not os.path.isdir (Config.get('data_dir') + d):
			os.mkdir (Config.get('data_dir') + d)

	try:
		f = open (Config.get('data_dir') + '/pid', 'r')
		cpid = f.read ()
		f.close ()

		os.kill (int (cpid), signal.SIGKILL)
		logger.critical ('Already running, killed: ' + str (cpid))
	except:
		pass

	logger.setLevel (60 - Config.get('verbose') * 10)

	# Identity initialization
	try:
		identity = Identity.load()
	except:
		identity = Identity.generate()
		identity.save()


	pp = PeerPool(identity)
	#pp.listen()
	pp.bootstrap()