import sys
sys.path.append("/home/pi/llpi/pylib")

import socket 
import llnet as net
 
tw = net.Twitter('twitter_app1')
time_ntp = net.get_time_ntp()
hostname = socket.gethostname()

msg = "[%s] %s: active at %s" % (time_ntp, hostname, net.get_ip_address())

tw.update_status(msg)
