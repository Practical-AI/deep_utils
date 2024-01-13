from elasticsearch import AsyncElasticsearch

from deep_utils.utils.logging_utils.logging_utils import value_error_log
from deep_utils.elasticsearch.search_engine.abs_elasticsearch_search_engine import ElasticSearchABS


class AsyncElasticsearchEngin(ElasticSearchABS):
    def __init__(self, elastic_url="http://localhost:9200", es: AsyncElasticsearch = None, timeout=10, logger=None,
                 verbose=1):
        if es is None:
            self.es = AsyncElasticsearch(elastic_url, timeout=timeout)
        elif isinstance(es, AsyncElasticsearch):
            self.es = es
        else:
            value_error_log(logger, "url or es instance are not provided")
        self.verbose = verbose

    async def match_all(self, index: str, size: int = 20):
        """
        query={"match_all": {}}, size=size
        :param index:
        :param size:
        :return:
        """
        resp = await self.es.search(
            index=index,
            query={"match_all": {}},
            size=size,
        )
        return resp

    async def search_match_query(self, index, field="", value="", keyword="match", size=None,
                                 return_source: bool = False):
        """
        A simple match search
        {
        "query": {
            "keyword": {
                "field": "value"
                     }
                 }
         }
        :param index:
        :param field:
        :param value:
        :param keyword:
        :param size:
        :param return_source:
        :return:

        """
        query = self.get_match_query(field_name=field, field_value=value, keyword=keyword)
        results = await self.es.search(index=index, query=query, size=size)
        hits = AsyncElasticsearchEngin.get_hits(results.body, return_source=return_source)
        return hits

    async def prefix(self, index: str, field: str, value: str, size: int = 10,
                     return_source: bool = True):
        """
        GET /_search
            {
              "query": {
                "prefix" : { field : value }
              }
            }
        :param index:
        :param field:
        :param value:
        :param size:
        :param return_source:
        :return:
        """
        query = {"prefix": {field: value}}
        results = await self.es.search(index=index, query=query, size=size)
        hits = AsyncElasticsearchEngin.get_hits(results.body, return_source=return_source)
        return hits
