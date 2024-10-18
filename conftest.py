#Fixtures are defined using the “@pytest.fixture” decorator. And they are especially useful for reusable setup code.
# It provides a convenient way to set upa Spark environment for testing without having to repeat the setup code in each test.


# Ideally fixtures should be  written in a separate file like “conftest.py” and no need to specify where.
# it is written as pytest framework will directly use fixtures present in this file.
import pytest
from lib.Utils import get_spark_session

# This fixture creates a SparkSession object for testing and returns it to the test functions that request it.
# When Test functions run they will call this Fixture to get Spark Session
# First 2 lines of code till yield part will run as part of Setup to get the resources ,
# Then  Unit test cases will run and
# Finally remaining part of code will run where we stop Spark Session to release resources

@pytest.fixture
def spark_session():
    "Creates Spark session"
    spark_session = get_spark_session("LOCAL")
    yield  spark_session
    spark_session.stop()

@pytest.fixture
def expected_results(spark_session):
    "Reads Expected Results file and returns a Dataframe to compare with Calculated value in our Unit test case"
    results_schema="state string, count int"
    return  spark_session.read.format("csv").schema(results_schema).load("data/test_result/state_aggregate.csv")

# python -m pytest --fixtures --> Gives us a list of Fixtures which includes System defined fixtures and fixtures written by us in conftest.py.
#  C:\Users\Abhigya\.virtualenvs\RetailAnalysis-2m9CDxgO\Scripts\python.exe -m pytest -m latest -v
# collected 6 items / 5 deselected / 1 selected
