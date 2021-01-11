# you can change whatever you want in this module, just make sure it doesn't 
# break the searcher module
import math


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_docs(relevant_docs, k=None):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param k: number of most relevant docs to return, default to everything.
        :param relevant_docs: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        ranked_results = sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)
        #ranked_results = sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)
        if k is not None:
            ranked_results = ranked_results[:k]
        return [d[0] for d in ranked_results]

    def cos_sim_ranking(self, indexer, relevant_docs, query):
        w_ij_table = dict()
        ranked_docs = dict()
        w_iq = math.sqrt(len(query))
        # iter_counter = len(relevant_docs.keys())
        #mapped_tweets = dict()
        # tweet not in mapped_tweets.values()
        for curr_tweet in relevant_docs:
            # if curr_tweet in w_ij_table.keys():
            #    continue
            curr_tweet = curr_tweet
            for term in indexer.tweetDict[curr_tweet]:
                if term in indexer.inverted_idx.keys():
                    idf = math.log2(len(indexer.tweetDict) / indexer.inverted_idx[term])
                    tf = indexer.tweetDict[curr_tweet][term][0]
                    tf_idf = tf * idf
                    tf_idf_pow = math.pow(2, tf_idf)
                    if curr_tweet in w_ij_table:
                        if term in query:
                            w_ij_table[curr_tweet] = [w_ij_table[curr_tweet][0] + tf_idf,
                                                      w_ij_table[curr_tweet][1] + tf_idf_pow]
                        else:
                            w_ij_table[curr_tweet][1] = w_ij_table[curr_tweet][1] + tf_idf_pow
                    else:
                        w_ij_table[curr_tweet] = [0, 0]
                        w_ij_table[curr_tweet] = [tf_idf, tf_idf_pow]
                else:
                    continue
            sum_w_ij = w_ij_table[curr_tweet][0]
            denominator = math.sqrt(w_ij_table[curr_tweet][1]) * w_iq
            ranked_docs[curr_tweet] = sum_w_ij / denominator
        return ranked_docs