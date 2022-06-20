import logging
from typing import Sequence, TypeVar

from Client import GRPCQueryDispatcher, RabbitMQQueryDispatcher
from Logger.CustomLogFormatter import CustomLogFormatter
from Message import *

logger = logging.getLogger("QueryUtils")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)


class QueryBuilder:
    __query_type: str
    __query_paths: Sequence[str]
    __query_data: dict
    __executor: Executor

    def data(self, data: dict):
        self.__query_data = data
        return self

    def query_type(self, query_type: str):
        self.__query_type = query_type
        return self

    def paths(self, paths: Sequence[str]):
        self.__query_paths = paths
        return self

    def executor(self, executor):
        self.__executor = executor
        return self

    def build(self):
        return {
            'Size': SizeQuery(self.__query_paths, self.__query_data, self.__executor),
            'Colors': ColorQuery(self.__query_paths, self.__query_data, self.__executor),
            'Dogs': DogsQuery(self.__query_paths, self.__query_data, self.__executor),
            'Similarity': SimilarityQuery(self.__query_paths, self.__query_data, self.__executor),
            'Faces': FacesQuery(self.__query_paths, self.__query_data, self.__executor),
            'Formats': FormatQuery(self.__query_paths, self.__query_data, self.__executor),
            'Body': BodyQuery(self.__query_paths, self.__query_data, self.__executor),
            'Animals': AnimalQuery(self.__query_paths, self.__query_data, self.__executor),
            'Styles': StyleQuery(self.__query_paths, self.__query_data, self.__executor),
            'People': PeopleQuery(self.__query_paths, self.__query_data, self.__executor),
            'Text': TextQuery(self.__query_paths, self.__query_data, self.__executor),
            'Metadata': MetadataQuery(self.__query_paths, self.__query_data, self.__executor),
            'Weather': WeatherQuery(self.__query_paths, self.__query_data, self.__executor)
        }[self.__query_type]


class QueryExecutor:
    def __init__(self):
        self.__rmq_dispatcher = RabbitMQQueryDispatcher()
        self.__grpc_dispatcher = GRPCQueryDispatcher()
        self.__http_dispatcher = ...

    # This is a lie
    M = TypeVar('M', bound=Message)

    def execute(self, queries: Sequence[M], query_cb):
        new_paths = queries[0].paths

        current_query = 1
        for query in queries:
            query.paths = new_paths
            result = ""
            if query.executor == Executor.RabbitMQ:
                result = self.__rmq_dispatcher.dispatch_query(query)
            elif query.executor == Executor.GRPC:
                result = self.__grpc_dispatcher.dispatch_query(query)
            elif query.executor == Executor.HTTP:
                ...
            else:
                # Throw something, dunno
                ...
            current_query += 1
            query_cb(result, current_query)
