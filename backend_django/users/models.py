from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from xadmin.models_base import BaseModel

class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta(BaseModel.Meta):
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        # db_table = BaseModel.Meta.db_table + '_role'

    def __str__(self):
        return self.name

class User(AbstractUser, BaseModel):
    """自定义用户模型"""
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    avatar = models.CharField(max_length=200, blank=True, null=True, verbose_name='头像')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users', verbose_name='角色')
    
    # 移除默认的groups和user_permissions字段
    groups = None
    user_permissions = None

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        db_table = BaseModel.Meta.db_table + '_user'

    def __str__(self):
        return self.username