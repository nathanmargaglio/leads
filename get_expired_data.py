#!/usr/bin/python

import time
import datetime
from dataret.crawler import crawler
from dataret.parser import parser
from dataret.database_parser import database_parser

todays_date = datetime.datetime.now().date()
name = "{}_{}_{}".format(todays_date.month,todays_date.day,todays_date.year)
print "Crawling started:"
#crawler(name)
print "Parsing Started:"
#parser(name)
print "Adding to Database:"
database_parser(name)
print "Done!"
