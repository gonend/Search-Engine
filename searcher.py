from ranker import Ranker
import nltk
#nltk.download
from nltk.corpus import wordnet as wn
from spellchecker import SpellChecker
from nltk.corpus import lin_thesaurus as thes
import utils


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model 
    # parameter allows you to pass in a precomputed model that is already in 
    # memory for the searcher to use such as LSI, LDA, Word2vec models. 
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=30):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        query_as_list = []
        Etype = self._indexer.get_engine_type()

        if Etype == '1': #or Etype == 'best':
            print("Runnig on WordNet Method")
            stemming = True
            query_as_list = self._parser.parse_sentence(query, stemming)
            self.wordnet_method(query_as_list)

        elif Etype == '2':
            print("Runnig on Spelling Correction Method")
            stemming = False
            query_as_list = self._parser.parse_sentence(query, stemming)
            query_as_list = self.spelling_Correction_method(query_as_list)

        elif Etype == '3':
            print("Runnig on Tesaurus Method")
            stemming = False
            query_as_list = self._parser.parse_sentence(query, stemming)
            self.thesaurus_method(query_as_list)
            print("thesaurus method")

        elif Etype == 'best':
            print("Runing Best")
            stemming = False
            query_as_list = self._parser.parse_sentence(query, stemming)
            query_as_list = self.spelling_Correction_method(query_as_list)
            self.wordnet_method(query_as_list)

        relevant_docs = self._relevant_docs_from_posting(query_as_list)
        n_relevant = len(relevant_docs)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs)
        cos_docs = Ranker.cos_sim_ranking(self._ranker, self._indexer,ranked_doc_ids,query_as_list)
        final_docs = Ranker.rank_relevant_docs(cos_docs)
        for doc in final_docs:
            print(doc)
        return n_relevant, final_docs


    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        relevant_docs = {}
        for term in query_as_list:
            posting_list = self._indexer.get_term_posting_list(term)
            for tweet in posting_list:
                tweet = tweet['tweet_id']
                df = relevant_docs.get(tweet, 0)
                relevant_docs[tweet] = df + 1
        #relevant_docs = sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)
        return relevant_docs

    def wordnet_method(self, query_as_list):
        optional_syn = {}
        for word in query_as_list:
            count = 0
            try:
                syns = wn.synsets(word)
                if len(syns) > 0:
                    cur_word = word  #+"."+str(syns[0].pos())
                    optional_syn[cur_word] = list()
                    for synSet in syns:
                        optional_syn[cur_word].append(synSet._name)
            except:
                #print(query_as_list[i] + " is not in wordent dict")
                continue
        #print(optional_syn)
        extneded_words = self.wordNet_highest_sim(optional_syn)
        #print(extneded_words)
        #print("hell yea")
        for tuple in extneded_words:
            query_as_list.append(tuple[2])
        return query_as_list

    def wordNet_highest_sim(self, optional_syn):
        score_tuples = list()
        for query_word in optional_syn.keys():
            curr_word = wn.synsets(query_word)[0]
            for sim_word in optional_syn[query_word]:
                w = wn.synset(sim_word)
                key_word = query_word.replace("." + str(curr_word.pos()) + ".01", '')
                lemma_name = w._lemma_names[0]
                if lemma_name != key_word:
                    sim = curr_word.wup_similarity(w)
                    if sim is not None:
                        t = [sim, key_word, lemma_name]
                        score_tuples.append(t)
        score_tuples.sort(reverse=True)
        #print(score_tuples)
        return score_tuples[:4]

    def spelling_Correction_method(self,query_as_list):
        correction_option = {}
        sc = SpellChecker()
        for term in query_as_list:
            if term not in self._indexer.inverted_idx.keys():
                correction = sc.correction(term)
                if correction in self._indexer.inverted_idx.keys():
                    if term not in correction_option.keys():
                        correction_option[term] = correction
        for replacment in correction_option.keys():
            inx = query_as_list.index(replacment)
            query_as_list.pop(inx)
            query_as_list.insert(inx,correction_option[replacment])
        return query_as_list

    def thesaurus_method(self,query_as_list):
        replace_syn = []
        for word in query_as_list:
            try:
                syn_options = list(thes.scored_synonyms(word,fileid="simN.lsp"))
                if len(syn_options) > 0:
                    replace_syn.append(syn_options[0])
            except:
                print(word + " is not in thes dict")
        if replace_syn:
            for elem in replace_syn:
                query_as_list.append(elem[0])
        return query_as_list