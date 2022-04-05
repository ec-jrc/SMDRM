from datetime import datetime, timezone
import os
import requests

class AirflowJobsTrigger:
    """Represents an object to handle jobs for the Airflow API."""

    # Airflow API config
    USERNAME = os.getenv("AIRFLOW_USERNAME", "airflow")
    PASSWORD = os.getenv("AIRFLOW_PASSWORD", "airflow")
    HOST = os.getenv("AIRFLOW_HOST", "airflow-webserver")
    PORT = os.getenv("AIRFLOW_PORT", "8080")

    BASEURL = "http://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/api/v1/".format(
        HOST=HOST,
        PORT=PORT,
        USERNAME=USERNAME,
        PASSWORD=PASSWORD,
    )

    @classmethod
    def run_dag(
        cls,
        filename: str,
        dag_id: str = "twitter",
        collection_id: str = "smdrm_uploads-volume",
    ):
        """
        Manually trigger DAG run via Airflow REST API.
        The collection ID is the Docker volume name used
        to make input zipfiles available inside Airflow tasks.

        Notes:
        collection_id=smdrm_uploads-volume is the name of a special
        Docker Volume initialized at application startup.
        """

        # build DAG run ID
        exec_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        dag_run_id = "ui_{}_{}".format(collection_id, exec_time)
        # build dagRun url
        url = cls.BASEURL + "dags/{DAG_ID}/dagRuns".format(DAG_ID=dag_id)
        # build payload
        payload = {
            "conf": {
                # aka Docker Volume ID
                "COLLECTION_ID": collection_id,
                # inside the pipeline task container filesystem
                # Docker Volume is mounted @ /data directory
                "INPUT_PATH": os.path.join("/data", filename),
            },
            "dag_run_id": dag_run_id,
            "logical_date": exec_time,
        }
        response = requests.post(url, json=payload)
        return response.json()
