import pytest
from airflow.models import DagBag

@pytest.fixture(scope="session")
def dagbag():
    """Init all dags in the dag directory
    configured in the airflow.cfg file."""
    return DagBag()

