from datetime import datetime
import pandas as pd 
import time
from pathlib import Path
import re 



class preprocesser:
    # ===================================
    # Default parameters
    # ===================================
    csv_path = "./webmarine/buffer_result.csv"
    data_buffer = None

    def __init__(self):
        # load data
        self.data = pd.read_csv(self.csv_path, index_col = [0])
    
    def load_data_to_buffer(self):
        self.data_buffer = pd.read_csv(self.csv_path, index_col = [0])

    def inspect_data_buffer(self):
        print(self.data_buffer.head(5))


    # ==============
    # data cleaning 
    #===============
    # preprocess raw title 
    def preprocess_title(self, title):
        # break |title| into brand, model, year, description
        try:
            title_breakdown = title.lower().split(' ')
            year = title_breakdown[0]
            max_index = 0
            if (title_breakdown[1] == 'land'):
                if (title_breakdown[3] == 'range'):
                    brand = title_breakdown[1] + ' ' + title_breakdown[2]
                    model = title_breakdown[3] + ' ' + title_breakdown[4]
                    max_index = 5
                else:
                    brand = title_breakdown[1] + ' ' + title_breakdown[2]
                    model = title_breakdown[3]
                    max_index = 4

            elif (title_breakdown[1] == 'aston'):
                brand = title_breakdown[1] + ' ' + title_breakdown[2]
                model = title_breakdown[3]
                max_index = 4
  
            elif (title_breakdown[1] == 'alfa'):
                brand = title_breakdown[1] + ' ' + title_breakdown[2]
                model = title_breakdown[3]
                max_index = 4
            elif(re.match("^[0-9]*$", title_breakdown[2])):
                brand = title_breakdown[1]
                model = title_breakdown[2] + ' ' + title_breakdown[3]
                max_index = 4
            else:
                brand = title_breakdown[1]
                model = title_breakdown[2]
                max_index = 3

            description = ' '.join(title_breakdown[max_index:len(title_breakdown)])
            return year, brand, model, description
        except:
            return False, False, False, False

    # preprocess raw price 
    def preprocess_price(self, price):
        try: 
            return int(price)
        except: 
            try:
                price = re.sub('[^0-9]','', price)
                return int(price)
            except:
                return False

        return False 

    # preprocess raw odometers  
    def preprocess_odometer(self, km):
        try:
            km = re.sub('[^0-9]','', km)
            return int(km)
        except:
            return None

    def preprocess_bodytype_and_engine(self, bodytype, matic, petrol):
        bodytype = bodytype.lower()
        matic = matic.lower()
        petrol = petrol.lower()

        if bodytype == 'automatic' or bodytype == 'manual':
            bodytype = None

        if matic not in ['automatic', 'manual', 'amt']:
            matic = 'automatic'

        paramters_list = petrol.split()
        cyl = 0
        vol = 0
        turbo = False
        fuel = None
        hybrid = False
        electric = False
        for parameter in paramters_list:
            if (re.match("[0-9]*cyl", parameter)):
                cyl = int(re.sub("[^0-9]", '', parameter))
            elif(re.match("[0-9].[0-9]*l", parameter)):
                vol = re.match("([0-9].[0-9]*)l", parameter)
                vol = float(vol.group(1))
            elif(parameter == 'turbo'):
                turbo = True
            elif(parameter in ['petrol', 'diesel']):
                fuel = parameter
            elif(parameter == 'hybrid'):
                cyl = None
                vol = None
                hybrid = True
            elif(parameter == 'electric'):
                cyl = None
                vol = None
                electric = True

        return bodytype, cyl, vol, turbo, fuel, hybrid, electric


    def preprocess_url(self, url):
        try:
            car_id = re.match('/cars/details/.*/([A-Z0-9-]*)/.*', url)
            car_id = car_id.group(1)
            return url, car_id
        except:
            return False, False

    def preprocess_data_buffer(self):
        columns = [ 'id', 'year', 'brand', 'model', 
                    'description', 'price', 'odometer', 'bodytype',
                    'cylinder', 'volume', 'turbo', 
                    'fueltype', 'hybrid', 'electric', 'state', 'url']
        processed_list = []

        for index, row in self.data_buffer.iterrows():
            title = row[0]
            url = row[1]
            price = row[2]
            odometer = row[3]
            bodytype = row[4]
            matic = row[5]
            petrol = row[6]
            state = row[7]

            cleaned_row = []

            # break |title| into brand, model, year, description 
            year, brand, model, description = self.preprocess_title(title)
            price = self.preprocess_price(price)
            odometer = self.preprocess_odometer(odometer)
            bodytype, cyl, vol, turbo, fuel, hybrid, electric = self.preprocess_bodytype_and_engine(bodytype, matic, petrol)
            url, car_id = self.preprocess_url(url)

            # load into buffer
            processed_record = [car_id, year, brand, model, description, price, odometer, bodytype, cyl, vol, turbo, fuel, hybrid, electric, state, url]
            processed_list.append(processed_record)

            # save in pandas dataframe 
            buffer_df = pd.DataFrame(processed_list, columns = columns)
            buffer_df.to_csv('./preprocessing/processed_result.csv')

        buffer_df = pd.DataFrame(processed_list, columns = columns)
        buffer_df.to_csv('./preprocessing/processed_result.csv')

    def run_preprocesser(self, show_header = False):
        if self.data_buffer == None:
            self.load_data_to_buffer()

        if (show_header):
            self.inspect_data_buffer()

        self.preprocess_data_buffer()





            




