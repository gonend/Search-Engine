import pandas as pd
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils


# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model = None
        self._indexer.set_engine_type('1')

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        df = pd.read_parquet(fn, engine="pyarrow")
        documents_list = df.values.tolist()
        # Iterate over every document in the file
        number_of_documents = 0
        Etype = self._indexer.get_engine_type()
        if Etype == "1":
            stemming = True
        elif Etype == "2":
            stemming = False
        elif Etype == "3":
            stemming = False
        elif Etype == "best":
            stemming = False

        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document,stemming)
            number_of_documents += 1
            print(number_of_documents)
            # index the document data
            if parsed_document is None:
                continue
            self._indexer.add_new_doc(parsed_document)
        #self._indexer.save_index("idx_bench")
        if len(self._indexer.inverted_idx) > 100000:
            self._indexer.remove_least_and_most_idf()
        print('Finished parsing and indexing.')

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """

        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self, model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and
        assign to self._model, which is passed on to the searcher at query time.
        """
        pass

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        #if self._indexer is None:
        #    Indexer.load_index("idx_bench")
        searcher = Searcher(self._parser, self._indexer, model=self._model)
        return searcher.search(query)
