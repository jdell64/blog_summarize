import smtplib
import urllib2
import mailchimp
import logging
import ConfigParser
from bs4 import BeautifulSoup
import time
import sys
from unidecode import unidecode

# load the configparser
config = ConfigParser.RawConfigParser()


# set up logging
# make log_level in config file, which means i have to set this in the loop
# logging.basicConfig(filename='blog_summary.log',level=logging.INFO)
logger = logging.getLogger('BSS')
hdlr = logging.FileHandler('blog_summary.log')
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)




def get_mailchimp_api():
    return mailchimp.Mailchimp(MAILCHIMP_API)  #your api key here




# get blogs
def get_blogs(blog_list):
    logger.info("Started summarizing blogs: "+blog_list)
    blog_list = blog_list.split(",")
    blog_summaries = ["<div class='summaries'>"]
    if len(blog_list) > 0:
        for blog in blog_list:
            logger.info("Getting blog: " + blog)
            try:
                html = urllib2.urlopen(blog).read()
                urllib2.urlopen(blog).close()
            except:
                logger.error("Error with reading the website:" + blog)

            soup = BeautifulSoup(html)
            titles = soup.findAll("h2", {"class": "entry-title"})
            if len(titles) < 1:
                titles = soup.findAll("h1", {"class": "entry-title"})
                if len(titles) < 1:
                    logger.error("Unable to find any titles on blog:" + blog)
                    break

            most_recent_title = titles[0].string
            contents = soup.findAll("div", {"class": "entry-content"})
            most_recent_content = contents[0].text
            paragraphs = most_recent_content.split("\n")
            paragraphs = filter(None, paragraphs)  # drop empties
            desired_text = '<p>' + paragraphs[0]
            index = 1
            while len(desired_text.split(" ")) < 30:  # if the desired text has less than 30 words
                desired_text += '</p><p>' + paragraphs[index]  # add the next paragraph
                logger.warn("Paragraph selection for "+blog+" was too short. Adding in next paragraph.")
                index += 1
            blog_summary = '<div class="summary"><h2 class="title"><a href="' + blog + '">' + most_recent_title + '</a></h1><div ' \
                                                                                                                  'class="content">' + desired_text + '</p></div></div>'
            blog_summaries.append(blog_summary)
        logger.info("Finished with blog: "+blog)
    else:
        logger.error("No blogs in the blog list. Check the config file.")
        return False
    blog_summaries.append('</div>')
    blog_summaries = "".join(blog_summaries)
    # for stupid blogs with stupid non-ASCII characters:
    blog_summaries = unidecode(blog_summaries)
    logger.info("Finished summarizing blogs.")
    return blog_summaries


# will return the mailchimpAPI object

def monkey_around(m, blog_summaries):
    logger.info("Starting to monkey around.")


    # template = m.templates.info(TEMPLATE_ID)
    # print template, type(template)
    # source = template['source']
    # print source

    with open('head', 'r') as f:
        head = f.read()
    with open('tail', 'r') as f:
        tail = f.read()

    html = head + blog_summaries + tail

    # print data
    # source = source.replace('REPLACE_TITLE', 'the real title')
    # source = source.replace('REPLACE_CONTENT', 'the real content')

    new_value = {'html': html}

    # m.templates.update(TEMPLATE_ID, values=new_value)

    # create a new campaign

    # put these in the config file:
    campaign_values = {'list_id': LIST_ID, 'subject': SUBJECT, 'from_email': FROM_EMAIL, 'from_name': FROM_NAME,
                       'to_name': TO_NAME}

    # print m.lists.list()
    camp = m.campaigns.create("regular", options=campaign_values, content=new_value)

    logger.info("Done monkeying around.")
    return camp['id']
    # camp['id']



# SEND EMAIL
def send_mail(m, cid):
    logger.info("Sending email.")
    m.campaigns.send(cid)
    logger.info("Email sent.")

# if something goes wrong, email the admin
def send_error_email(message):
    logger.error("sending an email to the admin with message: %s" % message)

    service_email = config.get('error_email', 'service_email')
    service_pass = config.get('error_email', 'service_pass')
    admin_email = config.get('error_email', 'admin_email')
    admin_email = admin_email.split(",")

    FROM = service_email
    TO = admin_email #must be a list
    SUBJECT = "Error with summarizing blog"
    TEXT = message

    # Prepare actual message
    headMess = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        #server = smtp.lib.SMTP_SSL("smtp.gmail.com", 465)

        server.ehlo()
        server.starttls()
        server.login(service_email, service_pass)
        server.sendmail(FROM, TO, headMess)
        #server.quit()
        server.close()
        logger.error('Successfully sent the email to: %s' %admin_email)
    except:
        logger.error('Unable to send the email to: %s' %admin_email)
        logger.error( str(sys.exc_info()))





#put in the loop
while (1):
# read the config file every time you run

    config.read('myconfig.cfg')
    # TEMPLATE_ID = config.getint('main', 'template_id')
    # CAMPAIGN_ID = config.get('main', 'campaign_id')
    MAILCHIMP_API = config.get('main', 'key')
    LIST_ID = config.get('mail_chimp', 'list_id')
    SUBJECT = config.get('mail_chimp', 'subject')
    FROM_EMAIL = config.get('mail_chimp', 'from_email')
    FROM_NAME = config.get('mail_chimp', 'from_name')
    TO_NAME = config.get('mail_chimp', 'to_name')
    BLOG_LIST = config.get('main', 'blogs')
    SECONDS_TO_SLEEP = config.getint('mail_chimp','wait_interval')
    m = get_mailchimp_api()
    blog_summaries=""
    cid=0

    try:
        blog_summaries = get_blogs(BLOG_LIST)
        cid = monkey_around(m, blog_summaries)
        send_mail(m, cid)
    except:
        logger.error("Unexpected error:" + str(sys.exc_info()))
        send_error_email(str(sys.exc_info()))
    #     SEND AN EMAIL HERE

    logger.info("Done. Sleeping for %s seconds" % SECONDS_TO_SLEEP)

    time.sleep(SECONDS_TO_SLEEP)


# todo: put logging level in config file and set the variable in the loop.
# todo: gui for editing the config file. separate application
# todo: subtract run time from interval?
# todo: update config_generator