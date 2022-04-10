# Database libraries
import pymongo
import redis
import uuid
import datetime
import json

# API Database Classes
class ExperimentDatabase():
    def __init__(self):
        """
        Database that stores the experiments description
        """
        # 'redis' is the hostname of the redis container on the application’s network
        self.client = redis.Redis(host='redis', port=6379)

    def insert(self, data):
        """
        Insert the experiment into the database.

        Attributes
        ----------
            data: python dict
        """
        experiment_id = "experiment_"+str(uuid.uuid1())
        data['id'] = experiment_id
        data_string = json.dumps(data)

        self.client.set(experiment_id, data_string)
        self.client.lpush("experiment-list", experiment_id)

        return experiment_id

    def request(self):
        """
        Return a experiment registered on the database
        """
        id = self.client.rpop( "experiment-list" )

        if not id:
            return {"text":"experiment list is empty"}

        data_string = self.client.get( id )
        data = json.loads(data_string) 
        self.client.delete(id)

        return data

class ResultsDatabase():
    def __init__(self) -> None:
        """
        Database that stores the experiment's results
        """
        self.client = pymongo.MongoClient('mongo', 27017)

    def insert(self, data):
        # Setting the experiment id as the entry id
        data["_id"] = data["experiment_data"]["id"]

        # Connecting to the Mongo Database 'db'
        db = self.client.db
        db.results.insert_one( data )

        return data["_id"]

class DummyDatabase():
    def insert(self, data):
        return 0
