import urllib2
import mailchimp
import os
import ConfigParser
from bs4 import BeautifulSoup
from unidecode import unidecode


# constants

config = ConfigParser.RawConfigParser()


#put in the loop

config.read('myconfig.cfg')
TEMPLATE_ID = config.getint('main', 'template_id')
CAMPAIGN_ID = config.get('main','campaign_id')
MAILCHIMP_API = config.get('main', 'key')



# get blogs

BLOG_LIST = config.get('main', 'blogs')

BLOG_LIST = BLOG_LIST.split(",")

blog_summaries = ["<div class='summaries'>"]
for blog in BLOG_LIST:
    # print blog
    html =  urllib2.urlopen(blog).read()
    urllib2.urlopen(blog).close()

    soup = BeautifulSoup(html)

    # print soup.h1['entry-title']
    # print soup.h2['entry-title']
    titles = soup.findAll("h2", { "class" : "entry-title" })
    if len(titles) < 1:
        titles = soup.findAll("h1", { "class" : "entry-title" })

    most_recent_title = titles[0].string

    contents = soup.findAll("div", { "class" : "entry-content" })
    most_recent_content = contents[0].text
    paragraphs = most_recent_content.split("\n")
    paragraphs = filter(None, paragraphs) # drop empties

    desired_text='<p>'+paragraphs[0]
    index = 1
    while len(desired_text.split(" ")) < 30: # if the desired text has less than 30 words
        desired_text += '</p><p>' + paragraphs[index] # add the next paragraph
        index += 1


    blog_summary = '<div class="summary"><h2 class="title"><a href="'+ blog +'">'+most_recent_title+'</a></h1><div ' \
                                                                               'class="content">'+desired_text+'</p></div></div>'
    blog_summaries.append(blog_summary)

blog_summaries.append('</div>')
blog_summaries = "".join(blog_summaries)


# for stupid blogs with stupid non-ASCII characters:

blog_summaries = unidecode(blog_summaries)









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
with open('tail', 'r') as f:
    tail = f.read()


html = head+blog_summaries+tail


# print data
# source = source.replace('REPLACE_TITLE', 'the real title')
# source = source.replace('REPLACE_CONTENT', 'the real content')

new_value = {'html': html}

# m.templates.update(TEMPLATE_ID, values=new_value)

# create a new campaign

# put these in the config file:
campaign_values = {'list_id':'6ff9a39094','subject':'CT BLOGS', 'from_email':'jeff.tindell@gmail.com','from_name':'jeff',
                   'to_name':'Subscriber'}

# print m.lists.list()

camp = m.campaigns.create("regular", options=campaign_values, content=new_value)
# camp['id']

# SEND EMAIL
m.campaigns.send(camp['id'])


