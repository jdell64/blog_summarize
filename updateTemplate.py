import mailchimp
import os
import ConfigParser

# constants
config = ConfigParser.RawConfigParser()
config.read('myconfig.cfg')
TEMPLATE_ID = config.getint('main', 'template_id')
MAILCHIMP_API = config.get('main', 'key')

CURR_DIR = os.path.dirname(os.path.realpath(__file__))



# will return the mailchimpAPI object   

def get_mailchimp_api():
    return mailchimp.Mailchimp(MAILCHIMP_API)  #your api key here


m = get_mailchimp_api()

template = m.templates.info(TEMPLATE_ID)
# print template, type(template)
source = template['source']
# print source

with open('head', 'r') as f:
    head = f.read()
with open('current-blog-summary.txt', 'r') as f:
    data = f.read()
with open('tail', 'r') as f:
    tail = f.read()


html = head+data+tail


# print data
# source = source.replace('REPLACE_TITLE', 'the real title')
# source = source.replace('REPLACE_CONTENT', 'the real content')

test = {'html': html}

m.templates.update(TEMPLATE_ID, values=test)
