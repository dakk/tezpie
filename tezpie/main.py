import logging
import os
import sys
import getopt
import binascii

from .config import Config
from .p2p import PeerPool
from .p2p.messages import ConnectionMessage
from .crypto import Identity, Nonce, KeyBox

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

	"""
	n = Nonce(3369213215035299664512484585000639319797562869764196177932)
	remote_pub = b"6c7266f30190cb955da4bb4e665cdf66b741ac5e68f6a7f580a94c879a21d62f"
	sent = b"007c26041c0df7cfe10010d0784ee426c0e8fad73c8241d29fa15c8782df66f972f33e48cb7909aeef66b57be8a7f2d31cd9742bbc4c68850b6c939989683a2e927b0b017ebda76400fb883fabdc064b286c980c0000002254455a4f535f424554414e45545f323031382d30362d33305431363a30373a33325a00000000"
	recv = b"007c4d146c7266f30190cb955da4bb4e665cdf66b741ac5e68f6a7f580a94c879a21d62f73db0e9d1a25784c1ebd94e806cdc99ed12675ea46834e42159c0e9be276e6411858e87ce7b78e307ed7f0cd881d312a0000002254455a4f535f424554414e45545f323031382d30362d33305431363a30373a33325a00000000"
	#print (ConnectionMessage.parse(binascii.unhexlify(recv)).pubkey)

	nonces = Nonce.generate(binascii.unhexlify(sent), binascii.unhexlify(recv), False)
	keybox = KeyBox(nonces['remote'], remote_pub, nonces['local'], identity.seckey)
	#keybox = KeyBox(nonces['remote'], identity.seckey, nonces['local'], remote_pub)

	sent2 = b"0000"
	#print(binascii.hexlify(keybox.encrypt(binascii.unhexlify(sent2))))
	sent2_enc = b"96c7a8f46a9945626babe703b12d239f3eec"
	recv2_enc = b"f599e74759650965d948d4851e2d39d0eeec"
	recv2 = keybox.native_box().decrypt(binascii.unhexlify(recv2_enc), nonces['remote'].get())
	print (recv2)
	"""