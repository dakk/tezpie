from colorlog import ColoredFormatter
import logging
import sys
import os

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




def app_data_path (appname, roaming=True):
	if sys.platform.startswith('java'):
		os_name = platform.java_ver()[3][0]
		if os_name.startswith('Windows'):
			system = 'win32'
		elif os_name.startswith('Mac'):
			system = 'darwin'
		else:
			system = 'linux2'
	else:
		system = sys.platform

	if system == "win32":
		const = roaming and "CSIDL_APPDATA" or "CSIDL_LOCAL_APPDATA"
		path = os.path.normpath(_get_win_folder(const))
		if appname:
			path = os.path.join(path, appname)
	elif system == 'darwin':
		path = os.path.expanduser('~/Library/Application Support/')
		if appname:
			path = os.path.join(path, appname)
	else:
		path = os.getenv('XDG_DATA_HOME', os.path.expanduser("~/"))
		if appname:
			path = os.path.join(path, '.'+appname)
	return path


NAME = "tezpie"
VERSION = 0.1

class Config:
	_instance = None

	config = {
		'chain_id': b'NetXdQprcVkpaWU',
		'version': VERSION,
		'data_dir': app_data_path(NAME),
		'p2p_lookup_nodes': ["boot.tzalpha.net", "bootalpha.tzbeta.net"],
		'p2p_default_port': 9732,
		'p2p_max_peers': 8,
		'p2p_min_peers': 1,
		'verbose': 5,
		'daemon': False,
	}

	def get_obj():
		if Config._instance == None:
			Config._instance = Config()
		return Config._instance

	def get(key):
		o = Config.get_obj()
		return o.config[key]

	def set(key, value):
		o = Config.get_obj()
		o.config[key] = value