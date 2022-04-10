# API-related libraries
from flask import jsonify, request
from jsonschema import validate
import json

# This come from a config file
DATABASES = [ "tjrn30", "brlaws" ]
CLUSTERING_ALGORITHMS = [ "kmeans", "hdbscan", "spectral" ]
TEXT_EXTRACTION_ALGORITHMS = ["tfidf", "tfidfkohonen"]

# Get from MongoDB
TEXT_EXTRACTION_MODELS = []

# API endpoits
class ExperimentManager():
    def __init__(self, database) -> None:
        """
        Experiment Manager
        
        Manager of experiment related requests. 
        Wraps API endpoint that adds new experiment to the database.

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
                "clustering":{ 
                    "type":"object",
                    "properties":{ 
                        "algorithm":{
                            "type": "string",
                            "enum": CLUSTERING_ALGORITHMS
                            },
                            "hyperparameters":{"type": "object"}
                    },
                },
                "vectorization":{ "type":"string" }
            }
        }
        self._bad_request = {"status":400, "text":"bad request"}
        
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
        id_ = self.database.insert(data)
        return id_

class ExperimentRequester():
    def __init__(self, database) -> None:
        """
        ExperimentRequester

        Class wraping the API endpoint to provide a experiment description.

        Attributes
        ---------
            database: database object
        """
        self.database = database

    def request_experiment(self):
        """
        Return a experiment description
        """
        data = self.database.request()
                    
        response = jsonify( data )
        return response

class ResultManager():
    """
    Class wraping the API endpoint that recieves a experiment result

    Attributes
    ---------
        database: database object
    """
    
    def __init__(self, database):
        
        self.database = database

        stats_schema = {
            "type":"object",
            "properties":{
                "min":{"type":"number"},
                "max":{"type":"number"},
                "mean":{"type":"number"},
                "std":{"type":"number"}
            },
            "required":["min", "max", "mean", "std"]
        }
        self._result_schema = {
            "type":"object",
            "required":["execution_time", "structure", "nlp-based"],
            "properties":{
                "execution_time":{"type":"number"},
                "structure":{
                    "type":"object",
                    "properties":{
                        "number_of_clusters":{"type":"number"},
                        "percentage_clustered":{"type":"number"},
                        "cluster_size":stats_schema
                    }
                },
                "nlp-based":{
                    "type":"object",
                    "properties":{
                        "coherence":{
                            "type":"object",
                            "properties":{
                                "u_mass":stats_schema,
                                "c_v":   stats_schema,
                                "c_npmi":stats_schema
                            }
                        },
                        "shared_words":stats_schema,
                    }
                }
            },
        }

        self._post_schema = {
            "type":"object",
            "properties":{
                "experiment_data":{
                    "type":"object"
                    ## HERE GOES ALL THE INFORMATION FROM A EXPERIMENT
                },
                "results":self._result_schema,
            }
        }

        self._bad_request = {"status":400, "text":"bad request"}
        
    def post_result(self):
        """
        Recieves a POST request with a result from a experiment and adds it to the database.
        """
        if not self.valid_data(request):
            return jsonify(self._bad_request)

        data = request.get_json()
        id = self.__insert_into_database(data)
        if id==-1:
            return self._bad_request
        
        response = jsonify( { "text":"Result accepted.", 
                              "status":200,
                              "id":id 
                            } )
        return response
    
    def __insert_into_database(self, data):
        try: 
            self._bad_request[ 'exception' ] = "Error when saving data."
            return self.database.insert(data)
        except:
            return -1

    def valid_data(self, response):
        try:
            self._bad_request[ 'exception' ] = "Unable to get json data."
            request.get_json()
        except:           
            return False
        
        data = request.get_json()
        try:
            validate(instance=data, schema=self._post_schema)
        except Exception as exception:
            self._bad_request[ 'exception' ] = str(exception)
            return False

        return True
