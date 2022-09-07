import datetime
import time 
import getpass
from helper import check_password
import collector 

def get_current_time():
	now = datetime.datetime.now()
	now_date_time = now.strftime("%Y-%m-%d_%H:%M:%S")
	return str(now_date_time)

class controller:
	collecter = None
	extractor = None
	password = None

	def __init__(self):
		# tolerence for 5 times password trying 
	    for tolerance in range(0, 5):
	        print("controller({}): ENTER PASSWORD ...".format(get_current_time()))
	        password = getpass.getpass()
	        unlock = check_password(password)

	        # Stop early if password is correct
	        if (unlock == False):
	        	print("controller({}): PASSWORD INCORRECT ... \n".format(get_current_time()))
	        else:
	        	print("controller({}): SUCCESS ... \n".format(get_current_time()))
	        	self.password = password
	        	self.collecter = collector.collecter(self.password)
	        	break

	def run_app(self):
		if self.password == None:
			exit(0)
		while (True):
			cmd = input("controller({}): ENTER SCRIPT COMMAND ... \n".format(get_current_time()))
			cmd = cmd.lower()

			if (cmd == 'quit' or cmd == 'q'):
				break

			elif (cmd == 'export_all' or cmd == 'e'):
				extract = extractor.extractor(self.password)
				extract.get_all()

			elif (cmd == 'setup' or cmd == 's'):
				self.collecter.setup()

			elif (cmd == 'update' or cmd == 'u'):
				self.collecter.update_by_brand()

			elif (cmd == 'auto' or cmd == 'a'):
				self.collecter.setup()
				self.collecter.update_by_brand()

					
cont = controller()
cont.run_app()




















