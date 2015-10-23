README
======

Some random Python stuff for my Raspberry Pis. 

The configuration file for this library is stored somewhere else. An example of such a configuration file will be


```
[twitter_app1]
APP_KEY = xxx
APP_SECRET = xxx
OAUTH_TOKEN = xxx
OAUTH_TOKEN_SECRET = xxx
```


* Case 1: push IP address to Twitter

```Python
import sys
sys.path.append("/home/pi/app/llpi_pylib")

import llnet as net

tw = net.Twitter('twitter_app1')
time_ntp = net.get_time_ntp()

msg = "[%s] XXXpi: active at %s" % (time_ntp, net.get_ip_address())

tw.update_status(msg)
```
