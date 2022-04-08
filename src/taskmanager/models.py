import redis

from flask import jsonify, request

class ExperimentManager():
    def __init__(self) -> None:
        self.redis_client = redis.Redis()
        
    def schedule_experiment(self):
        if not self.valid_schedule(request):
            return jsonify({"status":400, "error":"bad request"})
        response = jsonify( {"echo":request.get_json()} )
        return response

    def valid_schedule(self, request):
        try:
            request.get_json()
        except:
            return False

        return True