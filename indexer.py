# DO NOT MODIFY CLASS NAME
import pickle
from os import path

import utils


class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.tweetDict = {}
        self._engineType = ''
        self.config = config

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                posting_data = [term, document.tweet_id, document.term_doc_dictionary[term]]
                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = 1
                else:
                    self.inverted_idx[term] += 1
                if not self.postingDict.keys().__contains__(posting_data[0]):
                    single_term_data = [{"tweet_id": posting_data[1],
                                                          "tf": posting_data[2][0],
                                                          "inx": posting_data[2][1]}]
                    self.postingDict[posting_data[0]] = single_term_data
                else:
                    self.postingDict[posting_data[0]].append({"tweet_id": posting_data[1],
                                                          "tf": posting_data[2][0],
                                                          "inx": posting_data[2][1]})
                if document.tweet_id in self.tweetDict:
                    self.tweetDict[document.tweet_id].update(
                        {term: [document.term_doc_dictionary[term][2],
                                document.term_doc_dictionary[term][0]]})
                else:
                    self.tweetDict[document.tweet_id] = {term: [document.term_doc_dictionary[term][2],
                                                                   document.term_doc_dictionary[term][0]]}

                if len(self.inverted_idx) > 100000:
                    self.remove_least_and_most_idf
            except:
                print('problem with the following key {}'.format(term[0]))

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        index = utils.load_obj(fn)
        self.inverted_idx = index[0]
        self.postingDict = index[1]
        self.tweetDict = index[2]

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj([self.inverted_idx,self.postingDict,self.tweetDict],fn)

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self._is_term_exist(term) else {}

    def set_engine_type(self,type):
        self._engineType = type

    def get_engine_type(self):
        return self._engineType

    def remove_least_and_most_idf(self):
        remove_list = []
        for term in self.inverted_idx:
            if self.inverted_idx[term] <= 1:
                remove_list.append(term)
        print("final inverted inx size: " + str(len(self.inverted_idx)))
        for to_remove in remove_list:
            self.inverted_idx.pop(to_remove)
        sorted_final_data = sorted(self.inverted_idx.items(), key=lambda item: item[1],reverse=True)
        temp = sorted_final_data[:100000]
        self.inverted_idx = dict(temp)
