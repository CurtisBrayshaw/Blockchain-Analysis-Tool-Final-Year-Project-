import sqlite3
from sqlite3 import Error
import pandas as pd
import os
path = os.getcwd()

def create_connection(db_file, data_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        data_file.to_sql("LeadSource", con=conn, if_exists='append', index_label='id')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def get_block_graph_data():
    db = sqlite3.connect(path + '\\Database\\blocks.db')
    df = pd.read_sql_query("Select * from LeadSource", db)
    return df


def get_tx_data():
    db = sqlite3.connect(path + '\\Database\\transactions.db')
    df = pd.read_sql_query("Select * from LeadSource", db)
    return df


def get_tx_graph_data():
    db = sqlite3.connect(path + '\\Database\\inputs.db')
    df = pd.read_sql_query("Select * from LeadSource", db)
    df2 = get_tx_data()
    return df


def get_address_graph_data():
    db = sqlite3.connect(path + '\\Database\\address.db')
    df = pd.read_sql_query("Select * from LeadSource", db)
    return df


def deleteDB(id):
    if id == 1:
        if os.path.exists(path + '\\Database\\blocks.db'):
            os.remove(path + '\\Database\\blocks.db')
        else:
            print("File does not exist")
    if id == 2:
        if os.path.exists(path + '\\Database\\transactions.db'):
            os.remove(path + '\\Database\\transactions.db')
        if os.path.exists(path + '\\Database\\inputs.db'):
            os.remove(path + '\\Database\\inputs.db')
        else:
            print("File does not exist")
    if id == 3:
        if os.path.exists(path + '\\Database\\address.db'):
            os.remove(path + '\\Database\\address.db')
        else:
            print("File does not exist")
    else:
        print("Deleted")