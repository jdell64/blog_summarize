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
- last time sent (in case server bounces)
- send two weeks from last time sent
- as service and run on startup