import requests
import unittest

class TestScheduleEndpoint(unittest.TestCase):

	def test_return_error_no_params(self):
		get_response = requests.get( "http://127.0.0.1:8000/schedule" )
		data = get_response.json()
		self.assertEqual( data['status'], 400 )

	def test_return_sucess_correct_params(self):
		data = {"database":"tjrn30",
		        "clustering":{ "algorithm":"kmeans",
				               "hyperparameters":{}
							 },
				"vectorization":"tfidf"
				}
		response = requests.post("http://127.0.0.1:8000/schedule", json=data)
		response_data = response.json()

		for key in data.keys():
			self.assertEqual( response_data['data'][key], data[key] )

class TestResultEndpoint(unittest.TestCase):
	def test_return_error_no_params(self):
		response = requests.post( "http://127.0.0.1:8000/result" )
		data = response.json()
		self.assertEqual( data['status'], 400 )

	def test_return_error_wrong_params(self):
		## Dont contain execution time
		incorrect_data = {
			"experiment_data":{},
			"results":{
				"structure":{
					"number_of_clusters":10,
					"percentage_clustered":0.91,
					"cluster_size":{ "min":1, "max":10, "mean":5, "std":1 }
				},
				"nlp-based":{
					"coherence":{
						"u_mass":{ "min":1, "max":10, "mean":5, "std":1 },
						"c_v":{ "min":1, "max":10, "mean":5, "std":1 },
						"c_npmi":{ "min":1, "max":10, "mean":5, "std":1 }
					},
					"shared_words":{"min":1, "max":10, "mean":5, "std":1 }
				}
			}
		}

		response = requests.post( "http://127.0.0.1:8000/result", json=incorrect_data )
		data = response.json()
		self.assertEqual(data['status'], 400 )

	def test_return_sucess_correct_params(self):
		correct_data = {
			"experiment_data":{"id":"experiment_result_mongodb_test"},
			"results":{
				"execution_time":12.1,
				"structure":{
					"number_of_clusters":10,
					"percentage_clustered":0.91,
					"cluster_size":{ "min":1, "max":10, "mean":5, "std":1 }
				},
				"nlp-based":{
					"coherence":{
						"u_mass":{ "min":1, "max":10, "mean":5, "std":1 },
						"c_v":{ "min":1, "max":10, "mean":5, "std":1 },
						"c_npmi":{ "min":1, "max":10, "mean":5, "std":1 }
					},
					"shared_words":{"min":1, "max":10, "mean":5, "std":1 }
				}
			}
		}

		response = requests.post( "http://127.0.0.1:8000/result", json=correct_data )
		data = response.json()
		self.assertEqual( data['status'], 200 )