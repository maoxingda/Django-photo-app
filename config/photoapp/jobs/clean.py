from django_extensions.management.jobs import BaseJob

from photoapp.models import Photo, CnTag


class Job(BaseJob):
    help = "清除数据"

    def execute(self):
        Photo.objects.all().delete()
        CnTag.objects.all().delete()
