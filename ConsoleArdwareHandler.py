import Configuration as config
from ArdwareHandler import *

class ConsoleArdwareHandler(ArdwareHandler):
	def process(self,data):
		print "[x] :%s" % data

