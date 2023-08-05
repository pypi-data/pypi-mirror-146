# batch_job.py


from src import settings
from .object_def.event import Event


def creates_batchs(batchs):
    # jobs
    for batch in batchs:
        event = Event(batch, settings.APP_DIR + "/jobs/")
        event.to_file()
