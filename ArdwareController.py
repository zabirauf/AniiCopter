import serial
import Configuration as config
import re


class ArdwareController:
	def __init__(self):
		# Yes i know its very very bad to put hardcoded indexes, i know we all sworn not to do that :)
		self.keys = {config.LEFT_LR:0,config.LEFT_UD:2,config.RIGHT_LR:4,config.RIGHT_UD:3,config.BTN:1}
		self.patterns = [re.compile('(?<=%s)\d+'%x) for x,v in self.keys.iteritems()]
		self.values = {config.LEFT_LR:0,config.LEFT_UD:0,config.RIGHT_LR:0,config.RIGHT_UD:0,config.BTN:0}
		self.subscribers = []

	def subscribe(self,subscriber):
		self.subscribers.append(subscriber)

	def publish_to_all_subscribers(self):
		for subscriber in self.subscribers:
			subscriber.process(self.get_converted_values_according_to_position())

	def parse_line(self,line):
		key = line[0:3]
		try:
			match = self.patterns[self.keys[key]].search(line)
			val = match.group(0)
			return val
		except Exception as ex:
			pass

	def get_converted_values_according_to_position(self):
			
		if config.DEFAULT_POSITION == config.SOUTH:
			return {
				config.LEFT_LR :config.MAX_RAW_VAL-self.values[config.LEFT_LR],
				config.LEFT_UD :config.MAX_RAW_VAL-self.values[config.LEFT_UD],
				config.RIGHT_LR:config.MAX_RAW_VAL-self.values[config.RIGHT_LR],
				config.RIGHT_UD:config.MAX_RAW_VAL-self.values[config.RIGHT_UD],
				config.BTN:self.values[config.BTN]
				}
		elif config.DEFAULT_POSITION == config.EAST:
			return {
				config.LEFT_LR :config.MAX_RAW_VAL-self.values[config.LEFT_UD],
				config.LEFT_UD :self.values[config.LEFT_LR],
				config.RIGHT_LR:config.MAX_RAW_VAL-self.values[config.RIGHT_UD],
				config.RIGHT_UD:self.values[config.RIGHT_LR],
				config.BTN:self.values[config.BTN]
			}
		elif config.DEFAULT_POSITION == config.WEST:
			return {
				config.LEFT_LR :self.values[config.LEFT_UD],
				config.LEFT_UD :config.MAX_RAW_VAL-self.values[config.LEFT_LR],
				config.RIGHT_LR:self.values[config.RIGHT_UD],
				config.RIGHT_UD:config.MAX_RAW_VAL-self.values[config.RIGHT_LR],
				config.BTN:self.values[config.BTN]
			}

		return self.values

	def connect(self):
		self.ser = serial.Serial(config.SERIAL_CHANNEL,config.SERIAL_BAUD_RATE)
		print "Connected to Arduino"

	def close(self):
		self.ser.close()
		print "Disconnected from Arduino"

	def pingpin(self):
		line = self.ser.readline()
		val = self.parse_line(line)
		self.values[line[0:3]] = int(val)
		self.publish_to_all_subscribers()
		
		



