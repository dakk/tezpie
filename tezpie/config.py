from colorlog import ColoredFormatter
import logging

formatter = ColoredFormatter(
	'%(log_color)s[%(asctime)-8s] %(module)s: %(message_log_color)s%(message)s',
	datefmt=None,
	reset=True,
	log_colors = {
		'DEBUG': 'blue',
		'PLUGINFO': 'purple',
		'INFO':	'green',
		'WARNING': 'yellow',
		'ERROR': 'red',
		'CRITICAL': 'red',
	},
	secondary_log_colors={
		'message': {
			'DEBUG': 'purple',
			'PLUGINFO': 'blue',
			'INFO':	'yellow',
			'WARNING': 'green',
			'ERROR': 'yellow',
			'CRITICAL': 'red',
		}
	},
	style = '%'
)

stream = logging.StreamHandler ()
stream.setFormatter (formatter)

logger = logging.getLogger ('tezpie')
logger.addHandler (stream)
logger.setLevel (10)


P2P_BOOTSTRAP_NODES = ["boot.tzalpha.net", "bootalpha.tzbeta.net"]
P2P_DEFAULT_PORT = 9732
