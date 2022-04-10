from crypt import methods
from flask import Flask

from models import ExperimentManager, ExperimentRequester, ResultManager
from databases import DummyDatabase, ResultsDatabase, ExperimentDatabase

app = Flask(__name__)

@app.route('/')
def test():
    return "Cheia de manias, toda dengosa"

experiments_database = ExperimentDatabase()
experiment_manager = ExperimentManager(experiments_database)
experiment_requester = ExperimentRequester(experiments_database)

results_database = ResultsDatabase()
result_manager = ResultManager( results_database )

app.add_url_rule('/schedule', 'schedule', 
                 experiment_manager.schedule_experiment, 
                 methods=['GET', 'POST'] )
                 
app.add_url_rule('/request', 'request', 
                 experiment_requester.request_experiment, 
                 methods=['GET'] )

app.add_url_rule('/result', 'result',
                 result_manager.post_result,
                 methods=['POST']
                 )