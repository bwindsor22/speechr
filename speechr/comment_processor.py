import resource_loader
import pandas as pd
import numpy as np
from speechr.classifiers import bow_classifier, keyword_classifier


class Processor:
    def __init__(self):
        slurs = resource_loader.load_csv_resource_to_list('racial_slurs')
        violent_words = resource_loader.load_csv_resource_to_list('violent_words')

        self.CC = keyword_classifier.KeywordClassifier(slurs, violent_words)
        self.BOWC = bow_classifier.BagOfWordsClassifier()
        # self.toxic_users = get_toxic_users.Toxic_Users()
        # self.toxic_users.run()

    def clear(self):
        self.potential_hate_comments = pd.DataFrame(data=np.zeros((0, len(columns))), columns=columns)

        scores_cols = ['comment_id', 'score']
        self.keyword_scores = pd.DataFrame(data=np.zeros((0, len(scores_cols))), columns=scores_cols)
        self.bag_of_words_scores = pd.DataFrame(data=np.zeros((0, len(scores_cols))), columns=scores_cols)

        count_keyword_scores = len(self.keyword_scores[self.keyword_scores.score > 0])
        count_bow_scores = len(self.bag_of_words_scores[self.bag_of_words_scores.score > 0])

    def process_comment_list(self, comment_list, redditor_list, i, hate_sub, columns, last_scan_time):
        for comment in comment_list:
            j = 0
            if datetime.datetime.utcfromtimestamp(comment.created_utc) < last_scan_time:
                self.logger.debug('skipping')
                continue

            self.i += 1
            if self.i % 100 == 0:
                self.logger.info('processing comment # ' + str(self.i))

            keyword_score = self.CC.analyze(comment.body)
            bow_score = self.BOWC.analyze(comment.body)
            self.logger.debug('comment {}, keyword {}, bow {}'.format(comment.body, keyword_score, bow_score))

            if keyword_score > 0 or bow_score > 0:
                time = datetime.datetime.utcfromtimestamp(comment.created_utc)
                current_time = datetime.datetime.utcnow()
                temp_df = pd.DataFrame([[comment.id, \
                                         redditor_list[j], \
                                         time, \
                                         comment.permalink, \
                                         hate_sub, \
                                         comment.score, \
                                         comment.body, \
                                         current_time]],
                                       columns=columns)
                j += 1
                temp_keyword = pd.DataFrame([[comment.id, keyword_score]],
                                            columns=self.keyword_scores.columns.values.tolist())
                temp_bowc = pd.DataFrame([[comment.id, bow_score]],
                                         columns=self.bag_of_words_scores.columns.values.tolist())

                self.potential_hate_comments = pd.concat(
                    [self.potential_hate_comments.reset_index(drop=True), temp_df.reset_index(drop=True)], axis=0)
                self.keyword_scores = pd.concat(
                    [self.keyword_scores.reset_index(drop=True), temp_keyword.reset_index(drop=True)], axis=0)
                self.bag_of_words_scores = pd.concat(
                    [self.bag_of_words_scores.reset_index(drop=True), temp_bowc.reset_index(drop=True)], axis=0)

                self.logger.info(comment.body)
                self.logger.info('keyword_score: ' + str(keyword_score))
                self.logger.info('bag of words score: ' + str(bow_score))

            # self.logger.info('comment_length = ' + str(self.i))
            self.comments_scanned = self.i

            self.logger.info('hate sub: ' + str(hate_sub) \
                             + '; comments scanned: ' + str(self.comments_scanned) \
                             + '; bow score: ' + str(len(self.bag_of_words_scores)))



    def load_and_clear_subreddit_comments_scores(self):
        self.DB.load_df(self.keyword_scores, 'keyword_scores', 'append')
        self.keyword_scores = self.keyword_scores.iloc[0:0]

        self.DB.load_df(self.bag_of_words_scores, 'bow_scores', 'append')
        self.bag_of_words_scores = self.bag_of_words_scores.iloc[0:0]
