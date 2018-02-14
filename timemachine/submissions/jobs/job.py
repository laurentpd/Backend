from django.db import models
import django_rq
import tempfile
import os
import json
import traceback
import sys
import time


def current_milli_time():
    return int(round(time.time() * 1000))


class Job(models.Model):
    name = models.CharField(blank=False, max_length=40)
    code = models.TextField(blank=False)
    method = models.CharField(blank=False, max_length=50)
    metadata = models.TextField(default="{}")
    completed = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    error = models.TextField(blank=True)
    execution_time_millis = models.IntegerField(default=0)

    def save_code(self):
        directory = tempfile.mkdtemp(prefix=self.name + '_')
        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            f.write(self.code)

        return directory

    def decode_meta(self):
        return json.loads(self.metadata)

    def run(self):
        start_millis = current_milli_time()
        result = self.execute()
        end_millis = current_milli_time()

        self.execution_time_millis = end_millis - start_millis
        self.completed = True

        if isinstance(result, Exception):
            exc_type, exc_value, _ = sys.exc_info()
            self.error = traceback.format_exception_only(exc_type, exc_value)
            self.success = False
        else:
            self.error = ""
            self.success = True

        self.save()

    def enqueue(self):
        django_rq.enqueue(self.run)

    def execute(self):
        pass