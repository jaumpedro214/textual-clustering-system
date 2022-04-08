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
				"vectorization":{"algorithm":"jandaira"}
				}
		get_response = requests.get("http://127.0.0.1:8000/schedule", json=data)
		response_data = get_response.json()

		for key in data.keys():
			self.assertEqual( response_data['data'][key], data[key] )