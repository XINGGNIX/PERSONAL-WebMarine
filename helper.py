# pip module
import os 
import time
import pymysql
import json 


def check_password(password):
	with open('./data_warehouse/db_config.json', 'r') as conf:
	    config = json.loads(conf.read())
	try:
	    host = config['db_conf']['host']
	    user = config['db_conf']['user']
	    connection = pymysql.connect(host = host, user = user, password = password, autocommit = True)
	    return True
	except:
	    return False