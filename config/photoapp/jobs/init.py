import os
from glob import glob
from pathlib import Path
from pprint import pprint

from django.contrib.auth.models import User
from django.core.files import File
from django_extensions.management.jobs import BaseJob

from photoapp.models import CnTag, Photo


class Job(BaseJob):
    help = "初始化数据"

    def execute(self):
        CnTag(name='是').save()
        CnTag(name='否').save()
        for (root, dirs, files) in os.walk(os.getcwd() + '/pic', topdown=True):
            user = User.objects.get(id=2)
            for file in files:
                path = Path(os.path.join(root, file))
                with path.open(mode='rb') as f:
                    tag = os.path.basename(root)
                    photo = Photo(
                        title=tag,
                        description=tag,
                        submitter=user,
                    )
                    photo.image = File(f, name=path.name)
                    photo.save()
                    # 必须先保存之后才能添加tag因为tag会用到对象ID
                    photo.tags.add(tag)
