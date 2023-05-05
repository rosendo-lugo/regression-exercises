# Standard ds libraries
import pandas as pd

# Import splitting function
from sklearn.model_selection import train_test_split


#-------------------------

def split_function(df, target_varible, seed=123):
    train_validate, test = train_test_split(df,
                                   random_state=seed,
                                   test_size=0.2,
                                   stratify= df[target_varible])
    
    train, validate = train_test_split(train_validate,
                                   random_state=seed,
                                   test_size=0.25, 
                                   stratify= train_validate[target_varible])
    return train, validate, test



#-------------------------

# This will clean the data. 
def prep_telco(telco_df):
    '''
    This function will clean the the telco dataset
    '''
    telco_df = telco_df.drop(columns =['contract_type_id', 'internet_service_type_id', 'payment_type_id'])
    
    dummy_telco = pd.get_dummies(telco_df[['gender',
                                             'partner',
                                             'dependents',
                                             'phone_service',
                                             'multiple_lines',
                                             'online_security',
                                             'online_backup',
                                             'device_protection',
                                             'tech_support',
                                             'streaming_tv',
                                             'streaming_movies',
                                             'paperless_billing',
                                             'churn',
                                             'contract_type',
                                             'internet_service_type',
                                             'payment_type']], dummy_na=False, drop_first=[True, True])
    telco_df = pd.concat([telco_df, dummy_telco], axis=1)
    telco_df.total_charges = telco_df.total_charges.str.replace(' ', '0').astype(float)
    return telco_df

#-------------------------


# This will clean the data. 
def prep_titanic(titanic_df):
    '''
    This function will clean the the titanic dataset
    '''
    # Drop any duplicates values
    titanic_df = titanic_df.drop_duplicates()

    # Drops columns that are already represented by other columns
    titanic_df = titanic_df.drop(columns =['embark_town','age','class','deck'])
    
    # Uses one-hot encoding to create dummies of string columns for future modeling 
    dummy_titanic = pd.get_dummies(data=titanic_df[['sex','embarked']], dummy_na=False, drop_first=True)
    titanic_df = pd.concat([titanic_df, dummy_titanic], axis=1)

    return titanic_df


#-------------------------


# This will clean the data. 
def prep_titanic_dropna(titanic_df):
    ''' 
    This function will clean the the titanic dataset
    '''
    # Drop any duplicates values
    titanic_df = titanic_df.drop_duplicates()
    
    titanic_df['embarked'] = titanic_df.embarked.fillna(value='S')

    # Drops columns that are already represented by other columns
    titanic_df = titanic_df.drop(columns =['embark_town','class','deck'])
    
    # The dropna() function removes all rows with at least one missing value.
    titanic_df = titanic_df.dropna()
    
    # Uses one-hot encoding to create dummies of string columns for future modeling 
    dummy_titanic = pd.get_dummies(data=titanic_df[['sex','embarked']], dummy_na=False, drop_first=True)
    titanic_df = pd.concat([titanic_df, dummy_titanic], axis=1)

    return titanic_df
#-------------------------

def prep_iris(iris_df):
    '''
    This function prepares the iris data by dropping the species_id and measurement_id.
    It also renames the species_name column to species and creates a dummies for the
    column species and at the end concats the dummy species columns with the iris database
    '''
    iris_df = iris_df.drop(columns = ['species_id', 'measurement_id'])
    iris_df = iris_df.rename(columns={'species_name': 'species'})
    dummy_iris = pd.get_dummies(iris_df.species, drop_first=True)
    iris_df = pd.concat([iris_df, dummy_iris], axis=1)
    return iris_df









