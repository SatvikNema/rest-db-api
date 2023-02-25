

from setuptools import find_packages, setup

setup(
    name="restDbApi",
    version="1.0.0",
    description="rest db api designed to be used with apache superset",
    author="Satvik Nema",
    author_email="satviknema@gmail.com",
    entry_points={
        "shillelagh.adapter": [
            "myrestadapter = restDbApi.rest_api_adapter:RestAdapter"
        ],
        "sqlalchemy.dialects": ["rest = restDbApi.rest_api_dialect:RestApiDialect"],
    },
    packages=find_packages()
)
