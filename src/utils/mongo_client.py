import bson
import logging
import pymongo
from etools.singleton_meta import SingletonMeta
from bson.objectid import ObjectId
from tornado.options import options
from etools.utils import clear_none_in_dict


class MongoClient(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = None
        self.record_collection = None

    def connect(self):
        self.client = pymongo.MongoClient(options.mongo_addr)
        self.record_collection = self.client[options.mongo_db][options.mongo_collection]

    def disconnect(self):
        self.client.close()

    def insert_record(self, sid, tid, gid, cid, user_locator, speaker, timestamp, content):
        record = {
            "sid": sid,
            "tid": tid,
            "gid": gid,
            "cid": cid,
            "cookie": user_locator.cookie,
            "user_id": user_locator.user_id,
            "timestamp": bson.Int64(timestamp),
            "speaker": speaker,
            "content": content
        }
        record = clear_none_in_dict(record)
        try:
            return str(self.record_collection.insert_one(record).inserted_id)
        except Exception as e:
            self.logger.exception("insert record[%s] failed, exception[%s]",
                                  record, e)
            return None

    def search_record(self, user_locator, timestamp, count):
        if user_locator.user_id is not None:
            key, value = "user_id", user_locator.user_id
        else:
            key, value = "cookie", user_locator.cookie
        query = {key: value, "timestamp":{"$lt": timestamp}}
        records = self.record_collection.find(query).sort("timestamp", -1).limit(count)
        records = list(records)
        for r in records:
            r["id"] = str(r["_id"])
            for k in ["_id", "sid", "tid", "gid", "cid", "cookie", "user_id"]:
                r.pop(k, None)
        return records

    def evaluate(self, record_id, correct):
        result = self.record_collection.update({
            "_id": ObjectId(record_id),
        }, {
            "$set": {
                "correct": correct,
                "content": {
                    "data": {
                        "evaluation": False
                    }
                }
            }
        })
        count = result.get("n")
        if count != 1:
            self.logger.warning("evalute record [%s], correct [%s] result [%s]",
                                record_id, correct, result)
            return False
        return True


mongo_client = MongoClient()
