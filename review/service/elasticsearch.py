import logging

from django.conf import settings
from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import streaming_bulk

FAILED_TO_LOAD_ERROR = 'Faild to load {}: {!r}'

logger = logging.getLogger(__name__)

def get_client():
    return Elasticsearch(hosts = [
        {
            'host' : settings.ES_HOST,
            'port' : settings.ES_PORT,
        }
    ])

def bulk_load(movies):
    all_ok = True
    es_movies = (m.as_elasticsearch_dict() for m in movies)
    for ok, result in streaming_bulk(
        get_client(),
        es_movies,
        index = settings.ES_INDEX,
        raise_on_error = False,
    ):
        if not ok:
            all_ok = False
            action, result = result.popitem()
            logger.error(FAILED_TO_LOAD_ERROR.format(result['_id'], result))
    return all_ok

def search_for_movie(query):
    client = get_client()
    result = client.search(index = settings.ES_INDEX, body = {
        'query' : {
            'match' : {
                'text' : query,
            },
        },
    })
    return (h['_source'] for h in result['hits']['hits'])