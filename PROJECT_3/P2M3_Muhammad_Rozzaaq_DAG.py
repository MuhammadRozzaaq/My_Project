import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import DAG


def load_postgre():
    '''
    fungsi ini untuk menarik data ke SQL. query di sertakan dalam file berbeda 
    '''
    conn_string="dbname='postgres' host='postgres' user='airflow' password='airflow' port='5432'"
    conn=db.connect(conn_string)

    df=pd.read_sql("select * from table_m3", conn)
    df.to_csv('P2M3_Muhammad_Rozzaaq_data_raw.csv')
    
def data_cleaning():
    '''
    fungsi ini akan melakukan data cleaning. seperti drop duplicated, handling missing value dan mengubah nama kolom
    '''
    df = pd.read_csv('P2M3_Muhammad_Rozzaaq_data_raw.csv')
    # drop duplicate
    df.drop_duplicates()
     
    # Menghandle missing value
    # Daftar kolom numerik dan kategorikal
    numeric = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
    kategoric = ['Dependents', 'Loan_ID', 'Gender', 'Married', 'Education', 'Self_Employed', 'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Loan_Status']
    
    # Mengisi missing value di kolom Numeric dengan mean
    df[numeric] = df[numeric].fillna(df[numeric].mean())

    # Mengisi missing value di kolom Categoric dengan mode
    df[kategoric] = df[kategoric].apply(lambda x: x.fillna(x.mode()[0]))

    # Mengubah nama kolum menjadi lowercase
    df.columns = df.columns.str.lower()

    df.to_csv("P2M3_Muhammad_Rozzaaq_data_clean.csv", index=False) 

def send_elastic():
    '''
    fungsi ini akan mengirimkan data hasil cleaning ke elastic search. nantinya akan dilakukan visualisasi ada kibana
    '''
    es = Elasticsearch("http://elasticsearch:9200")
    df=pd.read_csv("P2M3_Muhammad_Rozzaaq_data_raw.csv")
    for i,r in df.iterrows():
        doc=r.to_dict()
        res = es.index(index="milestone_3",id=i, doc_type="doc", body=doc)
        print(res)
        
default_args= {
    'owner': 'ojan',
    'start_date': datetime(2024, 8, 12, 16, 20, 0) - timedelta(hours=8),
    'retries': 1,
    'retry_delay': timedelta(seconds=1)
    }

with DAG('Airflow_Milestone',
    default_args=default_args, 
    schedule_interval='30 6 * * *',
    catchup=False) as dag:
    fetching_data = PythonOperator(
        task_id='fetching_data',
        python_callable=load_postgre)
    cleaning = PythonOperator(
        task_id='cleaning_data',
        python_callable=data_cleaning)
    Elastic = PythonOperator(
        task_id='Elastic',
        python_callable=send_elastic)
        

fetching_data >> cleaning >> Elastic
    

        
