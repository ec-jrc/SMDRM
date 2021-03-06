"""
### Twitter DAG
Twitter DAG is the workflow to run the pipeline tasks responsible to manipulate Twitter datapoints.

The expected input file format is zipfile. One zipfile at the time can be processed in each DAG run.
Each zipfile may contain 1 or more Newline Delimited JSON file(s), for a total size of 64 mb after compression.

A DAG run is a running instance of the workflow. It requires you to set a `COLLECTION_ID`, and a `INPUT_PATH`.
The COLLECTION_ID is the Docker volume name with the zipfile to be manipulated. Whereas the INPUT_PATH is the zipfile name.

The easiest way to trigger a DAG run is to upload a zipfile through the SMDRM API, available on the host @ http://localhost:7000/api/v1.
Ensure that the arguments in the body of the HTTP POST request are `dag_id=twitter`, and `collection_id=smdrm_uploads-volume`.
"""

import logging
from datetime import datetime, timedelta
from docker.types import Mount
from textwrap import dedent

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.utils.dates import days_ago
from airflow.operators.email import EmailOperator

# set logging
console = logging.getLogger(__name__)

# Docker Engine socket location is behind
# a proxy (container) in the Docker network
docker_url = "tcp://docker-proxy:2375"


def get_notification_emails_from_env():
    # emails to send failure notifications to
    emails_to_notify = []
    csv_emails = Variable.get("CSV_EMAILS_TO_NOTIFY_FAILURES", default_var=None)

    # enable email notification for DAG failures if emails are given
    if csv_emails is not None:
        for email in csv_emails.split(","):
            if email:
                emails_to_notify.append(email)

    return emails_to_notify


@task(task_id="push_collection_id")
def push_collection_id(ti=None, params=None, dag_run=None, test_mode=None):
    """Push collection ID XCom without a specific target"""
    cID = params["COLLECTION_ID"] if test_mode else dag_run.conf["COLLECTION_ID"]
    console.info("XCom collection ID push: {}".format(cID))
    ti.xcom_push(key="cID", value=cID)


@task(task_id="push_filepaths")
def push_filepaths(ti=None, params=None, dag_run=None, test_mode=None):
    """Push filepath XCom without a specific target"""
    fp = params["INPUT_PATH"] if test_mode else dag_run.conf["INPUT_PATH"]
    ti.xcom_push(key="filepath_raw", value=fp)
    console.info("XCom filepath pushed: {}".format(fp))
    # suffixes added to input fp to generate output filepaths
    file_extension = ".zip"
    for suffix in ["_extracted", "_transformed", "_annotated", "_geocoded"]:
        output_fp = fp.replace(file_extension, suffix + file_extension)
        ti.xcom_push(key="filepath" + suffix, value=output_fp)
        console.info("XCom filepath pushed: {}".format(output_fp))


# notification emails
emails = get_notification_emails_from_env()

