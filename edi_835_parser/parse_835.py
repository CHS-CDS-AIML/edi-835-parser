from edi_835_parser import parse
import os
import pandas as pd
from appeals.utils.bq import Update_BQ_Table
from appeals.schemas import edi_schema
from datetime import datetime

def parse_daily_files():
    """
    read 835 files from a directory called 835_files
    and load into dataframe
    """
   df = pd.DataFrame()
   today = str(datetime.now().date())
   directory = f"../835_files/today"
   for fn in os.listdir(directory):
       print(fn)
       try:
           ts = parse(f"{directory}/{fn}")
           try:
               fn_df = ts.to_dataframe()
           except:
               continue
           df = pd.concat([df, fn_df])
       except (AssertionError, IndexError):
           pass

    df.to_csv("edi_parsed_org.csv")#, header=False)

    return df

def write_data():
    df = pd.read_csv("edi_parsed_org.csv")
    df.drop(columns=["Unnamed: 0"], inplace=True)
    df["insert_ts"] = str(datetime.now())
    table_id = "prj-cdw-p-aiml-001-0b36.Appeals.835_data"
    schema = edi_schema()
    list_to_remove = list()
    for col in df.columns:
        #if df[col].dtype == object:
        df[col] = df[col].astype(str)
        if "_6" in col:
            list_to_remove.append(col)
    df.drop(columns=list_to_remove, inplace=True)
    Update_BQ_Table(table_id, df, schema=schema)
