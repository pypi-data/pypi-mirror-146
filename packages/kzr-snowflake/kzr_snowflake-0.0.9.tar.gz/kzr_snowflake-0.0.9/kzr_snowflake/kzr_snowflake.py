# pip install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.5.0/tested_requirements/requirements_36.reqs
# pip install snowflake-connector-python==2.5.0
from numpy.distutils.fcompiler import none
import json
import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.connector.pandas_tools import write_pandas
import timeit
import pandas as pd
import pyarrow
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

connection: SnowflakeConnection = none
path = ""
role = ""
warehouse = ""
database = ""
schema = ""


def get_engine():
    with open(path, "r") as f:
        cred = json.load(f)
    engine = create_engine(URL(
        user=cred['user'],
        password=cred['password'],
        account=cred['account'],
        role=role,
        warehouse=warehouse,
        database=database,
        schema=schema
    ))
    conn = engine.connect()
    return engine


def connect():
    global connection
    with open(path, "r") as f:
        cred = json.load(f)
    connection = snowflake.connector.connect(
        user=cred['user'],
        password=cred['password'],
        account=cred['account'],
        role=role,
        warehouse=warehouse,
        database=database,
        schema=schema,
        paramstyle='qmark'
    )
    print("connected!")


def execute(statement):
    with connection.cursor() as cs:
        try:
            cs.execute(statement)
        except Exception as e:
            print(e)
            return False
        finally:
            if not cs.messages:
                print("Executed")
                return True
    return False


def disconnect():
    connection.close()


def select_m(statement):
    print(timeit.timeit("pass"))
    cs = connection.cursor()
    df = none
    try:
        cs.execute(statement)
        df = cs.fetch_pandas_all()
    except Exception as e:
        print(e)
    finally:
        cs.close()
        print(timeit.timeit("pass"))
        return df


def select_one(statement):
    cs = connection.cursor()
    value = none
    try:
        cs.execute(statement)
        value = cs.fetchone()
    except Exception as e:
        print(e)
    finally:
        cs.close()
        print(timeit.timeit("pass"))
        return value


def insert_m(statement, params):
    cs = connection.cursor()
    try:
        cs.executemany(statement, params)
    except Exception as e:
        print(e)
    finally:
        cs.close()


def select_into_df(statement):
    try:
        df = pd.read_sql(
            statement,
            connection
        )
    except Exception as e:
        print(e)
    finally:
        return df


def insert_df(table_name, df):
    success = False
    try:
        success, nchunks, nrows, output = write_pandas(
            connection,
            df,
            table_name
        )
    except Exception as e:
        print('error: {}'.format(e))
    finally:
        if success:
            print(
                'success = ' + str(success)
                + '\nnchunks = ' + str(nchunks)
                + '\nnrows = ' + str(nrows)
                + '\nnrows = ' + str(nrows)
            )


def create_task(
    name
    , sql
    , warehouse=False
    , user_task_managed_initial_warehouse_size=False
    , schedule=False
    , allow_overlapping_execution=False
    , user_task_timeout_ms=False
    , comment=False
    , after=False
    , when=False
    , replace=False
    , print_statement=False
):
    if (warehouse and user_task_managed_initial_warehouse_size) or (not warehouse and
                                                                    not user_task_managed_initial_warehouse_size):
        print('Use one type of warehouse option!')
        return False

    if (schedule and after) or (not schedule and not after):
        print('Choose either task is after another task or provide schedule!')
        return False

    statement = f"CREATE TASK {name}" if not replace else f"CREATE OR REPLACE TASK {name}"
    statement += f"\n\tUSER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = '{user_task_managed_initial_warehouse_size}" if not warehouse else f"\n\tWAREHOUSE = {warehouse}"
    statement += f"\n\tSCHEDULE = '{schedule}'" if not after else f"\n\tAFTER = '{after}'"
    if allow_overlapping_execution:
        statement += f"\n\tALLOW_OVERLAPPING_EXECUTION = TRUE"
    if user_task_timeout_ms:
        statement += f"\n\tUSER_TASK_TIMEOUT_MS = {user_task_timeout_ms}"
    if comment:
        statement += f"\n\tCOMMENT = {comment}"
    if when:
        statement += f"\nWHEN\n\t{when}"
    statement += f"\nAS\n\t{sql};"

    if print_statement: print(statement)
    return execute(statement)
