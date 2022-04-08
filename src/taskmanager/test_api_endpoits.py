import requests

get_response = requests.get( "http://127.0.0.1:8000" )
print(get_response.text)

get_response = requests.get( "http://127.0.0.1:8000/schedule" )
print(get_response.text)

get_response = requests.get( "http://127.0.0.1:8000/schedule", 
                             json={"database":"TJRN30",
                                   "algorithm":"K-Means",
                                   "hyperparameters":{"n_clusters":8,"random_state":214}
                                   }
)
print(get_response.text)