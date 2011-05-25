#! /usr/bin/python


import urllib
import urllib2
import sys
import getopt
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-h", "--host", dest="host", default="localhost", help="The host machine running the kannel server. Default is localhost")
parser.add_option("-s", "--port", dest="port", default="13013", help="The port used for sendsms. Default is 13013")
parser.add_option("-u", "--username", dest="username", help="The sendsms user")
parser.add_option("-p", "--password", dest="password", help="The sendsms password")
parser.add_option("-m", "--message", dest="text", help="The text message to be sent")
parser.add_option("-d", "--dest", dest="dest_phone", help="The phone number the sms will be sent to")

(options, args) = parser.parse_args()

params = urllib.urlencode ({'username':options.username, 'password':options.password,
                            'to':options.dest_phone, 'text': options.text})

try:
    resp = urllib.urlopen ("http://%s:%s/cgi-bin/sendsms?%s" % (options.host, options.port, params))
    print "SMS Sent"
except urllib2.URLError, err:
    print "SMS Failed: ", err
