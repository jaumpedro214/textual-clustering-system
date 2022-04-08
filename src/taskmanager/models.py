import redis

from flask import jsonify, request

from jsonschema import validate

DATABASES = [ "tjrn30", "brlaws" ]
CLUSTERING_ALGORITHMS = [ "kmeans", "hdbscan", "spectral" ]
TEXTUAL_EXTRACTION_ALGORITHMS = ["tfidf"]

class ExperimentManager():
    def __init__(self) -> None:
        """
        Experiment Manager
        
            Manager of experiment related requests
        """
        self.redis_client = redis.Redis()
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
                    
        response = jsonify( {"echo":request.get_json()} )
        return response

    def valid_schedule(self, request):
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