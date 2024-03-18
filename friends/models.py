from django.db import models

# Create your models here.
from typing import Iterable

# from test.user.models import CustomUser
from apis.models import CustomUser

import random
# Create your models here.
class Group(models.Model):
    user = models.ManyToManyField(CustomUser,related_name='member_groups' )
    name = models.CharField(max_length=30)
    leader = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='leading_groups')
    joinning_code = models.CharField(max_length=4)
    def save(self):
        if not self.joinning_code:
            self.joinning_code =  "".join([random.randint(1,9) for _ in range(4)])
        return super().save()
