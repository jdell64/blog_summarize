__author__ = 'Jeff Tindell'

import ConfigParser

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('main')
config.set('main', 'key', '')
config.set('main', 'blogs', 'http://domain.com,http://domain2.com')

config.add_section('error_email')
config.set('error_email', 'service_email', 'blogs@...')
config.set('error_email', 'service_pass', '')
config.set('error_email', 'admin_email', '')


config.add_section('mail_chimp')
config.set('mail_chimp', 'list_id', '')
config.set('mail_chimp', 'subject', '')
config.set('mail_chimp', 'from_email', '')
config.set('mail_chimp', 'from_name', '')
config.set('mail_chimp', 'to_name', '')

# this is interval between emails in seconds
# 60 sec * 60 min * 24 hr = 86400 seconds in a day
# 86400 seconds * 7 days = 604800 seconds in a week
config.set('mail_chimp', 'wait_interval', 1209600)


# Writing our configuration file to 'example.cfg'
with open('myconfig.cfg', 'wb') as configfile:
    config.write(configfile)