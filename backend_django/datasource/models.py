from django.db import models
from django.utils import timezone
from system.models import User
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
        db_table = 'ds_datasource'

    def __str__(self):
        return self.name


class QueryLog(BaseModel):
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, verbose_name='数据源')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='执行用户')
    sql = models.TextField(verbose_name='SQL语句')
    status = models.CharField(max_length=20, default='success', verbose_name='执行状态')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')
    execution_time = models.FloatField(default=0, verbose_name='执行时间(秒)')
    result_count = models.IntegerField(default=0, verbose_name='结果行数')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '查询日志'
        verbose_name_plural = verbose_name
        db_table = 'ds_query_log'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.datasource.name} - {self.created_at}"