# default arguments for DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": emails,
    "email_on_failure": len(emails) > 0,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="twitter",
    default_args=default_args,
    description="Establishes the workflow to process Twitter datapoints.",
    catchup=False,
    start_date=days_ago(5),
    schedule_interval=None,
    tags=[
        "SMDRM",
        "ETL",
    ],
) as dag:

    # DAG documentation
    # providing that you have a docstring at the beginning of the DAG
    dag.doc_md = __doc__

    ## API SENSORS

    # check if DeepPavlov API is ready
    is_deeppavlov_api_ready = HttpSensor(
        task_id="is_deeppavlov_api_ready",
        http_conn_id="deeppavlov_api",
        # everything after url domain
        endpoint="status",
        # status response: {"ready": True}
        response_check=lambda r: r.json()["ready"],
        poke_interval=10,
        timeout=30,
    )
    # documentation
    is_deeppavlov_api_ready.doc_md = dedent(
        """\
        #### DeepPavlov API Uptime Status
        Status check for DeepPavlov API.
        This is an external plugin required by the following
        task `transform_tweets` for Named Entity Recognition tagging.
        """
    )

    # check if Floods API is ready
    is_floods_api_ready = HttpSensor(
        task_id="is_floods_api_ready",
        http_conn_id="floods_api",
        # everything after url domain
        endpoint="status",
        # status response: "ready"
        response_check=lambda r: r.json() == "ready",
        poke_interval=10,
        timeout=30,
    )
    # documentation
    is_floods_api_ready.doc_md = dedent(
        """\
        #### Floods API Uptime Status
        Status check for Floods API.
        This is an external plugin required by the following
        task `floods_annotate` for Named Entity Recognition annotation.
        """
    )

    # check if Elasticsearch API is ready
    is_elasticsearch_api_ready = HttpSensor(
        task_id="is_elasticsearch_api_ready",
        http_conn_id="elasticsearch_api",
        # everything after url domain
        endpoint="_cluster/health",
        # status response: {"status": "green|yellow"}
        response_check=lambda r: r.status_code == 200 and "status" in r.json(),
        poke_interval=10,
        timeout=30,
    )
    # documentation
    is_elasticsearch_api_ready.doc_md = dedent(
        """\
        #### Elasticsearch API Uptime Status
        Status check for Elasticsearch API.
        This is an external NoSQL DB plugin required by the following
        task `cache_tweets` for caching enriched datapoints. It enables
        fast queries, and dataset discovery through Kibana dashboard.

        Kibana is available at the default port @ http://localhost:5601.
        """
    )

    ## Pipeline Tasks

    # extract tweets task
    extract_tweets = DockerOperator(
        task_id="extract_tweets",
        api_version="auto",
        auto_remove=True,
        image="tasks/extract-tweets",
        docker_url=docker_url,
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume",
            ),
        ],
        mount_tmp_dir=False,
        command='python extract_tweets.py \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_raw") }} \
        --output-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_extracted") }}',
    )
    # documentation
    extract_tweets.doc_m = dedent(
        """\
        #### Extract Tweets
        Extracts/creates specific fields to enforce the SMDRM Datapoint Data Model.
        It minimizes the memory consumption footprint by removing unnecessary data.
        """
    )

    # transform tweets task
    transform_tweets = DockerOperator(
        task_id="transform_tweets",
        api_version="auto",
        auto_remove=True,
        image="tasks/transform-tweets",
        docker_url=docker_url,
        network_mode="smdrm_default",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume",
            ),
        ],
        mount_tmp_dir=False,
        command='python transform_tweets.py \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_extracted") }} \
        --output-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_transformed") }}',
    )
    # documentation
    transform_tweets.doc_m = dedent(
        """\
        #### Transform Tweets
        Appy normalization transformations on the datapoint `text` field,
        and extracts place candidates for geocoding purposes.
        """
    )

    # annotations
    annotate_tweets = DockerOperator(
        task_id="annotate_tweets",
        api_version="auto",
        auto_remove=True,
        environment={
            # TODO: parametize
            "ANNOTATOR_ID": "floods",
            },
        image="tasks/annotate-tweets",
        docker_url=docker_url,
        network_mode="smdrm_default",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume",
            ),
        ],
        mount_tmp_dir=False,
        command='python annotate_tweets.py \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_transformed") }} \
        --output-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_annotated") }}',
    )
    # documentation
    annotate_tweets.doc_m = dedent(
        """\
        #### Annotate Tweets
        Annotate `text` data with a chose Named Entity Recognition annotator.
        """
    )

    # geocode
    geocode_tweets = DockerOperator(
        task_id="geocode_tweets",
        api_version="auto",
        auto_remove=True,
        image="tasks/geocode-tweets",
        docker_url=docker_url,
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume",
            ),
        ],
        mount_tmp_dir=False,
        command='python geocode_tweets.py \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_annotated") }} \
        --output-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_geocoded") }}',
    )
    # documentation
    geocode_tweets.doc_m = dedent(
        """\
        #### Geocode Tweets
        Search place candidates identified at `transform_tweets`
        step against our Global Places datasets.
        """
    )

    # cache
    cache_tweets = DockerOperator(
        task_id="cache_tweets",
        api_version="auto",
        auto_remove=True,
        image="tasks/cache-tweets",
        docker_url=docker_url,
        network_mode="smdrm_default",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume",
            ),
        ],
        mount_tmp_dir=False,
        command='python cache_tweets.py \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_geocoded") }}',
    )
    # documentation
    cache_tweets.doc_m = dedent(
        """\
        #### Cache Tweets
        Caches the content of a zipfile of enriched datapoints
        that passed through the tasks of a pipeline (DAG) to ElasticSearch.

        You can use the Kibana UI to manage the cached datapoints.
        """
    )

    ## Dependencies

    [
        ## XCom Metadata
        push_collection_id(),
        push_filepaths(),
        # API sensors
        is_deeppavlov_api_ready,
        is_floods_api_ready,
        is_elasticsearch_api_ready,
    ] >> extract_tweets

    # Tasks
    (
        extract_tweets
        >> transform_tweets
        >> annotate_tweets
        >> geocode_tweets
        >> cache_tweets
    )
