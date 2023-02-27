from superset.db_engine_specs.sqlite import SqliteEngineSpec


class GraphQLEngineSpec(SqliteEngineSpec):
    """Engine for GraphQL API tables"""

    engine = "restboii"
    engine_name = "REST"
    allows_joins = True
    allows_subqueries = True

    default_driver = "apsw"
    sqlalchemy_uri_placeholder = "rest://"
