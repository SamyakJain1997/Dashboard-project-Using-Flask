import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sqlalchemy.types import *
import os,sys
import random

host= "localhost"
default_db_name = "aisplcdb"
user = "aisplcdb"
passwd = "Aisplcdb_987"

def mysql_connection(dbname):
    try:
        conn = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{dbname}')
        # print("Connection Sucessfull!")
        return conn
    except Exception as err:
        print(err)

def db_connection_global():
    try:
        conn = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}')
        print("Connection Sucessfull!")
        return conn
    except Exception as err:
        print(err)

def df_to_sql(df,db,table,if_exists): #in_exists - replace or append
    try:
        engine=mysql_connection(db)
        df.to_sql(table, engine,if_exists=if_exists,chunksize=10000, index=False)
        print("Data Updated Successfully!!")
    except Exception as err:
        print(err)


def data_from_source_to_df(filepath):
    try:
        filename = (os.path.basename(filepath))
        ext = os.path.splitext(filename)[1]
        if ext == '.csv':
            df = pd.read_csv(filepath,encoding="iso-8859-1",low_memory=False)
        elif ext == '.xlsx':
            df = pd.read_excel(filepath, sheet_name="Sheet1")
        else:
            print(f"Not a CSV/XLSX File !!! Ignoreing {filename}")
            pass
        df.insert(1, 'data_source', filename)
        return df
    except Exception as err:
        print("Check file type of sheet name , incase of xlsx default it will take 'Sheet1' ")
        print(err)

def sql_check_id_exists(db,table,key,id,return_key):
    
    try:
        engine=mysql_connection(db)
        connection = engine.connect()
        query= f"SELECT {return_key} FROM {table} WHERE {key} = '{id}';"
        # print(query)
        values = connection.execute(query).fetchone()
        if values is None:
            return False
        else:
            return values[0]
    except Exception as err:
        print(err)


def genarate_aispl_id(program_type):
    fixed_digits = 8
    random_num = (random.randrange(167000, 99999999, fixed_digits))
    if program_type == "VIPCLP":
        id = str(random_num).rjust(9,'0')  
        id = "AISPL"+"1"+id
    else:
        id = str(random_num).rjust(9,'0')  
        id = "AISPL"+"2"+id
    return id

def get_df_from_sql_table(db,query):
    engine=mysql_connection(db)
    connection = engine.connect()
    value_list = connection.execute(query).fetchall()
    columns = connection.execute(query).keys()
    resp_list=[]
    if len(value_list) != 0:
        for values in value_list:
            vals = (list(values))
            keys = (list(columns))
            ref_dict = {k:v for k,v in zip(keys,vals)}
            resp_list.append(ref_dict)
    df = pd.DataFrame(resp_list)
    return df


def fix_columns_name(df):
    df.columns = df.columns.str.replace('[^a-zA-Z0-9]',' ')
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ",'_')
    df.columns = df.columns.str.lower()
    return df


def df_preprocessing(df):
    df.reset_index(drop=True, inplace=True)
    df = df.drop_duplicates()
    final_df = df.dropna(axis=1, how='all')
    final_df.index = np.arange(1, len(df) + 1)
    return final_df

def sql_table_to_df(db,table):
    conn = mysql_connection(db)
    sql_query_df = pd.read_sql_query (f'''SELECT*FROM {table}''', conn)
    return sql_query_df


def remove_duplicate_sql_table(db,table):
    try:
        sql_data_df = sql_table_to_df(db,table)
        print(sql_data_df.shape)
        sql_data_df = sql_data_df.drop_duplicates()
        print(sql_data_df.shape)
        df_to_sql(sql_data_df,db,table,"replace")
        status = True
    except Exception as e:
        print(e)

def get_new_adobe_aispl_id(program_type,db,table,key,id,return_key):
    aispl_id_check = True
    while aispl_id_check == True:
        random_aispl_id = genarate_aispl_id(program_type)
        aispl_id_check = sql_check_id_exists(db,table,key,id,return_key)
    return random_aispl_id
 

def adobe_data_upload_update(df,db,table):
    if 'aispl_id' not in df:
        df['aispl_id'] = ""
    for index, row in df.iterrows():
        if (df.at[index,"aispl_id"] == ""):
            key = "membership_number"
            id = df.at[index,"membership_number"]
            return_key = "aispl_id"
            if id == "":
                key = "end_user_name"
                id = df.at[index,"end_user_name"]
            resp_ = sql_check_id_exists(db,table,key,id,return_key)
            if resp_ is not None:
                if resp_ != False:
                    aispl_id = resp_ 
                else:
                    resp_ = get_new_adobe_aispl_id(df.at[index,"program_type"],db,table,key,id,return_key)
                    aispl_id = resp_
        else:
            aispl_id = df.at[index,"aispl_id"]
        df.at[index,"aispl_id"] = aispl_id
    return df

def get_adobe_db_data_on_id(updated_df):
    id_tup = tuple(list(updated_df['aispl_id'].unique()))
    query = f"SELECT * FROM adobe_db_test WHERE aispl_id IN {id_tup};"
    db_df = get_df_from_sql_table("aisplcdb",query)
    return db_df

def update_adobe_data_to_sql(file,db,table):
    try:
        print("Adobe_data_update_started!")
        df = data_from_source_to_df(file)
        # df = pd.read_csv(file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = fix_columns_name(df)
        df= df_preprocessing(df)
        updated_df= adobe_data_upload_update(df,db,table)
        db_df = get_adobe_db_data_on_id(updated_df)
        print("db_df",db_df.shape)
        updated_df = updated_df.astype('str')
        print("updated_df",updated_df.shape)
        db_df = db_df.astype('str')
        final_df = pd.concat([updated_df, db_df]).drop_duplicates(keep=False).reset_index(drop=True)
        print(f"Number of the data going to update!{final_df.shape[0]}")
        final_df = final_df.astype({'current_anniversary_date': 'datetime64[ns]',"start_date":"datetime64[ns]","membership_expiration_date":"datetime64[ns]"},errors='ignore')
        print(final_df.head(5))
        remove_duplicate_sql_table(db,table)
        df_to_sql(final_df,db,table,"append")
        print("Adobe data updated to database!")
        return "data updated sucessfully!!"
    except Exception as e:
        # print(e)
        return f"Error:data updated failed,{e}"

if __name__ == "__main__":
    file = "/root/AISPL/centraldbdata/Centralized Data/Adobe/adobe_ptech_mod/final_data/Adobe 21-22.csv"
    update_adobe_data_to_sql(file,'aisplcdb_dev','adobe_cdb_test')
