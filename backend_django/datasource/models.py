from django.db import models
from django.utils import timezone
from users.models import User
from xadmin.models_base import BaseModel

class DataSource(BaseModel):
    name = models.CharField(max_length=100, verbose_name='数据源名称')
    type = models.CharField(max_length=50, default='mysql', verbose_name='数据源类型')
    host = models.CharField(max_length=255, verbose_name='主机地址')
    port = models.IntegerField(verbose_name='端口')
    database = models.CharField(max_length=100, verbose_name='数据库名')
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '数据源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name