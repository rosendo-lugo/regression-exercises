import pandas as pd 
from env import get_db_url
import os

def check_file_exists(fn, query, url):
    """
    check if file exists in my local directory, if not, pull from sql db
    return dataframe
    """
    if os.path.isfile(fn):
        print('csv file found and loaded')
        return pd.read_csv(fn, index_col=0)
    else: 
        print('creating df and exporting csv')
        df = pd.read_sql(query, url)
        df.to_csv(fn)
        return df


def get_zillow_data():
    url = get_db_url('zillow_db')
    query = '''
    select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from properties_2017
    where propertylandusetypeid = 261
            '''
    filename = 'zillow.csv'
    df = check_file_exists(filename, query, url)
    return df

