from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from xadmin.models_base import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        db_table = 'sys_role'

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
        db_table = 'sys_user'

    def __str__(self):
        return self.username

        
class Menu(BaseModel):
    """系统菜单模型"""
    name = models.CharField(max_length=50, verbose_name='菜单名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父菜单')
    path = models.CharField(max_length=100, verbose_name='路由路径')
    component = models.CharField(max_length=100, verbose_name='组件路径', default='layout/index')
    component_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='组件名称')
    redirect = models.CharField(max_length=100, blank=True, null=True, verbose_name='重定向路径')
    name_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='路由名称代码')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='图标')
    sort = models.IntegerField(default=0, verbose_name='排序')
    hidden = models.BooleanField(default=False, verbose_name='是否隐藏')
    meta_title = models.CharField(max_length=50, blank=True, null=True, verbose_name='菜单标题')
    meta_icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='菜单图标')
    meta_need_tagview = models.BooleanField(default=False, verbose_name='是否需要tagview')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_menus', verbose_name='创建者', null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_menus', verbose_name='更新者', null=True)
    menu_type = models.CharField(max_length=1,choices=(("C","菜单"),("F","按钮"),("M","目录")),default="M")

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        db_table = 'sys_menu'
        ordering = ['sort']

    def __str__(self):
        return self.name
    
# class UserMenu(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_menus', verbose_name='用户')
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='user_menus', verbose_name='菜单')


class RoleMenu(BaseModel):
    """角色菜单关联模型"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_menus', verbose_name='角色')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='role_menus', verbose_name='菜单')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_role_menus', verbose_name='创建者')
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_role_menus', verbose_name='更新者')
    class Meta:
        verbose_name = '角色菜单关联'
        verbose_name_plural = verbose_name
        db_table ='sys_role_menu'
    def __str__(self):
        return f"{self.role.name} - {self.menu.name}"

class SystemConfig(BaseModel):
    """系统配置模型"""
    key = models.CharField(max_length=50, unique=True, verbose_name='配置键')
    value = models.TextField(verbose_name='配置值')
    description = models.TextField(blank=True, null=True, verbose_name='配置描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_configs', verbose_name='创建者')

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
        db_table = 'sys_config'

    def __str__(self):
        return f"{self.key}: {self.value}"


class BizBaseModel(BaseModel):
    """业务公共字段模型"""
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_creator', verbose_name='创建者', blank=True, null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updator', verbose_name='更新者', blank=True, null=True)
    class Meta:
        abstract = True