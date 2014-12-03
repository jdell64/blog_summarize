blog_summarize

This is a powershell script that summarizes wordpress blogs and writes them to an html file locally. 

To specify the blogs, change the first variable in the code:

    $urls = "http://...",
      "http://...",
      "http://..."

These need to be installed:

- import mailchimp
- from bs4 import BeautifulSoup
- from unidecode import unidecode

todo:
- install script
- send two weeks from last time sent (make this configurable)
- ignore last sent time with switch
- as service and run on startup (done, add to repo)
- adjust admin email... should have a message in the error message (replaced with text file attachment for now)
- log rotation
- switch for test list