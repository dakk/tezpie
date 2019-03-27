import logging

from . import config
from .p2p import PeerPool

logger = logging.getLogger('tezpie')

def start():
	logger.info ('tezpie is starting')

	pp = PeerPool()
	pp.bootstrap()