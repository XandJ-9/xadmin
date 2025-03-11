from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    """所有模型的基类，用于设置统一的表前缀"""
    class Meta:
        abstract = True

    @classmethod
    def get_db_table(cls):
        app_label = cls._meta.app_label
        model_name = cls._meta.model_name
        table_name = f"{app_label}_{model_name}"
        return f"{settings.DATABASE_TABLE_PREFIX}_{table_name}"
