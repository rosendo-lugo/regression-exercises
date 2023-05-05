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
    # How to import a database from MySQL
    url = get_db_url('zillow')
    query = '''
    select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from properties_2017
    where propertylandusetypeid = 261
            '''
    filename = 'zillow.csv'
    df = check_file_exists(filename, query, url)
    
    # drop any nulls in the dataset
    df = df.dropna()
    
    # change the year to     
    df.yearbuilt = df.yearbuilt.astype(int)
    df.yearbuilt
    

    # rename columns
    df.columns
    df = df.rename(columns={'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'area',
       'taxvaluedollarcnt':'taxvalue', 'fips':'county'})
        
    # renamed the county codes inside county
    df.county = df.county.map({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    
    # Added a new column named tax rate
    df['tax_rate'] = round(df['taxamount']/df['taxvalue'],2)
    return df

# This will clean the data. 
def prep_zillow(df):
    '''
    This function will clean the the  dataset
    '''
    # drop any nulls in the dataset
    df = df.dropna()
    
    # change the year to     
    df.yearbuilt = df.yearbuilt.astype(int)
    df.yearbuilt


    return df