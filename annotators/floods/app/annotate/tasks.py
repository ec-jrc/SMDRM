from . import celery
from flask import current_app

@celery.task(name='app.tasks.annotate_batch')
def annotate_batch(texts):
    # do some processing
    pass
