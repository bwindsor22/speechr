from flask import Flask
from speechr.endpoints_enum import Endpoints


class FlaskApp:

    def __init__(self, cache):
        self.app = Flask(__name__)

        self.cache = cache
        self.app.add_url_rule('/status', 'status', self.status)
        self.app.add_url_rule('/all_comments', Endpoints.all_comments.name, self.all_comments)
        self.app.add_url_rule('/comment_rates', Endpoints.comment_rates.name, self.comment_rates)
        self.app.add_url_rule('/times_refreshed', Endpoints.times_refreshed.name, self.times_refreshed)
        
        self.app.run(host='0.0.0.0')
    
    def status(self):
        return 'Server running'
        
    def all_comments(self):
        return self.cache[Endpoints.all_comments]

    def comment_rates(self):
        return self.cache[Endpoints.comment_rates]

    def times_refreshed(self):
        return self.cache[Endpoints.times_refreshed]
