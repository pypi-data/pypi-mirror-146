# -*- coding: utf-8 -*-
# author: Kyusong Lee

from pymongo import MongoClient
from soco_trainer_plugin.core.config import Config, EnvVars
import datetime

import logging
from bson import ObjectId
from datetime import datetime
import ssl


class SearchLog(object):
    @staticmethod
    def get_doc(task_id, index_id, query):
        doc = {"index_id": index_id,
               "task_id": task_id,
               'query': query,
               "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
               }
        return doc


class Database(object):
    logger = logging.getLogger(__name__)
    def __init__(self, mongo_url):
        if EnvVars.mongodb_ssl and EnvVars.mongodb_ssl.lower() == 'true':
            self.client = MongoClient(host=mongo_url,
                                      socketTimeoutMS=Config.db_timeout,
                                      connectTimeoutMS=Config.db_timeout,
                                      serverSelectionTimeoutMS=Config.db_timeout,
                                      ssl=True,
                                      ssl_cert_reqs=ssl.CERT_NONE,
                                      retryWrites=False)
        else:

            self.client = MongoClient(host=mongo_url,
                                      socketTimeoutMS=Config.db_timeout,
                                      connectTimeoutMS=Config.db_timeout,
                                      serverSelectionTimeoutMS=Config.db_timeout,
                                      retryWrites=False)

    def create_index(self):
        # check existing index
        col = self.client[Config.db_name][Config.op_collection]
        existed = False
        for index in col.list_indexes():
            name = index['name']
            expire = index.get('expireAfterSeconds', -1)
            mismatch_expire = expire < 0 or (expire > 0 and expire != EnvVars.op_ttl)
            if name == 'generation_time_1':
                if mismatch_expire:
                    col.drop_index(index['name'])
                    self.logger.info("Delete existing index {}".format(name))
                else:
                    existed = True
                    self.logger.info("Found valid existing index {}".format(name))

                break

        # create a new index with the
        if not existed:
            res = col.create_index('generation_time', expireAfterSeconds=EnvVars.op_ttl)
            self.logger.info(res)
            self.logger.info("Create TTL index with TTL={}".format(EnvVars.op_ttl))

    def _norm_query(self, query):
        for k, v in query.items():
            if k == '_id' and type(v) is not ObjectId and type(v) is str:
                try:
                    query[k] = ObjectId(v)
                except Exception as e:
                    self.logger.warn(e)
                    raise Exception("Value is not valid Object ID")
        return query


    def read_task_meta(self, task_id, key):
        collection = self.client[Config.db_name][Config.task_collection]
        doc = collection.find_one({'_id': ObjectId(task_id)}, {key: 1})
        if doc:
            return doc.get(key)

        return None

    def write_task_meta(self, task_id, key, value):
        collection = self.client[Config.db_name][Config.task_collection]
        res = collection.update_one({'_id': ObjectId(task_id)}, {"$set": {key: value}})
        return res

    def push_task_meta(self, task_id, key, value):
        collection = self.client[Config.db_name][Config.task_collection]
        res = collection.update_one({'_id': ObjectId(task_id)},
                                    {'$push': {key: value}})
        return res

    def create_op(self, task_id, name, **kwargs):
        collection = self.client[Config.db_name][Config.op_collection]
        doc = {'task_id': task_id, 'name': name}
        doc.update(kwargs)
        doc['generation_time'] = datetime.utcnow()
        res = collection.insert_one(doc)
        op_id = str(res.inserted_id)
        return op_id

    def write_op_meta(self, op_id, key, value):
        collection = self.client[Config.db_name][Config.op_collection]
        res = collection.update_one({'_id': ObjectId(op_id)}, {"$set": {key: value}})
        return res

    def write_op_metas(self, op_id, meta):
        collection = self.client[Config.db_name][Config.op_collection]
        res = collection.update_one({'_id': ObjectId(op_id)}, {'$set': meta})
        return res

    def read_op(self, op_id):
        return self.find_document(Config.db_name, Config.op_collection, '_id', op_id)

    def write_file_meta(self, doc_id, key, value):
        collection = self.client[Config.db_name][Config.file_collection]
        res = collection.update_one({'_id': ObjectId(doc_id)}, {"$set": {key: value}})
        return res

    def find_document(self, db_name, collection_name, key, value, only_return=None):
        """

        :param db_name:
        :param collection_name:
        :param key:
        :param value:
        :return:
        """
        if key == "_id" and type(value) is not ObjectId:
            try:
                value = ObjectId(value)
            except Exception as e:
                print(e)
                raise Exception("Value is not valid Object ID")

        db = self.client[db_name]
        collection = db[collection_name]
        if only_return is None:
            return collection.find_one({key: value})
        else:
            return collection.find_one({key: value}, {v: 1 for v in only_return})

    def log_publish(self, task_id, s_time, e_time, num_docs, publish_size, status, parameters):
        collection = self.client[Config.db_name][Config.publish_log_collection]
        resp = collection.insert({'task_id': task_id, 'start_time': s_time, 'end_time': e_time,
                                  'num_docs': num_docs, 'publish_size': publish_size,
                                  'status': status, 'parameters': parameters})
        return resp

    def count_document_query(self, db_name, collection_name, query):
        """
        :param db_name:
        :param collection_name:
        :param key:
        :param value:
        :return:
        """
        query = self._norm_query(query)
        db = self.client[db_name]
        collection = db[collection_name]
        return collection.count(query)

    def count_task_docs(self, task_id, only_non_indexed=False):
        if only_non_indexed:
            return self.count_document_query(Config.db_name, Config.file_collection,
                                             {'task_id': task_id, 'is_indexed': {'$in': [False, None]}})
        else:
            return self.count_document_query(Config.db_name, Config.file_collection, {'task_id': task_id})

if __name__ == "__main__":
    x = Database("mongodb://localhost:6005")
    m = x.client.trainer.train_data.find()
    for x in m:
        print (x)