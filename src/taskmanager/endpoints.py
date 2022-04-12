# API-related libraries
from flask import jsonify, request
from jsonschema import validate

# This come from a config file
DATABASES = [ "tjrn30", "brlaws" ]
CLUSTERING_ALGORITHMS = [ "kmeans", "hdbscan", "spectral" ]
TEXT_EXTRACTION_ALGORITHMS = ["tfidf", "tfidfkohonen"]

# Get from MongoDB
TEXT_EXTRACTION_MODELS = []

# API endpoits

class InsertDataEndpoint():
    def __init__(self, database):
        """
        Base class for all POST endpoints

        Attributes
        ---------
            database: database object
        """
        self._bad_request = {"status":400, "text":"bad request"}
        self.database = database
        self._schema = {}

    def valid_data(self, request):
        """
        Validate schedule request
        """
        try:
            data = request.get_json()
        except:
            return False

        try: 
            validate(instance=data, schema=self._schema)
        except:
            return False

        return True

    def _insert_into_database(self, data):
        try:
            return self.database.insert(data)
        except:
            return -1

class ExperimentManager( InsertDataEndpoint ):
    def __init__(self, *args, **kwargs):
        """
        the API endpoint that schedules the experiments
        """
        super( ExperimentManager, self ).__init__( *args, **kwargs )

        self._schema = { 
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
        
    def schedule_experiment(self):
        """
        Add a experiment to the schedule list
        """
        if not self.valid_data(request):
            return jsonify(self._bad_request)

        data = request.get_json()
        id = self._insert_into_database(data)
        response = jsonify( { "text":"Experiment sucessfully created.", 
                              "data":data,
                              "id":id 
                            } )
        return response

class ResultManager( InsertDataEndpoint ):
    """
    Class wraping the API endpoint that recieves a experiment result
    """
    
    def __init__(self, *args, **kwargs):
        super( ResultManager, self ).__init__( *args, **kwargs )

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

        self._schema = {
            "type":"object",
            "properties":{
                "experiment_data":{
                    "type":"object"
                    ## HERE GOES ALL THE INFORMATION FROM A EXPERIMENT
                },
                "results":self._result_schema,
            }
        }
        
    def post_result(self):
        """
        Recieves a POST request with a result from a experiment and adds it to the database.
        """
        if not self.valid_data(request):
            return jsonify(self._bad_request)

        data = request.get_json()
        id = self._insert_into_database(data)
        if id==-1:
            return self._bad_request
        
        response = jsonify( { "text":"Result accepted.", 
                              "status":200,
                              "id":id 
                            } )
        return response

class TextExtractionModelManager( InsertDataEndpoint ):

    def __init__(self, *args, **kwargs):
        super( TextExtractionModelManager, self ).__init__( *args, **kwargs )
        self._schema = {
            "type":"object",
            "properties":{
                "hyperparameters":{ "type":"object" },
                "algorithm":{ 
                    "type":"string",
                    "enum":TEXT_EXTRACTION_ALGORITHMS
                    },
                "name":{ "type":"string" },
            }
        }

    def post_text_algorithm(self):
        """
        Recieves a POST request with a vectorizing algorithm and adds it to the database.
        """
        if not self.valid_data(request):
            return jsonify(self._bad_request)

        data = request.get_json()
        id = self._insert_into_database(data)
        if id==-1:
            return self._bad_request
        
        response = jsonify( { "text":"Algorithm accepted.", 
                              "status":200,
                              "id":id 
                            } )
        return response


class ExperimentRequester():
    def __init__(self, database) -> None:
        """
        Class wraping the API endpoint to provide a experiment description.
        """
        self.database = database

    def request_experiment(self):
        """
        Return a experiment description
        """
        data = self.database.request()
                    
        response = jsonify( data )
        return response