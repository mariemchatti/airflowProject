import requests
import pymongo
import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def fetch_data_and_insert_into_mongodb():

    api_key = 'YOUR_API_KEY'
    symbol = 'AAPL'
    urlProfile = 'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={api_key}'
    responseProfile = requests.get(urlProfile)
    profile = responseProfile.json()
    urlRating = 'https://financialmodelingprep.com/api/v3/rating/{symbol}?apikey={api_key}'
    responseRating = requests.get(urlRating)
    rating = responseRating.json()

    data = {
        "rating": rating,
        "profile": profile,
        "timestamp": datetime.now()
    }

    client = pymongo.MongoClient("mongodb://my-mongodb:27017/")
    db = client["mydatabase"]
    collection = db["mycollection"]
    collection.insert_one(data)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 2, 22),
    'retries': 1,
    'retry_delay': datetime(minutes=1)
}

dag = DAG(
    dag_id='project',
    default_args=default_args,
    schedule_interval=datetime(minutes=1),
)

task = PythonOperator(
    task_id='taskid',
    python_callable=fetch_data_and_insert_into_mongodb,
    dag=dag,
)
