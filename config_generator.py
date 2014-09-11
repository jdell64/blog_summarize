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
config.set('main', 'key', 'type mail chimp key here')
# config.set('main', 'template_id', 'type an int for the template id')
config.set('main', 'campaign_id', 'campaign_id_here')
config.set('main', 'blogs', 'list,blogs,seperated,by,comma')
# config.set('Section1', 'a_float', '3.1415')
# config.set('Section1', 'baz', 'fun')
# config.set('Section1', 'bar', 'Python')
# config.set('Section1', 'foo', '%(bar)s is %(baz)s!')

config.add_section('email')
config.set('email', 'list_id', 'id for the list you are sending it to')
config.set('email', 'subject', 'the subject of the email')
config.set('email', 'from_email', 'who the email will appear to be from, eg Blogs@company.com')
config.set('email', 'from_name', 'who the email will appear to be from, eg Company, INC')
config.set('email', 'to_name', 'the name you are sending it to')

# this is interval between emails in seconds
# 60 sec * 60 min * 24 hr = 86400 seconds in a day
# 86400 seconds * 7 days = 604800 seconds in a week
config.set('email', 'wait_interval', 'seconds to wait inbetween emails')


# Writing our configuration file to 'example.cfg'
with open('myconfig.cfg', 'wb') as configfile:
    config.write(configfile)