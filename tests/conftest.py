from typing import Generator

import pytest
from sqlalchemy.engine import Connection
from sqlalchemy import create_engine

GET_SQL_ALCHEMY_URI = 'rest://api.covidtracking.com?ishttps=1'
POST_SQL_ALCHEMY_URI = 'rest://some.api.com?ishttps=0'

@pytest.fixture
def simple_url() -> str:
    return GET_SQL_ALCHEMY_URI


@pytest.fixture
def post_sql_uri():
    return POST_SQL_ALCHEMY_URI


@pytest.fixture
def covid_data_connection(simple_url: str) -> Generator[Connection, None, None]:
    engine = create_engine(simple_url)
    with engine.connect() as connection:
        yield connection


@pytest.fixture
def post_data_connection(post_sql_uri: str) -> Generator[Connection, None, None]:
    engine = create_engine(post_sql_uri)
    with engine.connect() as connection:
        yield connection
