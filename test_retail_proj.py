# The unit test cases typically start with the prefix "test_". This naming
# convention helps Pytest automatically discover and execute the test
# cases when you run your test suite.
import pytest
from lib.Utils import get_spark_session
from lib.DataReader import read_customers,read_orders
from lib.DataManipulation import filter_closed_orders,count_orders_state,filter_orders_generic
from lib.ConfigReader import  get_app_config


# Whatever functions we write should start with "test_"  So it can be identified as Unit Test function
# Below we have written 4 unit test cases
def test_read_customers_df(spark_session):
    cust_df=read_customers(spark_session,"LOCAL")
    assert cust_df.count() == 12435 #Assertions are used within the test methods to compare the expected output of the function with the actual output


def test_read_orders_df(spark_session):
    orders_df=read_orders(spark_session,"LOCAL")
    assert orders_df.count() == 68884

# To run the test run the code:“python -m pytest”.
# As the python file is present in the virtual environment complete path of python.exe file
# so we will mention so the command will become: <virtual-env-path>/scripts/python -m pytest
# To get more details add -v (verbose) at the end of the command: C:\Users\Abhigya\.virtualenvs\RetailAnalysis-2m9CDxgO\Scripts\python -m pytest -v
# We will see details like test file name, names of function tested along with Test result and progress%
# test_retail_proj.py::test_read_customers_df PASSED      (50%)                                                                                                                                                                         [ 50%]
# test_retail_proj.py::test_read_orders_df PASSED          (100%)

@pytest.mark.transformation
def test_filtered_orders_df(spark_session):
    closed_orders_df=filter_closed_orders(read_orders(spark_session,"LOCAL"))
    assert closed_orders_df.count() == 7556

@pytest.mark.skip("Work in Progress")
def test_read_app_config():
    config_dict=get_app_config("LOCAL") # config_dict --> Will be a Dictionary
    assert config_dict["orders.file.path"] == "data/orders.csv"

# On testing we will see
# test_retail_proj.py::test_read_customers_df PASSED       (25%)
# test_retail_proj.py::test_read_orders_df PASSED          (50%)
# test_retail_proj.py::test_filtered_orders_df PASSED      (75%)
#  test_retail_proj.py::test_read_app_config PASSED        (100%)

# Testing count_orders_state where we calculate statewise count with the file: state_aggregate.csv
# This will take 2 fixtures: spark_session,expected_results
@pytest.mark.transformation
def test_count_orders_state(spark_session,expected_results):
    cust_df=read_customers(spark_session,"LOCAL")
    actual_results=count_orders_state(cust_df) # THis will be a Dataframe since we used Count with GroupBy
    assert actual_results.collect() == expected_results.collect() # collect returns Dataframe contents in form of list and we compare both lists


#Testing CLOSED order status count
@pytest.mark.skip
def test_check_closed_orders_count(spark_session):
    orders_df=read_orders(spark_session,"LOCAL")
    closed_orders_count=filter_orders_generic(orders_df,'CLOSED').count()
    assert closed_orders_count == 7556

#Testing PENDING_PAYMENT order status count
@pytest.mark.skip
def test_check_pending_pay_orders_count(spark_session):
    orders_df=read_orders(spark_session,"LOCAL")
    pending_pay_orders_count=filter_orders_generic(orders_df,'PENDING_PAYMENT').count()
    assert pending_pay_orders_count == 15030

#Testing COMPLETE order status count
@pytest.mark.skip
def test_check_complete_orders_count(spark_session):
    orders_df=read_orders(spark_session,"LOCAL")
    complete_orders_count=filter_orders_generic(orders_df,'COMPLETE').count()
    assert complete_orders_count == 22900

# Instead of writing 3 separate test cases , we can parameterize our test function
# Parameterizing test function allows us to write a more generic test function that can handle different scenarios by passing parameters.
# By doing so, we can avoidduplicating code for similar test cases and make our test suite more maintainable.
#All 3 parameters will be passed sequentially to test function
@pytest.mark.latest
@pytest.mark.parametrize(
    "status,count" ,
    [
        ("CLOSED",7556),("PENDING_PAYMENT",15031),('COMPLETE',22900)
    ]
)
def test_check_orders_count(spark_session,status,count):
    orders_df=read_orders(spark_session,"LOCAL")
    filtered_count=filter_orders_generic(orders_df,status).count()
    assert  filtered_count == count

#Testing above parametrized test function: C:\Users\Abhigya\.virtualenvs\RetailAnalysis-2m9CDxgO\Scripts\python.exe -m pytest -m latest -v
# OUTPUT
# collected 11 items / 8 deselected / 3 selected
# test_retail_proj.py::test_check_orders_count[CLOSED-7556] PASSED                      [ 33%]
# test_retail_proj.py::test_check_orders_count[PENDING_PAYMENT-15030] PASSED            [ 66%]
# test_retail_proj.py::test_check_orders_count[COMPLETE-22900] PASSED                   [ 100%]

# Changing count to 15031 for PENDING_PAYMENT usecase
# OUTPUT
# collected 11 items / 8 deselected / 3 selected
# test_retail_proj.py::test_check_orders_count[CLOSED-7556] PASSED                      [ 33%]
# test_retail_proj.py::test_check_orders_count[PENDING_PAYMENT-15031] FAILED            [ 66%]
# test_retail_proj.py::test_check_orders_count[COMPLETE-22900] PASSED                   [ 100%]
