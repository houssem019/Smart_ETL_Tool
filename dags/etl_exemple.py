import time
from datetime import datetime
import json
from textwrap import dedent
from airflow.operators.python import PythonOperator
import pendulum
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
import pandas as pd
from sqlalchemy import create_engine

#extract tasks


#
# def load(tbl_dict: dict):
#     conn = BaseHook.get_connection('postgres')
#     engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
#     all_tbl_name = []
#     start_time = time.time()
#     #access the table_name element in dictionaries
#     for k, v in tbl_dict['table_name'].items():
#         #print(v)
#         all_tbl_name.append(v)
#         rows_imported = 0
#         sql = f'select * FROM {v}'
#         hook = mysql.MySqlHook(mysql_conn_id="mysql_db")
#         df = hook.get_pandas_df(sql)
#         print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {v} ')
#         df.to_sql(f'src_{v}', engine, if_exists='replace', index=False)
#         rows_imported += len(df)
#         print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
#     print("Data imported successful")
#     return all_tbl_name

# #load tasks
# @task()
# def prdProduct_model():
#     conn = BaseHook.get_connection('postgres')
#     engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
#     pc = pd.read_sql_query('SELECT * FROM public."stg_DimProductCategory" ', engine)
#     p = pd.read_sql_query('SELECT * FROM public."stg_DimProduct" ', engine)
#     p['ProductSubcategoryKey'] = p.ProductSubcategoryKey.astype(float)
#     p['ProductSubcategoryKey'] = p.ProductSubcategoryKey.astype(int)
#     ps = pd.read_sql_query('SELECT * FROM public."stg_DimProductSubcategory" ', engine)
#     #join all three
#     merged = p.merge(ps, on='ProductSubcategoryKey').merge(pc, on='ProductCategoryKey')
#     merged.to_sql(f'prd_DimProductCategory', engine, if_exists='replace', index=False)
#     return {"table(s) processed ": "Data imported successful"}

# [START how_to_task_group]
POSTGRES_CONN_ID="classicmodels_id"
with DAG(dag_id="Smart_ETL_Tool",schedule_interval="0 9 * * *", start_date=datetime(2022, 3, 5),catchup=False,  tags=["product_model"]) as dag:
    dag.doc_md = __doc__
    def extract():
        print("done")
        hook = PostgresHook(POSTGRES_CONN_ID)
        print(hook)
        sql = """ SELECT * FROM customers """
        df = hook.get_pandas_df(sql)
        print(df)
        tbl_dict = df.to_dict('dict')
        print('Extract task done successfully')
        return tbl_dict
    table=extract()
    # def load(**kwargs):
    #     print(table)
    #     conn = BaseHook.get_connection('postgres1_db')
    #     engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    #     all_tbl_name = []
    #     start_time = time.time()
    #     #access the table_name element in dictionaries
    #     for v in table.keys():
    #         #print(v)
    #         all_tbl_name.append(v)
    #         rows_imported = 0
    #         sql = f'select * FROM {v}'
    #         hook = PostgresHook(POSTGRES_CONN_ID)
    #         df = hook.get_pandas_df(sql)
    #         print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {v} ')
    #         df.to_sql(f'src_{v}', engine, if_exists='replace', index=False)
    #         rows_imported += len(df)
    #         print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
    #     print("Data imported successful")
    #     return all_tbl_name
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )
    load_task = PythonOperator(
        task_id='load',
        python_callable=extract,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=extract,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )
    extract_task >> transform_task >> load_task

    # with task_group.TaskGroup("extract_dimProudcts_load", tooltip="Extract and load source data") as extract_load_src:
    #     src_product_tbls = get_src_tables()
    #     load_dimProducts = load_src_data(src_product_tbls)
    #     #define order
    #     src_product_tbls >> load_dimProducts

    # # # [START howto_task_group_section_2]
    # # with task_group.TaskGroup("transform_src_product", tooltip="Transform and stage data") as transform_src_product:
    # #     transform_srcProduct = transform_srcProduct()
    # #     transform_srcProductSubcategory = transform_srcProductSubcategory()
    # #     transform_srcProductCategory = transform_srcProductCategory()
    # #     #define task order
    # #     [transform_srcProduct, transform_srcProductSubcategory, transform_srcProductCategory]

    # # with task_group.TaskGroup("load_product_model", tooltip="Final Product model") as load_product_model:
    # #     prd_Product_model = prdProduct_model()
    # #     #define order
    # #     prd_Product_model
    # extract_load_src

    # extract_load_src >> transform_src_product >> load_product_model
