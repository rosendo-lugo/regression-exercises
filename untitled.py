import pandas as pd

def get_zillow_data():
    # How to import a database from MySQL
    url = get_db_url('zillow')
    query = '''
    select p.bedroomcnt, p.bathroomcnt, p.calculatedfinishedsquarefeet, p.taxvaluedollarcnt, p.yearbuilt, p.fips, p2.transactiondate
    from properties_2017 p
        join predictions_2017 p2 using (parcelid)
    where p.propertylandusetypeid = 261
    order by p2.transactiondate
            '''
    filename = 'zillow.csv'
    df = check_file_exists(filename, query, url)
    
    # rename columns
    df.columns = ['bedrooms', 'bathrooms', 'area', 'property_value', 'yearbuilt', 'county', 'transaction_date']
    
    # Look at properties less than 25,000 sqft
    df = df[df.area < 25000]
    
    # Property value reduce to 95% total
    df = df[df.property_value < df.property_value.quantile(0.95)]
    
    # drop any nulls in the dataset
    df = df.dropna()
    
    # change the dtype from float to int  
    df[['area', 'yearbuilt', 'transaction_date']] = df[['area', 'yearbuilt', 'transaction_date']].astype(int)
    
    # rename the county codes inside county
    df['county'] = df['county'].map({6037: 'LA', 6059: 'Orange', 6111: 'Ventura'})
    
    # write the results to a CSV file
    df.to_csv('df_prep.csv', index=False)

    # read the CSV file into a Pandas dataframe
    prep_df = pd.read_csv('df_prep.csv')
    
    return df, prep_df


def get_zillow_data():
    # How to import a database from MySQL
    url = get_db_url('zillow')
    query = '''
    select p.bedroomcnt, p.bathroomcnt, p.calculatedfinishedsquarefeet, p.taxvaluedollarcnt, p.yearbuilt, p.fips, p2.transactiondate
    from properties_2017 p
        join predictions_2017 p2 using (parcelid)
    where p.propertylandusetypeid = 261
    order by p2.transactiondate
            '''
    filename = 'zillow.csv'
    df = check_file_exists(filename, query, url)
    
    # rename columns
    df.columns
    df = df.rename(columns={'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'area',
       'taxvaluedollarcnt':'property_value', 'fips':'county', 'transactiondate':'transaction_date'})
    
    # Look at properties lessthan 25,000 sqft
    df.area = df.area[df.area < 25_000].copy()
    
    # Property value reduce to 95% total
    df.property_value = df.property_value[df.property_value < df.property_value.quantile(.95)].copy()
    
        
    # drop any nulls in the dataset
    df = df.dropna()
    
    # change the dtype from float to int  
    df.area = df.area.astype(int).copy()
    df.county = df.county.astype(int).copy()
    df.yearbuilt = df.yearbuilt.astype(int).copy()
    df.transaction_date = df.transaction_date.astype(int).copy()
    
    # renamed the county codes inside countyß
    df.county = df.county.map({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    
    # write the results to a CSV file
    df.to_csv('df_prep.csv', index=False)

    # read the CSV file into a Pandas dataframe
    prep_df = pd.read_csv('df_prep.csv')
    
    return df, prep_df


    
# ----------------------------------------------------------------------------------
def get_zillow_data():
    # How to import a database from MySQL
    url = get_db_url('zillow')
    query = '''
    select p.parcelid, p.bedroomcnt, p.bathroomcnt, p.calculatedfinishedsquarefeet, p.taxvaluedollarcnt, p.yearbuilt, p.fips, p2.transactiondate
    from properties_2017 p
        join predictions_2017 p2 using (parcelid)
    where p.propertylandusetypeid = 261 and 279
            '''
    filename = 'zillow.csv'
    df = check_file_exists(filename, query, url)
    
    # filter to just 2017 transactions
    df = df[df['transactiondate'].str.startswith("2017", na=False)]
    
    # split transaction date to year, month, and day
    df_split = df['transactiondate'].str.split(pat='-', expand=True).add_prefix('transaction_')
    df = pd.concat([df.iloc[:, :40], df_split, df.iloc[:, 40:]], axis=1)
    
    # Drop duplicate rows in column: 'parcelid', keeping max transaction date
    df = df.drop_duplicates(subset=['parcelid'])
    
    # rename columns
    df.columns
    df = df.rename(columns={'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms',
                            'calculatedfinishedsquarefeet':'area','taxvaluedollarcnt':'property_value',
                            'fips':'county','transaction_0':'transaction_year',
                            'transaction_1':'transaction_month','transaction_2':'transaction_day'})
    
    # total outliers removed are 6029 out of 52442
    # # Look at properties less than 1.5 and over 5.5 bedrooms (Outliers were removed)
    # df = df[~(df['bedrooms'] < 1.5) & ~(df['bedrooms'] > 5.5)]

    # Look at properties less than .5 and over 4.5 bathrooms (Outliers were removed)
    df = df[~(df['bathrooms'] < .5) & ~(df['bathrooms'] > 4.5)]

    # Look at properties less than 1906.5 and over 2022.5 years (Outliers were removed)
    df = df[~(df['yearbuilt'] < 1906.5) & ~(df['yearbuilt'] > 2022.5)]

    # Look at properties less than -289.0 and over 3863.0 area (Outliers were removed)
    df = df[~(df['area'] < -289.0) & ~(df['area'] > 3863.0)]

    # Look at properties less than -444576.5 and over 1257627.5 property value (Outliers were removed)
    df = df[~(df['property_value'] < -444576.5) &  ~(df['property_value'] > 1257627.5)]
    
    # replace missing values with "0"
    df = df.fillna({'bedrooms':0,'bathrooms':0,'area':0,'property_value':0,'county':0})
    
    # drop any nulls in the dataset
    df = df.dropna()
    
    # drop all duplicates
    df = df.drop_duplicates(subset=['parcelid'])
    
    # change the dtype from float to int  
    df[['bedrooms','area','property_value','yearbuilt','transaction_month','transaction_day']] = df[['bedrooms','area','property_value','yearbuilt','transaction_month','transaction_day']].astype(int)
    
    # rename the county codes inside county
    df['county'] = df['county'].map({6037: 'LA', 6059: 'Orange', 6111: 'Ventura'})
    
    # get dummies and concat to the dataframe
    dummy_tips = pd.get_dummies(df[['county']], dummy_na=False, drop_first=[True, True])
    df = pd.concat([df, dummy_tips], axis=1)
    
    # dropping these columns for right now until I find a use for them
    df = df.drop(columns =['parcelid','transactiondate','transaction_year','transaction_month','transaction_day'])
    
    # Define the desired column order
    new_column_order = ['bedrooms','bathrooms','area','yearbuilt','county','county_Orange','county_Ventura','property_value',]

    # Reindex the DataFrame with the new column order
    df = df.reindex(columns=new_column_order)

    # write the results to a CSV file
    df.to_csv('df_prep.csv', index=False)

    # read the CSV file into a Pandas dataframe
    prep_df = pd.read_csv('df_prep.csv')
    
    return df, prep_df