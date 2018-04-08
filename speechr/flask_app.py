from flask import Flask
from speechr.endpoints_enum import Endpoints


class FlaskApp:

    def __init__(self, cache):
        self.app = Flask(__name__)

        self.cache = cache
        self.app.add_url_rule('/status',               'status',                            self.status)
        self.app.add_url_rule('/all_comments',         Endpoints.all_comments.name,         self.all_comments)
        self.app.add_url_rule('/comment_rates',        Endpoints.comment_rates.name,        self.comment_rates)
        self.app.add_url_rule('/times_refreshed',      Endpoints.times_refreshed.name,      self.times_refreshed)
        self.app.add_url_rule('/total_scanned',        Endpoints.total_scanned.name,        self.total_scanned)
        self.app.add_url_rule('/rolling_total_hate',   Endpoints.rolling_total_hate.name,        self.rolling_total_hate)
        self.app.add_url_rule('/percent_keyword_hate', Endpoints.percent_keyword_hate.name, self.percent_keyword_hate)
        self.app.add_url_rule('/percent_bow_hate',     Endpoints.percent_bow_hate.name,     self.percent_bow_hate)
        
        
        self.app.run(host='0.0.0.0')
    
    def status(self):
        return 'Server running'
        
    def all_comments(self):
        return self.cache[Endpoints.all_comments]

    def comment_rates(self):
        return self.cache[Endpoints.comment_rates]

    def times_refreshed(self):
        return self.cache[Endpoints.times_refreshed]
    
    def total_scanned(self):
        return self.cache[Endpoints.total_scanned]
    
    def rolling_total_hate(self):
        return self.cache[Endpoints.rolling_total_hate]
    
    def percent_keyword_hate(self):
        return self.cache[Endpoints.percent_keyword_hate]
    
    def percent_bow_hate(self):
        return self.cache[Endpoints.percent_bow_hate]
