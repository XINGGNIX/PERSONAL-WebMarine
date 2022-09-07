from webmarine import webmarine as marine 
from preprocessing import preprocessing as prepr 
from data_warehouse import data_warehouse as warehouse 
import re
import pandas as pd 
import os


class collecter:
    password = None
    brand_list = None

    def __init__(self, password):
        self.password = password
        ware_houser = warehouse.warehouser(self.password)
        try:
            self.brand_list = ware_houser.get_brand_model()
        except:
            pass

    def setup(self):
        web_marine = marine.webmarine()
        web_marine.run_webmarine()
        pre_processer = prepr.preprocesser()
        pre_processer.run_preprocesser()
        ware_houser = warehouse.warehouser(self.password)
        ware_houser.run_warehouser()
        self.brand_list = ware_houser.get_brand_model()

    def update_by_brand(self):
        print("collecter(): update by brands ... ")
        try:
            self.brand_list = ware_houser.get_brand_model()
        except:
            pass
        web_marine = marine.webmarine()
        tmp_features = {'brand': None}
        brands = ['renault', 'rolls-royce', 'skoda', 'ssangyong', 'subaru', 'suzuki', 'tesla', 'toyota', 'volkswagen', 'volvo', 'alfa-romeo']

        for brand in brands:
            print("collecter(): current brand = {} ...".format(brand))
            tmp_features['brand'] = brand
            web_marine.set_features(tmp_features)
            web_marine.run_webmarine()

            pre_processer = prepr.preprocesser()
            pre_processer.run_preprocesser()

            houser = warehouse.warehouser(self.password)
            houser.run_warehouser() 

        web_marine.end_webmarine()




