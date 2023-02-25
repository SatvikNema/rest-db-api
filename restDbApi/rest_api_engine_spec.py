""" Optional use in superset
from superset.db_engine_specs.sqlite import SqliteEngineSpec


class RestApiEngineSpec(SqliteEngineSpec):
    # Engine for REST API
    engine = "rest"
    engine_name = "REST"
    allows_joins = True
    allows_subqueries = True

    default_driver = "apsw"
    sqlalchemy_uri_placeholder = "rest://"
    # https://preset.io/blog/building-database-connector/
"""
