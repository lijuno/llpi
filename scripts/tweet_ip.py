"""
Push basic system info (hostname, IP address, etc.) to Twitter
"""

# First find the correct library path
import sys
import ConfigParser
import getpass
username_os = getpass.getuser()
config = ConfigParser.ConfigParser()
config.read('/home/%s/.llpi.cfg' % username_os)
llpi_path = config.get('general', 'LLPI_ROOT_PATH')

sys.path.append('%s/pylib' % llpi_path)

import socket 
import llnet as net

# Now do twitter stuff
twitter_app = config.get('tweet_ip', 'TWITTER_APP')
network_interface = config.get('tweet_ip', 'NETWORK_INTERFACE')
tw = net.Twitter(twitter_app)
time_ntp = net.get_time_ntp()
hostname = socket.gethostname()

msg = "[%s] %s: active at %s" % (time_ntp, hostname, net.get_ip_address(network_interface))

tw.update_status(msg)
