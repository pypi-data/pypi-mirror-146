"""ManoPot.
Simple TCP HoneyPot logger

Usage:
  manopot <config_filepath>

Options:
  <config_filepath>      Path to config options .ini file
  -h --help              Show this screen.
"""
import configparser
import sys
from manopot import HoneyPot

# Check arguments
if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
  print(__doc__)
  sys.exit(1)


# Load config
# config_filepath = 'manopot.ini'
config_filepath = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_filepath)

ports = config.get('default', 'ports', raw=True, fallback="8080,8888,9999,3306")
host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
log_filepath = config.get('default', 'logfile', raw=True, fallback="/var/log/manopot.log")


# Double check ports provided
ports_list = []
try:
    ports_list = ports.split(',')
except Exception as e:
    print('[-] Error parsing ports: %s.\nExiting.', ports)
    sys.exit(1)

# Launch honeypot
honeypot = HoneyPot(host, ports_list, log_filepath)
honeypot.run()
