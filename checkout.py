import schedule
import pymongo
import yaml
import datetime
import logging
import time

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
config = data['config']
client = pymongo.MongoClient(host='192.168.0.48', port=38213)
database = client['MOOP']
db = database['classroom']
logging.basicConfig(format=config['LOG_FORMAT'], level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def job():
    data_list = db.find()
    for data in data_list:
        if 0 < data['status'] < 3 and data['endTime'] <= datetime.datetime.utcnow():
            db.update_one({'_id': data['_id']}, {'$set': {'status': 3}})
            logging.info('correct classroomId: %s' % str(data['_id']))


schedule.every().day.at('00:00').do(job)

while True:
    schedule.run_pending()
    # 2小时一次
    time.sleep(7200)
