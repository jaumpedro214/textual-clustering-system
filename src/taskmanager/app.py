from crypt import methods
from flask import Flask

from endpoints import ExperimentManager, ExperimentRequester, ResultManager, TextExtractionModelManager

from databases import DummyDatabase, ResultsDatabase, ExperimentDatabase, TextExtractionModelsDatabase

app = Flask(__name__)

@app.route('/')
def test():
    return "Cheia de manias, toda dengosa"


# Experiment endpoints
experiments_database = ExperimentDatabase()
experiment_manager = ExperimentManager(experiments_database)
experiment_requester = ExperimentRequester(experiments_database)

# Text Extraction Models endpoint
text_extr_model_manager = TextExtractionModelManager( TextExtractionModelsDatabase() )

# Result endpoints
results_database = ResultsDatabase()
result_manager = ResultManager( results_database )

app.add_url_rule( '/create-text-extraction-model', 'create-text-extraction-model',
                  text_extr_model_manager.post_text_algorithm,
                  methods=['POST'] 
                )

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