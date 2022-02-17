from datetime import datetime, timezone
import glob
import logging
import os
import requests
import shutil
import time
import typing

from libdrm.common import log_execution
from libdrm.datamodels import ZipFileModel

# set logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("trigger_dag_run")

# envs
FILENAME = os.getenv("FILENAME")
DEBUG = int(os.getenv("DEBUG", 0))
AIRFLOW_USERNAME=os.getenv("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD=os.getenv("AIRFLOW_PASSWORD", "airflow")

# airflow REST API
airflow_api_base_url = "http://{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}@{host}:{port}/api/v1/".format(
    host="airflow-webserver",
    port=8080,
    AIRFLOW_USERNAME=AIRFLOW_USERNAME,
    AIRFLOW_PASSWORD=AIRFLOW_PASSWORD,
)

# data directories
data_root_dir = "/opt/smdrm/data"
imports_root_dir = os.path.join(data_root_dir, "import")
exports_root_dir = os.path.join(data_root_dir, "export")
volume_root_dir = os.path.join(data_root_dir, "airflow")


def get_import_files() -> typing.Iterable[str]:
    """Iter paths to zipfiles added in data/imports/."""
    if not FILENAME:
        console.warning("Processing all zipfiles in {}".format(imports_root_dir))
    pattern = os.path.join(imports_root_dir, "*.zip")
    for filepath in glob.iglob(pattern, recursive=True):
        if FILENAME and FILENAME not in filepath:
            continue
        yield filepath


def export_zipfile_to_airflow(filepath: str, datetime_fs: str, remove_original: bool = True) -> str:
    """Replace/move imported zipfile to Docker Volume filesystem."""
    # make datetime based filesystem in the Docker container executing the task
    # i.e. /data/YYYYMMDD/<filename>.zip
    # make the Docker filesystem if it does not exist
    os.makedirs(os.path.join(volume_root_dir, datetime_fs), exist_ok=True)
    # datetime based filesystem + filename
    airflow_rel_filepath = os.path.join(datetime_fs, os.path.basename(filepath))
    # replace by copy/remove file to avoid
    # OSError: [Errno 18] Invalid cross-device link
    shutil.copy(filepath, os.path.join(volume_root_dir, airflow_rel_filepath))
    if remove_original:
        console.warning("Removing {}".format(filepath))
        os.remove(filepath)
    # reference for REST API call and export
    return airflow_rel_filepath


def run_dag(
        airflow_rel_filepath: str,
        dag_run_id: str,
        logical_date: str,
        dag_id: str,
        collection_id: str = "smdrm_export_db"
    ):
    """
    Manually trigger DAG run via Airflow REST API.
    The Docker volume smdrm_export_db is the bridge
    to make input zipfiles available inside airflow.
    """
    url = airflow_api_base_url+"dags/{DAG_ID}/dagRuns".format(DAG_ID=dag_id)
    payload = {
        "conf": {
            # aka Docker Volume ID
            "COLLECTION_ID": collection_id,
            # inside the pipeline task container filesystem
            "INPUT_PATH": os.path.join("/data", airflow_rel_filepath),
            },
        "dag_run_id": dag_run_id,
        "logical_date": logical_date
        }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def dag_run_state(dag_run_id: str, dag_id: str):
    url = airflow_api_base_url+"dags/{DAG_ID}/dagRuns/{DAG_run_ID}".format(
            DAG_ID=dag_id,
            DAG_run_ID=dag_run_id,
        )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["state"]


def get_airflow_api_health():
    """REST API call to chech its health."""
    response = requests.get(airflow_api_base_url+"health")
    response.raise_for_status()
    return response.json()


class DAGRunFailure(Exception):
    pass


def wait_on_success(dag_run_id: str, dag_id: str, sleep_secs: int = 15):
    """Wait on DAG run to succed."""
    keep_waiting = True
    console.warning("Waiting on DAG run to complete...")
    while keep_waiting:
        state = dag_run_state(dag_run_id, dag_id=dag_id)

        if state == "failed":
            raise DAGRunFailure 

        if state != "success":
            console.debug("state={} > sleeping {} seconds...".format(state, sleep_secs))
            time.sleep(sleep_secs)
            continue

        keep_waiting = False
    return keep_waiting, state


def export_artifacts_to_host(airflow_abs_filepath: str):
    """Export artifacts to the directory mounted on the host."""
    d, f = os.path.split(airflow_abs_filepath)
    artifacts_pattern = os.path.join(d, "*.zip")
    for filepath in glob.iglob(artifacts_pattern, recursive=True):
        host_bind_filepath = os.path.join(exports_root_dir, os.path.basename(filepath))
        if f not in filepath:
            shutil.copy(filepath, host_bind_filepath)
            console.debug("Copied to {}".format(host_bind_filepath))
        # removing originals
        console.debug("Removing {}".format(filepath))
        os.remove(filepath)


def execute():
    if DEBUG:
        console.setLevel(logging.DEBUG)
   
    # validate Airflow API status
    airflow_api_health = get_airflow_api_health()
    console.debug("Airflow API health={}".format(airflow_api_health))

    # get input data paths
    for filepath in get_import_files():
        console.info("{} imported".format(filepath))

        # validate input zipfile
        if not ZipFileModel(filepath).is_valid():
            console.error("Fount invalid zipfile. Nothing to do...")
            continue

        # move imported zipfile into the Docker Volume
        # to make it available to the pipeline tasks in Airflow
        dt_based_fs = datetime.now().date().isoformat()
        airflow_rel_filepath = export_zipfile_to_airflow(
                filepath,
                dt_based_fs,
                remove_original=not DEBUG,
            )

        # DAG run trigger
        # get execution time
        utc_exec_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        console.debug("DAG run UTC execution time={}".format(utc_exec_time))

        dag_id = os.getenv("DAG_ID", "twitter")
        dag_run_id = os.getenv("DAG_run_ID", "manual_"+utc_exec_time)

        console.info("Triggering DAG run {}".format(dag_run_id))
        response = run_dag(airflow_rel_filepath, dag_run_id, utc_exec_time, dag_id)
        console.debug("DAG run response={}".format(response))

        # wait for DAG run state update
        keep_waiting, state = wait_on_success(dag_run_id, dag_id)
        console.info("DAG run state={}".format(state))

        if not keep_waiting:
            # export to bind mount folder on host
            console.info("Artifacts will be exported to data/exports on your host")
            airflow_abs_filepath = os.path.join(volume_root_dir, airflow_rel_filepath)
            export_artifacts_to_host(airflow_abs_filepath)


if __name__ == "__main__":
    execute()

