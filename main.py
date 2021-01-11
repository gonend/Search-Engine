import search_engine_1
import search_engine_2
import search_engine_3
import search_engine_best

if __name__ == '__main__':
    se = search_engine_best.SearchEngine()
    se.build_index_from_parquet("C:\\Users\\david\\PycharmProjects\\Search_Engine\\data\\benchmark_data_train.snappy.parquet")
    print(se.search("30-62000"))
    print("commit")
#"C:\\Users\\david\\Search_Engine\\testData"
#C:\\Users\\david\\PycharmProjects\\Search_Engine-master\\testData
