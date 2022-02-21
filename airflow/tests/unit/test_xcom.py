import datetime
import pytest
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType

from conftest import twitter


class TestXComPush:

    CONF = {"COLLECTION_ID": "testID", "INPUT_PATH": "/data/test.zip"}
    EXEC_DATE = datetime.datetime.now(datetime.timezone.utc)

    def test_push_collection_id_task(self, unittest_dag):
        task_id = "push_collection_id"
        # adding task is possible within the unittest_dag context
        twitter.push_collection_id()
        # create a test DAG run instance
        dagrun = unittest_dag.create_dagrun(
            conf=self.CONF,
            state=DagRunState.RUNNING,
            run_type=DagRunType.MANUAL,
            run_id=task_id+"_unittest_"+self.EXEC_DATE.isoformat(),
        )
        # create and run a task instance from the dag run
        ti = dagrun.get_task_instance(task_id=task_id)
        ti.task = unittest_dag.get_task(task_id=task_id)
        ti.run(ignore_ti_state=True)

        assert ti.state == DagRunState.SUCCESS
        assert ti.xcom_pull(task_ids=task_id, key="cID") == self.CONF["COLLECTION_ID"]
        

    def test_push_filepaths_task(self, unittest_dag):
        task_id = "push_filepaths"
        # adding task is possible within the unittest_dag context
        twitter.push_filepaths()
        # create a test DAG run instance
        dagrun = unittest_dag.create_dagrun(
            conf=self.CONF,
            state=DagRunState.RUNNING,
            run_type=DagRunType.MANUAL,
            run_id=task_id+"_unittest_"+self.EXEC_DATE.isoformat(),
        )
        # create and run a task instance from the dag run
        ti = dagrun.get_task_instance(task_id=task_id)
        ti.task = unittest_dag.get_task(task_id=task_id)
        ti.run(ignore_ti_state=True)

        assert ti.state == DagRunState.SUCCESS
        assert ti.xcom_pull(task_ids=task_id, key="filepath_raw") == "/data/test.zip"
        assert ti.xcom_pull(task_ids=task_id, key="filepath_extracted") == "/data/test_extracted.zip"
        assert ti.xcom_pull(task_ids=task_id, key="filepath_transformed") == "/data/test_transformed.zip"
        assert ti.xcom_pull(task_ids=task_id, key="filepath_floods") == "/data/test_floods.zip"
        assert ti.xcom_pull(task_ids=task_id, key="filepath_geocoded") == "/data/test_geocoded.zip"
    
