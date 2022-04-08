import requests
from jsonschema import validate

get_response = requests.get( "http://127.0.0.1:8000/schedule" )
print(get_response.text)

get_response = requests.get( "http://127.0.0.1:8000/schedule", 
                             json={"database":"tjrn30",
                                   "clustering":{ "algorithm":"kmeans",
                                                  "hyperparameters":{}
                                                },
                                   "vectorization":{"algorithm":"jandaira" }
                                   }
                           )
print(get_response.text)