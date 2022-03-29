import pytest
from datetime import datetime, timezone
from airflow.models import DagBag, TaskInstance


@pytest.fixture(scope="class")
def dag(dagbag):
    """Get Twitter DAG instance."""
    return dagbag.get_dag("twitter")


class TestTwitterDagDefinition:

    EXPECTED_TASKS = [
        "push_collection_id",
        "push_filepaths",
        "is_deeppavlov_api_ready",
        "is_floods_api_ready",
        "is_elasticsearch_api_ready",
        "extract_tweets",
        "transform_tweets",
        "annotate_tweets",
        "geocode_tweets",
        "cache_tweets"
    ]
    EXPECTED_N_TASKS = len(EXPECTED_TASKS)

    # check if 2 lists are equivalent
    compare = lambda self, x, y: sorted(set(x)) == sorted(set(y))

    def test_number_of_tasks(self, dag):
        """
        Verify the number of tasks in the DAG
        """
        n_tasks = len(dag.tasks)
        assert (
            n_tasks == self.EXPECTED_N_TASKS
        ), "Wrong number of tasks, {0} expected, got {1}".format(
            self.EXPECTED_N_TASKS, n_tasks
        )

    def test_contain_tasks(self, dag):
        """
        Verify if the DAG is composed of the expected tasks
        """
        task_ids = [ti.task_id for ti in dag.tasks]
        assert self.compare(task_ids, self.EXPECTED_TASKS)

    @pytest.mark.parametrize(
        "task, expected_upstream, expected_downstream",
        [
            ("push_collection_id", [], ["extract_tweets"]),
            (
                "extract_tweets",
                [
                    "push_collection_id",
                    "push_filepaths",
                    "is_deeppavlov_api_ready",
                    "is_floods_api_ready",
                    "is_elasticsearch_api_ready",
                ],
                ["transform_tweets"],
            ),
            ("annotate_tweets", ["transform_tweets"], ["geocode_tweets"]),
            ("cache_tweets", ["geocode_tweets"], []),
        ],
    )
    def test_dependencies_of_tasks(
        self, dag, task, expected_upstream, expected_downstream
    ):
        """
        Verify if a given task has the expected upstream and downstream dependencies
        - Parametrized test function so that each task given in the array is tested with the associated parameters
        """
        task = dag.get_task(task)
        assert self.compare(
            task.upstream_task_ids, expected_upstream
        ), "The task {0} doesn't have the expected upstream dependencies".format(task)
        assert self.compare(
            task.downstream_task_ids, expected_downstream
        ), "The task {0} doesn't have the expected downstream dependencies".format(task)

    def test_start_date_schedule_interval_and_catchup(self, dag):
        """
        Verify that the start_date is at least 5 days ago
        catchup is False and schedule_interval is None
        because this task is manually triggered
        """
        assert (datetime.now(timezone.utc) - dag.start_date).days >= 5
        assert not dag.catchup and not dag.schedule_interval

    def test_same_start_date_all_tasks(self, dag):
        """
        Best Practice: All of your tasks should have the same start_date
        """
        tasks = dag.tasks
        start_dates = list(map(lambda task: task.start_date, tasks))
        assert len(set(start_dates)) == 1
