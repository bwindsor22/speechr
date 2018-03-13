from enum import Enum

class Endpoints(Enum):
    all_comments = 'all_comments'
    comment_rates = 'comment_rates'
    times_refreshed = 'times_refreshed'
    
    total_scanned = 'total_scanned'
    percent_keyword_hate = 'percent_keyword_hate'
    percent_bow_hate = 'percent_bow_hate'
