import sys,logger
from lib import DataManipulation, DataReader, Utils
from pyspark.sql.functions import *

if __name__ == '__main__':
    # If we run without Specifying Environment it should fail
    if len(sys.argv) < 2:
        print("Please specify the environment")
        sys.exit(-1)

    # Whatever argument we pass will be stored as env value in variable job_run_env
    job_run_env = sys.argv[1]
    #print("Creating Spark Session")

    #Creating Spark session using Utils.py file
    spark = Utils.get_spark_session(job_run_env)
    logger= logger.Log4j(spark)  # Getting Log4j instance to get LOG LEVEL messages
    logger.info("Created Spark Session")

    orders_df = DataReader.read_orders(spark,job_run_env)
    orders_filtered = DataManipulation.filter_closed_orders(orders_df)
    customers_df = DataReader.read_customers(spark,job_run_env)
    joined_df =DataManipulation.join_orders_customers(orders_filtered,customers_df)
    aggregated_results = DataManipulation.count_orders_state(joined_df)
    aggregated_results.show()
    logger.warn("End of Main")
   # print("end of main")
# Since Logging level is set as INFO for our application in log4j properties file, both INFO and WARN messages will be displayed
# Running application using : C:\Users\Abhigya\.virtualenvs\RetailAnalysis-2m9CDxgO\Scripts\python C:\Users\Abhigya\PycharmProjects\RetailAnalysis\application_main.py LOCAL
#OUTPUT
#24/10/11 17:40:06 INFO retail_analysis: Created Spark Session
# 24/10/11 17:40:18 WARN retail_analysis: End of Main
# we can see date along with priority folllowed by application name and Message
# since we have specified pattern "%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n"

#Say we comment out this line from log4j properties file log4j.additivity.retail_analysis=false
# both child(application level) and parent(root level) message will be added and displayed
#OUTPUT:
# 24/10/11 17:56:07 INFO retail_analysis: Created Spark Session
# 24/10/11 17:56:07 INFO retail_analysis: Created Spark Session
# 24/10/11 17:56:14 WARN retail_analysis: End of Main
# 24/10/11 17:56:14 WARN retail_analysis: End of Main

# Changing logging level to WARN in log4j properties file  using log4j.logger.retail_analysis=WARN, console
#Only WARN message will be printed as INFO has lower priority than WARN
#OUTPUT:24/10/11 17:48:33 WARN retail_analysis: End of Main

#Similary we set this property to ERROR -->log4j.logger.retail_analysis=ERROR, console
#nothing will be printed as both WARN and INFO have lower priority level than ERROR

