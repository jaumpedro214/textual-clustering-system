# Database libraries
import redis
import uuid
import datetime

# API-related libraries
from flask import jsonify, request
from jsonschema import validate
import json

DATABASES = [ "tjrn30", "brlaws" ]
CLUSTERING_ALGORITHMS = [ "kmeans", "hdbscan", "spectral" ]
TEXTUAL_EXTRACTION_ALGORITHMS = ["tfidf"]

class ExperimentDatabase():
    def __init__(self) -> None:
        # 'redis' is the hostname of the redis container on the application’s network
        self.client = redis.Redis(host='redis', port=6379)

    def insert_experiment(self, data):
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

    def request_experiment(self):
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

class ExperimentManager():
    def __init__(self, database) -> None:
        """
        Experiment Manager
        
        Manager of experiment related requests

        Attributes
        ---------
        database: database object
        """
        self.database = database
        self._experiment_schema = { 
                                    "type":"object",
                                    "properties":{
                                        "database":{"type":"string",
                                                    "enum":DATABASES
                                                    },
                                        "clustering":{ "type":"object",
                                                       "properties":{ 
                                                                      "algorithm":{"type": "string",
                                                                                   "enum":CLUSTERING_ALGORITHMS
                                                                                  },
                                                                      "hyperparameters":{"type": "object"}
                                                                    },
                                                     },
                                        "vectorization":{ "type":"object", 
                                                          "properties":{ "algoritm":{"type": "string"} } 
                                                        }
                                    }
                                  }
        self._bad_request = {"status":400, "error":"bad request"}
        
    def schedule_experiment(self):
        """
        Add a experiment to the schedule list
        """
        if not self.valid_schedule(request):
            return jsonify(self._bad_request)

        data = request.get_json()
        id = self.__insert_into_database(data)
        response = jsonify( { "text":"Experiment sucessfully created.", 
                              "data":data,
                              "id":id 
                            } )
        return response

    def valid_schedule(self, request):
        """
        Validate schedule request
        """

        try:
            request.get_json()
        except:
            return False
        
        data = request.get_json()
        
        try: 
            validate(instance=data, schema=self._experiment_schema)
        except:
            return False

        return True

    def __insert_into_database(self, data):
        id_ = self.database.insert_experiment(data)
        return id_

class ExperimentRequester():
    def __init__(self, database) -> None:
        self.database = database

    def request_experiment(self):
        """
        Return a experiment
        """
        data = self.database.request_experiment()
                    
        response = jsonify( data )
        return response
        