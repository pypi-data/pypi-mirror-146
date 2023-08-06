import hashlib
import json
import urllib.parse
from alibabacloud_ha3engine import client
from alibabacloud_ha3engine import models
from search_sdk import vector_util

from typing import List, Dict
from search_sdk import snowflake

id_generator = snowflake.IdWorker(1, 1, 0)


class Table:
    _table_name: str = None
    _client: client.Client = None
    _pk_field: str = None
    _data_source_name: str = None
    _hash_field: str = None
    _debug: bool = False

    def __init__(
        self,
        endpoint: str = None,
        instance_id: str = None,
        access_user_name: str = None,
        access_pass_word: str = None,
        table_name: str = None,
        pk_field: str = None,
        data_source_name: str = None,
        hash_field: str = None,
        debug: bool = False,
    ):
        conf = models.Config(
            endpoint=endpoint,
            instance_id=instance_id,
            access_user_name=access_user_name,
            access_pass_word=access_pass_word
        )
        self._client = client.Client(config=conf)
        self._table_name = table_name
        self._pk_field = pk_field
        self._data_source_name = data_source_name
        self._hash_field = hash_field
        self._debug = debug

    def insert(self, dict_list: List[Dict[str, str]]):
        document_array = []
        md5 = hashlib.md5()
        for field_map in dict_list:
            if self._pk_field not in field_map:
                field_map[self._pk_field] = id_generator.get_id()
            if self._hash_field is not None and len(self._hash_field) > 0 and self._hash_field in field_map\
                    and len(field_map.get(self._hash_field)) > 0:
                md5.update(field_map.get(self._hash_field).encode("utf8"))
                hash_value = md5.hexdigest()
                hash_field = self._hash_field + "_hash"
                field_map[hash_field] = hash_value
            add_document = {
                "fields": field_map,
                "cmd": "add"
            }
            document_array.append(add_document)
        request = models.PushDocumentsRequestModel()
        request.body = document_array
        response = self._client.push_documents(self._data_source_name, self._pk_field, request)
        if self._debug:
            print("request:{}, response:{}".format(document_array, response))
        return response.body

    def query(self, query_map: Dict[str, List[str]], page: int, query_num: int):
        query_terms = []
        for index_name, query_words in query_map.items():
            index_query = []
            for query_word in query_words:
                index_query.append("'%s'" % query_word)
            single_query = "%s_index:%s" % (index_name, ' | '.join(index_query))
            query_terms.append(single_query)
        query = ' AND '.join(query_terms)

        start = (page - 1) * query_num
        query_config = models.HaQueryconfigClause(
            start=str(start),
            hit=str(query_num),
            format="JSON",
        )
        sort = models.HaQuerySortClause(sort_key="RANK", sort_order="+")
        ha_query = models.HaQuery(
            query=query,
            cluster="general",
            config=query_config,
            sort=[sort],
        )
        ha_search_query = self._client.build_ha_search_query(haquery=ha_query)
        search_query = models.SearchQuery(query=ha_search_query)
        ha_query_request = models.SearchRequestModel(query=search_query)

        search_response = self._client.search(ha_query_request)
        if self._debug:
            print("request:{}, response:{}".format(ha_query_request, search_response))
        return search_response.body

    def search(self, vec: List[float], filter_expr: str = None, city_id: int = 0, topn: int = 30):
        limit = topn
        if filter_expr is not None and len(filter_expr) > 0:
            limit = 10000
        if city_id > 0:
            query_value = "%d#%s&n=%d" % (city_id, vector_util.vector_str(vec), limit)
            query = "vector_city_index:'%s'" % urllib.parse.quote(query_value)
        else:
            query = "vector_index:'%s&n=%d'" % (vector_util.vector_str(vec), limit)
        query_config = models.HaQueryconfigClause(
            start="0",
            hit=str(topn),
            format="JSON",
            custom_config={"timeout": "2000"},
        )
        kv_pair = {
            "formula": "proxima_score(vector_index)"
        }
        sort = models.HaQuerySortClause(sort_key="RANK", sort_order="+")
        ha_query = models.HaQuery(
            query=query,
            cluster="general",
            config=query_config,
            kvpairs=kv_pair,
            sort=[sort],
        )
        if len(filter_expr) > 0:
            ha_query.filter = filter_expr
        ha_search_query = self._client.build_ha_search_query(haquery=ha_query)
        search_query = models.SearchQuery(query=ha_search_query)
        ha_query_request = models.SearchRequestModel(query=search_query)

        search_response = self._client.search(ha_query_request)
        if self._debug:
            print("request:{}, response:{}".format(ha_query_request, search_response))
        return search_response.body

    def delete(self, pk_value: List[int]):
        document_array = []

        for pk in pk_value:
            del_document_fields = {
                self._pk_field: str(pk)
            }
            add_document = {
                "fields": del_document_fields,
                "cmd": "delete"
            }
            document_array.append(add_document)

        request = models.PushDocumentsRequestModel()
        request.body = document_array
        response = self._client.push_documents(self._data_source_name, self._pk_field, request)
        if self._debug:
            print("request:{}, response:{}".format(request, response))
        return response.body

    def update_annotation(self, raw_field_value: str):
        md5 = hashlib.md5()
        md5.update(raw_field_value.encode("utf8"))
        hash_value = md5.hexdigest()
        hash_field_name = self._hash_field + "_hash"
        query_map = {
            hash_field_name: [hash_value],
        }
        rs = self.query(query_map, 1, 100)
        rs_dict = json.loads(rs)
        id_list = []
        for item in rs_dict['result']['items']:
            if item['fields'][self._hash_field] == raw_field_value:
                id_list.append(item['fields'][self._pk_field])
        if len(id_list) == 0:
            resp = {
                "status": "failed",
                "code": 1
            }
            return json.dumps(resp)
        document_array = []
        for pk_id in id_list:
            update_fields = {
                self._pk_field: pk_id,
                'annotation': '1',
            }
            update_document = {
                'fields': update_fields,
                'cmd': 'update_field',
            }
            document_array.append(update_document)
        request = models.PushDocumentsRequestModel()
        request.body = document_array
        response = self._client.push_documents(self._data_source_name, self._pk_field, request)
        if self._debug:
            print("request:{}, response:{}".format(request, response))
        return response.body
