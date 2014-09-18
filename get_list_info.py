__author__ = 'jeff'
import ConfigParser
import mailchimp


config = ConfigParser.RawConfigParser()

def get_mailchimp_api(key):
    return mailchimp.Mailchimp(key)  #your api key here


config.read('myconfig.cfg')
    # TEMPLATE_ID = config.getint('main', 'template_id')
    # CAMPAIGN_ID = config.get('main', 'campaign_id')
MAILCHIMP_API = config.get('main', 'key')

m = get_mailchimp_api(MAILCHIMP_API)

list_data = m.lists.list()['data']

for clist in list_data:
    print clist['name'], ":", clist['id']

    # m.lists.list()['data'][0]['id']
