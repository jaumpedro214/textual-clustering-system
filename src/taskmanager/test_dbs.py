# Imports iniciais
import pymongo
import redis


try:
    pymongo.MongoClient('localhost',27017)
except:
    print("Unable to connect to MongDB")


try:
    redis.Redis()
except:
    print("Unable to connect to Redis")
