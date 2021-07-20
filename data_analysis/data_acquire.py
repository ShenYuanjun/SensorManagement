from pymongo import MongoClient
import time
import pickle

mark = 'env_test_0704'  # 要读取的collection名称，pkl文件也以此命名

client = MongoClient('mongodb://10.181.6.96/',
                     username='sensorTester',
                     password='test123456',
                     authSource='admin')
db = client['sensor_management']
collection = db[mark]

t = time.time()

data_all = []
for c in collection.find():  # query在这里设置
    data_all.append(c)

with open(mark + '.pkl', 'wb') as f:
    pickle.dump(data_all, f)

print('Time Consuming:', time.time() - t)
