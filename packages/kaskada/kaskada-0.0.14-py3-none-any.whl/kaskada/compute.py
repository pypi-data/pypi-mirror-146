"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from kaskada.client import Client
from typing import List
import kaskada
import kaskada.api.v1alpha.compute_pb2 as pb
from kaskada.slice_filters import EntityPercentFilter, SliceFilter
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Union
import datetime

import grpc

def query(query: str, with_tables: List[pb.WithTable] = [], with_views: List[pb.WithView] = [], result_behavior: str = 'all-results', response_as: str = 'parquet', data_token_id: str = None, dry_run: bool = False, resume_token: str = None, changed_since_time: Union[str, datetime.datetime, None] = None, limits: pb.QueryRequest.Limits = None, slice_filter: SliceFilter = None, experimental: bool = False, client: Client = None) -> pb.QueryResponse:
    """
    Performs a query

    Args:
        query (str): The query to perform
        with_tables (List[pb.WithTable], optional): A list of tables to use in the query, in addition to the tables stored in the system.
        with_views (List[pb.WithView], optional): A list of views to use in the query, in addition to the views stored in the system.
        result_behavior (str, optional): Determines which results are returned. Either "all-results" (default), or "final-results" which returns only the final values for each entity.
        responsed_as (str, optional): Determines how the response is returned.  Either "parquet" (default) or "redis-bulk".  Note: if "redis-bulk", result_behavior is assumed to be "final-results".
        data_token_id (str, optional): Enables repeatable queries.  Queries performed against the same dataToken are always run on the same input data.
        dry_run(bool, optional): When `True`, the query is validated and if there are no errors, the resultant schema is returned. No actual computation of results is performed.
        resume_token (str, optional): Enables resumeable queries. Queries performed against a resumeToken and a dataToken produce the changed feature values from new data.
        changed_since_time (datetime.datetime, optional): Configure the inclusive datetime after which results will be output.
        limits (pb.QueryRequest.Limits, optional): Configure limits on the output set.
        slice_filter (SliceFilter, optional): Enables slice filter. Currently, only slice entity percent filters are supported. Defaults to None.
        experimental(bool, optional): When `True`, then experimental features are allowed. Data returned when using this flag is not guaranteed to be correct.
        client (Client, optional): The Kaskada Client. Defaults to kaskada.KASKADA_DEFAULT_CLIENT.

    Returns:
        compute_pb.QueryResponse: Response from the API
    """

    if client == None:
        client = kaskada.KASKADA_DEFAULT_CLIENT

    if slice_filter is None:
        slice_filter = kaskada.KASKADA_DEFAULT_SLICE

    timestamp = None
    if isinstance(changed_since_time, str):
        timestamp = Timestamp()
        timestamp.FromJsonString(changed_since_time)
    elif isinstance(changed_since_time, datetime.datetime):
        timestamp = Timestamp()
        timestamp.FromDatetime(changed_since_time)
    elif changed_since_time != None:
        raise Exception('Invalid type for `changed_since_time`. Expected `str` or `datetime.datetime`.')

    try:
        kaskada.validate_client(client)

        request_args = {
            "data_token_id": data_token_id,
            "dry_run": dry_run,
            "experimental_features": experimental,
            "resume_token": resume_token,
            "changed_since_time": timestamp,
            "limits": limits,
            "query" : query,
            "result_behavior": 'RESULT_BEHAVIOR_FINAL_RESULTS' if result_behavior == 'final-results' else 'RESULT_BEHAVIOR_ALL_RESULTS',
            "with_tables" : with_tables,
            "with_views" : with_views,
        }

        if response_as == 'redis-bulk':
            request_args['redis_bulk'] = {}
        else:
            request_args['parquet'] = {}

        if slice_filter is not None:
            if isinstance(slice_filter, EntityPercentFilter):
                request_args['slice'] = {
                    'percent': {
                        'percent': slice_filter.get_percent()
                    }
                }
            else:
                raise Exception('invalid slice filter provided. only EntityPercentFilter is supported')

        req = pb.QueryRequest(**request_args)

        return client.computeStub.Query(req, metadata=client.get_metadata())
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)
