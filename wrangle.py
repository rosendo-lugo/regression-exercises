import pandas as pd 
from env import get_db_url
import os

# Stats
from scipy import stats
import sklearn.preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import QuantileTransformer



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
    
    # rename columns
    df.columns
    df = df.rename(columns={'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'area',
       'taxvaluedollarcnt':'taxvalue', 'fips':'county'})
    
    # change the dtype from float to int  
    make_ints = ['bedrooms','area','taxvalue','yearbuilt','county']
    for col in make_ints:
        df[col] = df[col].astype(int)
        
    # renamed the county codes inside countyß
    df.county = df.county.map({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    
    # Added a new column named tax rate
    df['tax_rate'] = round(df['taxamount']/df['taxvalue'],2)
    
    df = df [df.area < 25_000].copy()
    df = df[df.taxvalue < df.taxvalue.quantile(.95)].copy()
    
    return df

# ----------------------------------------------------------------------------------
def get_zillow_split(df):
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.25, random_state=123)
    
    return train, validate, test


# ----------------------------------------------------------------------------------

def get_minmax_train_scaler(X_train, X_validate):
    
    columns=['bedrooms', 'bathrooms','area','yearbuilt','taxamount','tax_rate']
    X_tr_mm_scaler = X_train.copy()
    X_v_mm_scaler = X_validate.copy()
    
    # Create a MinMaxScaler object
    mm_scaler = MinMaxScaler()

    # Fit the scaler to the training data and transform it
    X_tr_mm_scaler[columns] = mm_scaler.fit_transform(X_train[columns])
    X_tr_mm_scaler = pd.DataFrame(X_tr_mm_scaler)
    
    #using our scaler on validate
    X_v_mm_scaler[columns] = mm_scaler.transform(X_validate[columns])
    X_v_mm_scaler = pd.DataFrame(X_v_mm_scaler)
    
    # inverse transform
    X_tr_mm_inv = mm_scaler.inverse_transform(X_tr_mm_scaler[columns])
    X_tr_mm_inv = pd.DataFrame(X_tr_mm_inv, columns=columns)

    # add the county column to X_tr_mm_inv
    X_tr_mm_inv = pd.concat([X_tr_mm_inv, X_train[['county']].reset_index(drop=True)], axis=1)
    
    return X_tr_mm_scaler, X_v_mm_scaler, X_tr_mm_inv

# ----------------------------------------------------------------------------------
def get_std_train_scaler(X_train, X_validate):
    
    columns=['bedrooms', 'bathrooms','area','yearbuilt','taxamount','tax_rate']
    X_tr_std_scaler = X_train.copy()
    X_v_std_scaler = X_validate.copy()
    
    # Create a MinMaxScaler object
    std_scaler = StandardScaler()

    # Fit the scaler to the training data and transform it
    X_tr_std_scaler[columns] = std_scaler.fit_transform(X_train[columns])
    
    #using our scaler on validate
    X_v_std_scaler[columns] = std_scaler.transform(X_validate[columns])
    
    return X_tr_std_scaler, X_v_std_scaler

# ----------------------------------------------------------------------------------

def get_robust_train_scaler(X_train, X_validate):
     
    columns=['bedrooms', 'bathrooms','area','yearbuilt','taxamount','tax_rate']
    X_tr_rbs_scaler = X_train.copy()
    X_v_rbs_scaler = X_validate.copy()
    
    # Create a MinMaxScaler object
    rbs_scaler = RobustScaler()

    # Fit the scaler to the training data and transform it
    X_tr_rbs_scaler[columns] = rbs_scaler.fit_transform(X_train[columns])
    
    #using our scaler on validate
    X_v_rbs_scaler[columns] = rbs_scaler.transform(X_validate[columns])
    
    return X_tr_rbs_scaler, X_v_rbs_scaler

# ----------------------------------------------------------------------------------
def get_quant_normal(X_train):
    # Columns
    columns=['bedrooms', 'bathrooms','area','yearbuilt','taxamount','tax_rate']
    
    # Quantile transform with output distribution "normal"
    quant_norm = QuantileTransformer(output_distribution='normal')
    X_tr_quant_norm = pd.DataFrame(quant_norm.fit_transform(X_train[columns]),columns=columns)
    
    # Quantile trainsform by it self
    quant = QuantileTransformer()
    X_tr_quant = pd.DataFrame(quant.fit_transform(X_train[columns]),columns=columns)
    
    return quant_norm, X_tr_quant_norm, quant, X_tr_quant