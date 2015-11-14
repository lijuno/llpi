import time
from twython import Twython, TwythonError
import netifaces
import ConfigParser
import ntplib
import getpass


# Global config file object for all llpi_pylib stuff
username_os = getpass.getuser()
config = ConfigParser.ConfigParser()
#config.read('/home/%s/.llpi_pylib.cfg' % username_os)

# username_os is dependent on the environment, which may not be interpretted correctly in cron job
# Use absolute path to avoid such a conflict
config.read('/home/pi/.llpi_pylib.cfg')  


def get_ip_address(interface='wlan0'):
    # Return a string which may be masked 
    ip_str = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    ip_digits = ip_str.split('.')
    ip_digits = [int(i) for i in ip_digits]  # convert to four 8-bit int

    if not (ip_digits[0]== 10 or (ip_digits[0]==172 and ip_digits[1]>=16 and ip_digits[1]<=31) or (ip_digits[0]==192 and ip_digits[1]==168)):
        # if not private IP address, mask first two ints
        ip_str = "*.*.%s.%s"  %  (ip_digits[2], ip_digits[3])

    return ip_str


def get_time_ntp():
    # Get time from ntp and return a string
    # https://pypi.python.org/pypi/ntplib/
    try: 
        c = ntplib.NTPClient()
        res = c.request('pool.ntp.org')
        return time.ctime(res.tx_time)
    except Exception as e:
        raise e


class Twitter:

    def __init__(self, profile="twitter_app1"):
        # Get Twitter application authentication info first
        # Input "profile" is the section in config file
        self.APP_KEY = config.get(profile, 'APP_KEY')
        self.APP_SECRET = config.get(profile, 'APP_SECRET')
        self.OAUTH_TOKEN = config.get(profile, 'OAUTH_TOKEN')
        self.OAUTH_TOKEN_SECRET = config.get(profile, 'OAUTH_TOKEN_SECRET')
  
    def update_status(self, msg='Hallo!'):
        twitter = Twython(self.APP_KEY, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

        try:
            twitter.update_status(status=msg)
            print "Status update success: %s" % msg
        except TwythonError as e:
            raise e



