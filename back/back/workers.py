from celery import Celery
from flask import current_app as app

celery = Celery(
    "tasks", broker="redis://localhost:6380/0", backend="redis://localhost:6380/0"
)

# Create a subclass of the task
# that wraps the task execution in an application context.
# So its available


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
