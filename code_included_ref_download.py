from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from lxml import html
from HTMLParser import HTMLParser
import itertools
import time
import requests
import sys

def iso(text):
  print "\nxx\n"
  print text
  print "\nxx\n"

reload(sys)
sys.setdefaultencoding('utf8')

link_ids = open('wiley_ids.txt').read().splitlines()
out_file = open('refs.xml','w')

for i in range(0,237):

  link = 'http://onlinelibrary.wiley.com/doi/10.1002/14651858.'+link_ids[i]+'/references'
  page = requests.get(link)
  tree = html.fromstring(page.text)
  
  bibsections = tree.xpath("//*[@class='bibSection']/*[@class='bibSection']")

  print "number--",i
  print link_ids[i]
  print len(bibsections)

  for each in bibsections:
     out_file.write(html.tostring(each, pretty_print=True)+"\n")

  time.sleep(1)


