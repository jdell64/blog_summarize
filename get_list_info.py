import mailchimp

__author__ = 'jeff'
def get_mailchimp_api():
    return mailchimp.Mailchimp('')  #your api key here

m = get_mailchimp_api()

print m.lists.list()['data'][0]['id']
