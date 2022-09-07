import datetime
import time 
import getpass

class extractor:
    def __init__(self, password):
        self.password = password
        ware_houser = warehouse.warehouser(self.password)
        #self.brand_list = ware_houser.get_brand_model()
        #print(self.brand_list)
	
	def get_all()

	def get_current_time():
		now = datetime.datetime.now()
		now_date_time = now.strftime("%Y-%m-%d_%H:%M:%S")
		return str(now_date_time)

	def run_app(self):
		while (True):
			cmd = input("controller({}): ENTER SCRIPT COMMAND ... \n".format(get_current_time()))
			cmd = cmd.lower()

			if (cmd == 'quit' or cmd == 'q'):
				break 

			elif (cmd == 'setup' or cmd == 's'):
				self.collecter.setup()

			elif (cmd == 'update' or cmd == 'u'):
				self.collecter.update_by_brand()

			elif (cmd == 'auto' or cmd == 'a'):
				self.collecter.setup()
				self.collecter.update_by_brand()
					

				


cont = controller()
cont.run_app()




















