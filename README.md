README
======

Some useful random libraries and scripts used in my Raspberry Pi servers. 

## Config file

* This library use ConfigParser compatible format. 

* The config file is hard coded to be at '$HOME/.llpi.cfg', which is the only file needed to be customized to make this work. 
* The config file is read by 'pylib/llnet' and 'scripts/tweet\_ip'. 

* An example of config file

```
[general]
LLPI_ROOT_PATH = /home/pi/llpi


[twitter_app1]
APP_KEY = xxx
APP_SECRET = xxx
OAUTH_TOKEN = xxx
OAUTH_TOKEN_SECRET = xxx

[tweet_ip]
TWITTER_APP = twitter_app1
NETWORK_INTERFACE = wlan0

```


* This library depends on user environmental variables. When using the script with crontab, source the BASH profile first to set up the environmental variables correctly: 

```
0 5 * * * source $HOME/.profile; /path/to/command/to/run
```

## Use Cases

* Case 1: push IP address to Twitter

```
import sys
import socket
import llnet as net

tw = net.Twitter('twitter_app1')
time_ntp = net.get_time_ntp()
hostname = socket.gethostname()

msg = "[%s] %s: active at %s" % (time_ntp, hostname, net.get_ip_address("wlan0"))

tw.update_status(msg)
```


