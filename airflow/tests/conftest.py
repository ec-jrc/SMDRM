import pytest
from airflow import DAG
from airflow.utils.dates import days_ago 
from airflow.models import DagBag

import sys
sys.path.append("/opt/airflow/dags/twitter.py")
import twitter


@pytest.fixture(scope="session")
def dagbag():
    """Init all dags in the dag directory
    configured in the airflow.cfg file."""
    return DagBag()


@pytest.fixture()
def unittest_dag():
    """Generate a DAG for testing purpose only.
    Yielding the dag instance makes it possible to extend
    the DAG (i.e. adding tasks) at test function level."""
    with DAG(
        dag_id="twitter_test",
        schedule_interval=None,
        catchup=False,
        start_date=days_ago(5),
    ) as dag:
        yield dag

