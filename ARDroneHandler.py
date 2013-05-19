import Configuration as config
from ArdwareHandler import *
from math import ceil
import time
import libardrone


class ARDrone:

	def __init__(self):
		self.speed = 0
		self.drone = libardrone.ARDrone()

	def set_speed(self):
		self.drone.speed = self.speed

	def turn_left(self):
		self.set_speed()
		self.drone.turn_left()
		print "TURN_LEFT:%f" % self.speed

	def turn_right(self):
		print "TURN_RIGHT:%f" % self.speed
		self.set_speed()
		self.drone.turn_right()

	def move_up(self):
		print "UP:%f" % self.speed
		self.set_speed()
		self.drone.move_up()

	def move_down(self):
		print "DOWN:%f" % self.speed
		self.set_speed()
		self.drone.move_down()

	def move_forward(self):
		print "FORWARD:%f" % self.speed
		self.set_speed()
		self.drone.move_forward()

	def move_backward(self):
		print "BACKWARD:%f" % self.speed
		self.set_speed()
		self.drone.move_backward()

	def move_right(self):
		print "RIGHT:%f" % self.speed
		self.set_speed()
		self.drone.move_right()

	def move_left(self):
		print "LEFT:%f" % self.speed
		self.set_speed()
		self.drone.move_left()

	def hover(self):
		print "HOVERING:%f" % self.speed
		self.set_speed()
		self.drone.hover()

	def land(self):
		print "LANDING"
		self.set_speed()
		self.drone.land()

	def takeoff(self):
		print "TAKEOFF"
		self.set_speed()
		self.drone.takeoff()

	def reset(self):
		print "RESET"
		self.set_speed()
		self.drone.reset()

class ARDroneHandler(ArdwareHandler):

	def __init__(self):
		self.drone = ARDrone()
		self.values = None
		self.scaled_vals = None
		self.default_vals = None
		self.probe_time = time.time()+5
		self.FUN_STICK_L ={
			config.LEFT: lambda:self.drone.turn_left(),
			config.RIGHT: lambda:self.drone.turn_right(),
			config.UP: lambda: self.drone.move_up(),
			config.DOWN: lambda: self.drone.move_down()
		}

		self.FUN_STICK_R = {
			config.LEFT: lambda: self.drone.move_left(),
			config.RIGHT: lambda: self.drone.move_right(),
			config.UP: lambda: self.drone.move_forward(),
			config.DOWN: lambda: self.drone.move_backward()
		}
		self.hover_flag = False
		self.isFlying = False
		self.btnPreviousState = False

	def process(self,data):
		self.values = data
		
		if self.default_vals == None or time.time()<self.probe_time:
			self.default_vals =self.values
			print "Calibrating Current:%s, Future:%s" %(time.time(),self.probe_time) 
			return

		if config.BTN in self.values:
			flag= False
			btnState = True if self.values[config.BTN] == 1 else False
			if btnState != self.btnPreviousState and btnState:
				if self.isFlying:
					self.drone.land()
					self.isFlying = False
				else:
					self.drone.takeoff()
					self.isFlying = True
				flag=True
			self.btnPreviousState = btnState
			if flag:
				return

		diff = set(self.values.items()) - set(self.default_vals.items())
		if len(diff) <=0 and self.hover_flag:
			self.drone.speed=0
			self.drone.hover()
			print "Battery:%d" % (100)
			self.hover_flag = False

		#print self.values
		#print self.default_vals
		#print self.scaled_vals
		events = self.get_events()

		for event in events:
			self.hover_flag = True
			self.drone.speed = event[2]
			if event[0] == config.STICK_L:
				self.FUN_STICK_L[event[1]]()

			elif event[0] == config.STICK_R:
				self.FUN_STICK_R[event[1]]()

		
	def land(self):
		self.drone.land()

	def takeoff(self):
		self.drone.takeoff()

	def emergency(self):
		self.drone.reset()

	def battery_status(self):
		self.drone.navdata.get(0, dict()).get('battery', 0)
		

	def get_events(self):
		'''Each event is [stick,direction,speed]'''
		events = []
		for key,val in self.values.iteritems():
			if self.has_value_changed(key,val):
				default = self.default_vals[key]

				if key == config.LEFT_LR:
					event = [config.STICK_L]
					direction = config.LEFT if val < default else config.RIGHT
					speed = self.scale_value(default-val,default) if direction is config.LEFT else self.scale_value(val - default,config.MAX_RAW_VAL-default)
					event.append(direction)
					event.append(speed)

					events.append(event)

				elif key == config.LEFT_UD:
					
					event = [config.STICK_L]
					direction = config.DOWN if val < default else config.UP
					speed = self.scale_value(default-val,default) if direction is config.DOWN else self.scale_value(val - default,config.MAX_RAW_VAL-default)
					event.append(direction)
					event.append(speed)

					events.append(event)

				elif key == config.RIGHT_LR:
					event = [config.STICK_R]
					direction = config.LEFT if val < default else config.RIGHT
					speed = self.scale_value(default-val,default) if direction is config.LEFT else self.scale_value(val - default,config.MAX_RAW_VAL-default)
					event.append(direction)
					event.append(speed)

					events.append(event)

				elif key == config.RIGHT_UD:
					event = [config.STICK_R]
					direction = config.DOWN if val < default else config.UP
					speed = self.scale_value(default-val,default) if direction is config.DOWN else self.scale_value(val - default,config.MAX_RAW_VAL-default)
					event.append(direction)
					event.append(speed)

					events.append(event)

		return events


	def has_value_changed(self,key,val):
		return (val<self.default_vals[key]-config.MIN_THRESHOLD or val >self.default_vals[key]+config.MIN_THRESHOLD)

	def scale_value(self,val,max):
		if val == None:
			return None

		v = float(max)
		
		return self.round_to_decimal_places(val/v)

	def scale_values(self):
		if self.values == None:
			return None

		self.scaled_vals = self.values
		v = float(config.MAX_RAW_VAL)
		for key,val in self.values.iteritems():
			self.scaled_vals[key] = self.round_to_decimal_places(val/v)

	def round_to_decimal_places(self,val):
		num = ceil(val * 10) / 10.0
		return num