from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator



with DAG(
    dag_id='test',
    start_date=datetime(2022, 10, 5),
    schedule_interval="@once",
    catchup=False,
) as dag:
    task1=PostgresOperator( 
        task_id='create_pet_table',
        postgres_conn_id='postgres_db',
        sql="sql/test.sql",
    )
    task1
    
