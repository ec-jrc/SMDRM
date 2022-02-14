"""
### Twitter DAG
Add the documentation here...
"""

import logging
from datetime import datetime, timedelta
from docker.types import Mount
from textwrap import dedent

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.utils.dates import days_ago

# set logging
console = logging.getLogger(__name__)

# Docker Engine socket location is behind
# a proxy (container) in the Docker network
docker_url = "tcp://docker-proxy:2375"


@task
def push_collection_id(ti=None, params=None, dag_run=None, test_mode=None):
    """Push collection ID XCom without a specific target"""
    cID = params["COLLECTION_ID"] if test_mode else dag_run.conf["COLLECTION_ID"] 
    console.info("XCom collection ID push: {}".format(cID))
    ti.xcom_push(key="cID", value=cID)


@task
def push_filepaths(ti=None, params=None, dag_run=None, test_mode=None):
    """Push filepath XCom without a specific target"""
    fp = params["INPUT_PATH"] if test_mode else dag_run.conf["INPUT_PATH"] 
    ti.xcom_push(key="filepath_raw", value=fp)
    console.info("XCom filepath pushed: {}".format(fp))
    # suffixes added to input fp to generate output filepaths
    file_extension = ".zip"
    for suffix in ["_extracted", "_transformed", "_floods", "_geocoded"]:
        output_fp = fp.replace(file_extension, suffix + file_extension)
        ti.xcom_push(key="filepath"+suffix, value=output_fp)
        console.info("XCom filepath pushed: {}".format(output_fp))


# default arguments for DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["admin@localhost.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="twitter",
    default_args=default_args,
    description="Establishes the workflow to process Twitter datapoints.",
    catchup=False,
    params={"ENV": "dev"},
    start_date=days_ago(5),
    schedule_interval=None,
    tags=["SMDRM", "ETL",],
) as dag:

    # DAG documentation
    # providing that you have a docstring at the beginning of the DAG
    dag.doc_md = __doc__

    # extract tweets task
    extract_tweets = DockerOperator(
        task_id="extract_tweets",
        api_version="auto",
        auto_remove=True,
        image="smdrm/extract_tweets:0.1.1-{{ params.ENV }}",
        docker_url=docker_url,
        network_mode="host",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume"
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

    # transform tweets task
    transform_tweets = DockerOperator(
        task_id="transform_tweets",
        api_version="auto",
        auto_remove=True,
        image="smdrm/transform_tweets:0.1.4-{{ params.ENV }}",
        docker_url=docker_url,
        network_mode="host",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume"
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
    # annotations
    floods_annotate = DockerOperator(
        task_id="floods_annotate_tweets",
        api_version="auto",
        auto_remove=True,
        image="smdrm/floods_annotate:0.1.1-{{ params.ENV }}",
        docker_url=docker_url,
        network_mode="host",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume"
                ),
            ],
        mount_tmp_dir=False,
        command='python floods_annotate.py \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_transformed") }} \
        --output-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_floods") }}',
    )
    # documentation
    floods_annotate.doc_m = dedent(
        """\
        #### Floods Annotate
        Annotate `text` data with the Floods Named Entity Recognition annotator.
        """
    )

    # geocode
    geocode_tweets = DockerOperator(
        task_id="geocode_tweets",
        api_version="auto",
        auto_remove=True,
        image="smdrm/geocode_tweets:0.1.0-{{ params.ENV }}",
        docker_url=docker_url,
        network_mode="host",
        mounts=[
            Mount(
                source='{{ ti.xcom_pull(task_ids="push_collection_id", key="cID") }}',
                target="/data",
                type="volume"
                ),
            ],
        mount_tmp_dir=False,
        command='python geocode_tweets.py --debug \
        --input-path {{ ti.xcom_pull(task_ids="push_filepaths", key="filepath_floods") }} \
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

    # set tasks dependencies
    [
        # XCom metadata
        push_collection_id(),
        push_filepaths(),
        # api sensors
        is_deeppavlov_api_ready,
        is_floods_api_ready
    ] >> extract_tweets
    extract_tweets >>  transform_tweets >> floods_annotate >> geocode_tweets
    
