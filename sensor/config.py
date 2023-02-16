import pymongo
import pandas as pd 
import numpy as np 
import os
from dataclasses import dataclass


@dataclass
class Environment_variable:
    mongodb_url = os.getenv("MONGO_DB_URL")

env_var = Environment_variable()
mongo_clent = pymongo.MongoClient(env_var.mongodb_url)

