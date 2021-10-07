import requests

# available endpoints
endpoints_by_disaster = {
    "floods": "http://floods:5001/annotate",
    "fires": "http://fires:5002/annotate",
}


def api_annotate(disaster_type: str, batch: dict):
    """
    Call Annotation API with regards to the selected disaster type,
    and pass the batch to annotate. Batch format is {"batch": [{data_point1}, {data_point2}]}.
    Assume the endpoints are up and running.
    """
    return requests.post(endpoints_by_disaster[disaster_type], json=batch)
