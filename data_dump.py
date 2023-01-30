import pandas as pd
import pymongo
import json
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")
Data_base = 'aps'
Colleciton_name = 'sensor'
Datafile_path = '/config/workspace/aps_failure_training_set1.csv'
if __name__ == '__main__':
    df = pd.read_csv(Datafile_path)
    print(f'rows and columns:{df.shape}')
    df.reset_index(drop = True ,inplace = True)
    json_records = list(json.loads(df.T.to_json()).values())
    print(json_records[1])
    client[Data_base][Colleciton_name].insert_many(json_records) .
