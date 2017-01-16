#Prompt: search the given Yelp database for the online review that is most unique using MapReduce

# This code is modified from code originally written by Jim Blomo and Derek Kuo



from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep

import re

WORD_RE = re.compile(r"[\w']+")

class UniqueReview(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def mapper1_extract_words(self, _, record):
        """Take in a record, yield <word, review_id>"""
        for word in WORD_RE.findall(record['text']):
            yield [word.lower(), record['review_id']]

    def reducer1_count_reviews(self, word, review_ids):
        """Count the number of reviews a word has appeared in.  If it is a
        unique word (ie it has only been used in 1 review), output that review
        and 1 (the number of words that were unique)."""

        unique_reviews = list(set(review_ids))  # set() uniques an iterator
        if len(unique_reviews) == 1:
            yield [unique_reviews[0], 1]

    def reducer2_count_unique_words(self, review_id, unique_word_counts):
        """Output the number of unique words for a given review_id"""
        words_reviews = len(list(unique_word_counts))
        # print('{} contains {} unique words'.format(review_id, words_reviews))
        yield [review_id, words_reviews]


    def mapper3_aggregate_max(self, review_id, unique_word_count):
        """Group reviews/counts together by the MAX statistic."""
        yield ['MAX', [unique_word_count, review_id]]

    def reducer3_select_max(self, stat, count_review_ids):
        """Given a list of pairs: [count, review_id], select on the pair with
        the maximum count, and output the result."""
        [max_count, review_id] = max(count_review_ids)
        yield [review_id, max_count]

    def steps(self):
        return [MRStep(mapper=self.mapper1_extract_words, reducer=self.reducer1_count_reviews),
                MRStep(reducer=self.reducer2_count_unique_words),
                MRStep(mapper=self.mapper3_aggregate_max, reducer=self.reducer3_select_max)]

if __name__ == '__main__':
    UniqueReview.run()
