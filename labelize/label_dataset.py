
import os
import sys
import urllib3
import pandas as pd 

import snowflake.connector
from snowflake.connector import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
import getpass
import warnings
from snowflake.connector.pandas_tools import write_pandas
import fastparquet

import requests
import json
from bs4 import BeautifulSoup


# Set up the Snowflake connection by getting the username and password for the AU instance
#SF_USER = getpass.getpass(prompt = 'Please enter your Snowflake (AU) username:')
SF_USER = 'GUILLAUME'
SF_PASS = getpass.getpass(prompt = 'Please enter your Snowflake (AU) password:')
SF_ACCT = 'ia63414.australia-east.azure'

CURRENT_DIR = sys.path[0]

# Establish the connection to Snowflake to be utilised
SFC = create_engine(f'snowflake://{SF_USER}:{SF_PASS}@{SF_ACCT}/')



# Function to create the initial dataframe for drinks
def menu_items_dataframe():
    """
    Create a panda dataframe with item_name,item_id, menu_url,_category_item_type from dim_menu DB in Snowflake

    Input :
    None

    Output :
    panda dataframe
    """
    
    # The SQL query used on Snowflake:
    # FACT_SUBMISSION_LINE for Items and Variants (along with Venues, used for brands)
    sql_query_sub_line = '''
        SELECT       DISTINCT ITEM_NAME as name,ITEM_ID as item_id,MENU_URL as menu_url,category_name as category,item_type
                     FROM        analytics.bb.dim_menu
                     LIMIT 100000
    
    '''
    # Execute the query for Items on Snowflake
    df = pd.read_sql_query(sql_query_sub_line, con=SFC)
    df = df.dropna(subset = 'name')
    df['menu_url'] = df['menu_url'].fillna('other')
    return df

def get_description(df_menu_items):
    """
    Create a panda Dataframe of description

    Input :
    panda DataFrame with item_id and menu_url

    Output:
    panda DataFrame with item_id and their corresponding description
    
    """

    #Retrieve description
    df_menu_description = pd.DataFrame(columns = {'item_id':'','description':''})
    for url in df_menu_items['menu_url'].unique():
        if url!='other':
            json_ = requests.get(url).json() 
            try:
                df_items = pd.DataFrame(json_['items']).transpose().reset_index().rename({'index':'item_id'}, axis = 1)[['item_id','description']]
                df_menu_description = pd.concat([df_menu_description,df_items])
            except:
                print('error')
    
    df_menu_description = df_menu_description.merge(df_menu_items, on = ['item_id'],how = 'right')[['item_id','description']]
    # Remove empty descriptions
    df_menu_description = df_menu_description.dropna(subset = 'description')
    return df_menu_description


def create_label_dataset():
    """
    Create a dataset of label to identify name of an item, category and descriptions

    Input :
    None

    Output:
    - panda DataFrame with a column of texts and the other the corresponding label
    
    """
    # Get items from menu
    df_menu_items = menu_items_dataframe()
    #get description of some items (food only)
    df_menu_description = get_description(df_menu_items)
    # Concat the two dataframes and labelize data

    df_name = df_menu_items[['name']].rename(columns = {'name':'text'})
    df_name['label'] = 'name'

    # Concat the two dataframes and labelize data
    df_categories = df_menu_items[['category']].rename(columns = {'category':'text'})
    df_categories['label'] = 'category'

    df_descr = df_menu_description[['description']].rename(columns = {'description':'text'})
    df_descr['label'] = 'description'

    df_label_dataset = pd.concat([df_name,df_descr,df_categories])
    return df_label_dataset

def save_dataset(output_path):
    """
    Save the label dataset into a csv according the output_path
    
    Input :
    output_path : where the dataset should be saved
    
    Output:
    None
    """
    df_label_dataset = create_label_dataset()
    df_label_dataset.to_csv(output_path, index = False)


if __name__=="__main__":
    pass
    #save_dataset('./label_dataset.csv')
