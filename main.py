from ArdwareController import *
from ConsoleArdwareHandler import *
from ARDroneHandler import *



if __name__ == "__main__":

	console = ConsoleArdwareHandler()
	ardware = ArdwareController()
	ardrone = ARDroneHandler()

	#ardware.subscribe(console)
	ardware.subscribe(ardrone)
	
	ardware.connect()

	while True:
		try:
			ardware.pingpin()
		except KeyboardInterrupt:
			print "Closing"
			break
		except Exception as ex:
			print ex
			pass
	ardrone.land()
	ardware.close()