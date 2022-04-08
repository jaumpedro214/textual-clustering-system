from flask import Flask

from models import ExperimentManager

app = Flask(__name__)

@app.route('/')
def test():
    return "Cheia de manias, toda dengosa"

    

## API endpoint to request new experiments
experiment_manager = ExperimentManager()

app.add_url_rule('/schedule', 'schedule', 
                 experiment_manager.schedule_experiment, 
                 methods=['GET'] )