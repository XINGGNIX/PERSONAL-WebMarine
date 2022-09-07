import pandas as pd
import sqlalchemy
import pymysql
import json 

class warehouser:
    connection = None
    cursor = None
    buffer = None
    db_config = None
    password = None

    def __init__(self, password):
        # load configuration
        with open('./data_warehouse/db_config.json', 'r') as conf:
            self.db_config = json.loads(conf.read())
        
        # load data
        self.password = password

    def create_connection(self):
        try:
        # parameters 
            host = self.db_config['db_conf']['host']
            user = self.db_config['db_conf']['user']
            password = self.password

            # attempt establishing connection
            self.connection = pymysql.connect(host = host, user = user, password = password, autocommit = True)
            self.cursor = self.connection.cursor()
        except:
            print("warehouser(): Fail connect with MySQL ...")

    def drop_database(self):
        self.execute_query(self.db_config['sql_cmd']['drop_db'])

    def setup_database(self):
        with open(self.db_config['sql_file']['setup_db'], 'r') as f:
            self.execute_query(f.read())

    def execute_query(self, query):
        try:
            cursor = self.cursor
            query_list = query.replace('\n', ' ').replace('\t', ' ').split(';')
            for query_item in query_list:
                if (len(query_item) > 1):
                    cursor.execute(query_item + ";")
            self.cursor = cursor
        except Exception as err:
            print(err)
            pass 

    def switch_database(self):
        self.execute_query('USE car_sales;')

    def fill_brand_model(self, engine):
        data = self.buffer[['brand', 'model']].drop_duplicates()
        self.switch_database()
        for index, row in data.iterrows():
            try:
                values = "'{}', '{}'".format(row[0], row[1])
                script = self.db_config['sql_cmd']['insert_brand_model'].format(values = values)
                self.execute_query(script)
            except:
                pass

    def brand_model_to_id(self):
        self.execute_query(self.db_config['sql_cmd']['select_brand_model'])
        model_brand_dict = {}
        for model_brand in self.cursor.fetchall():
            model_brand_dict[model_brand[1] + ' ' + model_brand[2]] = model_brand[0]

        return model_brand_dict
        
    def data_pipeline(self):
        # get credentials  
        password = self.password
        user = self.db_config['db_conf']['user']
        host = self.db_config['db_conf']['host']
        port = self.db_config['db_conf']['port']
        engine_script = self.db_config['db_conf']['engine'].format(user = user, password = password, host = host, port = port)
        engine = sqlalchemy.create_engine(engine_script, echo = False)

        self.fill_brand_model(engine)
        brand_model_dict = self.brand_model_to_id()

        print(self.buffer)

        self.buffer['brand_model_id'] = self.buffer['brand'] + ' ' + self.buffer['model']
        self.buffer['brand_model_id'] = self.buffer['brand_model_id'].map(brand_model_dict)
        data = self.buffer.drop(columns = ['model', 'brand'])

        # CSV to SQL
        data_amount = len(self.buffer)
        bookmark = 0

        checkpoints = list(range(0, data_amount, 100)) + [len(self.buffer)]

        for i in range(1, len(checkpoints)):
            if (i >= len(checkpoints) - 1):
                break
            start = checkpoints[i]
            finished = checkpoints[i + 1]
            batch = data[checkpoints[i]:checkpoints[i + 1]]
            try:
                batch.to_sql(name = 'car', con = engine, if_exists = 'append', index = False)
            except:
                for idx, row in batch.iterrows():
                    try:
                        temp = pd.DataFrame(row).T
                        temp.to_sql(name = 'car', con = engine, if_exists = 'append', index = False)
                    except:
                        pass

    def close_connection(self):
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None

    def run_warehouser(self):
        self.buffer = pd.read_csv("./preprocessing/processed_result.csv", index_col = [0])
        print (self.buffer)
        self.create_connection()
        self.setup_database()
        self.data_pipeline()
        self.close_connection()


    def get_brand_model(self):
        self.create_connection()
        self.switch_database()
        self.execute_query(self.db_config['sql_cmd']['select_brand'])
        brand_model_buffer = []
        for model_brand in self.cursor.fetchall():
            brand_model_buffer.append(model_brand[0])

        self.close_connection()
        return brand_model_buffer

















