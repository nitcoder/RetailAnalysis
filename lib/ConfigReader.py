import configparser
from pyspark import SparkConf

# From configs directory we will create a python dictionary for both application and pyspark configs file
# loading the application configs in python dictionary and we will call by passing env
def get_app_config(env):
    config = configparser.ConfigParser() # Getting config object
    config.read("configs/application.conf") #Using config object reading application.conf file
    app_conf = {}
    # Adding key value pairs in application.conf in empty dictionary
    for (key, val) in config.items(env):
        app_conf[key] = val
    return app_conf
# loading the pyspark configs and creating a spark conf object
def get_pyspark_config(env):
    config = configparser.ConfigParser() #Getting config object
    config.read("configs/pyspark.conf") #Using config object reading pyspark.conf file
    #We want to  read above config  and create a Spark Config object so that we can pass the same when creating Spark Session
    # Also we are adding config items to SparkConf object
    pyspark_conf = SparkConf()
    for (key, val) in config.items(env):
        pyspark_conf.set(key, val)
    return pyspark_conf
