from flask import Flask

from models import ExperimentManager, ExperimentRequester, ExperimentDatabase

app = Flask(__name__)

@app.route('/')
def test():
    return "Cheia de manias, toda dengosa"

database = ExperimentDatabase()
experiment_manager = ExperimentManager(database)
experiment_requester = ExperimentRequester(database)

app.add_url_rule('/schedule', 'schedule', 
                 experiment_manager.schedule_experiment, 
                 methods=['GET'] )
app.add_url_rule('/request', 'request', 
                 experiment_requester.request_experiment, 
                 methods=['GET'] )