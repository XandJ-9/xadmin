from django.db import models
from django.conf import settings

class BaseModel(models.Model):

    """所有模型的基类，用于设置统一的表前缀"""
    class Meta:
        abstract = True
