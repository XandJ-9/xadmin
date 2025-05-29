from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class BaseModel(models.Model):

    """所有模型的基类，用于设置统一的表前缀"""
    class Meta:
        abstract = True
        db_table = settings.DATABASE_TABLE_PREFIX


class Captcha(models.Model):
    """验证码模型"""
    code = models.CharField(max_length=10, verbose_name='验证码')
    uuid = models.CharField(max_length=50, unique=True, verbose_name='UUID')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name
        db_table = 'sys_captcha'

    def __str__(self):
        return self.code

class Role(BaseModel):
    DATA_SCOPE_CHOICES = [
        ('1', '全部数据权限'),
        ('2', '自定数据权限'),
        ('3', '本部门数据权限'),
        ('4', '本部门及以下数据权限'),
    ]
    STATUS_CHOICES = [
        ('0', '正常'),
        ('1', '停用'),
    ]
    DEL_FLAG_CHOICES = [
        ('0', '存在'),
        ('2', '删除'),
    ]
    
    role_name = models.CharField(max_length=30, verbose_name='角色名称')
    role_key = models.CharField(max_length=100, verbose_name='角色权限字符串')
    role_sort = models.IntegerField(verbose_name='显示顺序')
    data_scope = models.CharField(max_length=1, default='1', choices=DATA_SCOPE_CHOICES, verbose_name='数据范围')
    menu_check_strictly = models.BooleanField(default=True, verbose_name='菜单树选择项是否关联显示')
    dept_check_strictly = models.BooleanField(default=True, verbose_name='部门树选择项是否关联显示')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='角色状态')
    del_flag = models.CharField(max_length=1, default='0', choices=DEL_FLAG_CHOICES, verbose_name='删除标志')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        db_table = 'sys_role'

    def __str__(self):
        return self.role_name

class Dept(BaseModel):
    DEPT_CHOICES = [
        ('1', '正常'),
        ('2', '停用'),
    ]

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, verbose_name='父部门')
    dept_name = models.CharField(max_length=30, verbose_name='部门名称')
    ancestors = models.CharField(max_length=50, default='', verbose_name='祖级列表')
    order_num = models.IntegerField(verbose_name='显示顺序')
    leader = models.CharField(max_length=20, blank=True, null=True, verbose_name='负责人')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='联系电话')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱')
    status = models.CharField(max_length=1, default='0', choices=DEPT_CHOICES, verbose_name='部门状态')
    del_flag = models.CharField(max_length=1, default='0', verbose_name='删除标志')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        db_table = 'sys_dept'

class User(AbstractUser, BaseModel):
    """自定义用户模型"""
    USER_STATUS_CHOICES = [
        ('0', '停用'),
        ('1', '正常'),
    ]
    USER_TYPE_CHOICES = [
        ('00', '系统用户'),
    ]
    SEX_CHOICES = [
        ('0', '男'),
        ('1', '女'),
        ('2', '未知'),
    ]
    DEL_FLAG_CHOICES = [
        ('0', '存在'),
        ('2', '删除'),
    ]
    
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,null=True, blank=True, verbose_name='部门ID')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    user_type = models.CharField(max_length=2, default='00', choices=USER_TYPE_CHOICES, verbose_name='用户类型')
    email = models.EmailField(max_length=50, blank=True, default='', verbose_name='用户邮箱')
    phonenumber = models.CharField(max_length=11, blank=True, default='', verbose_name='手机号码')
    sex = models.CharField(max_length=1, default='0', choices=SEX_CHOICES, verbose_name='用户性别')
    avatar = models.CharField(max_length=200, blank=True, null=True, verbose_name='头像')
    status = models.CharField(max_length=1, default='1', choices=USER_STATUS_CHOICES, verbose_name='是否启用')
    del_flag = models.CharField(max_length=1, default='0', choices=DEL_FLAG_CHOICES, verbose_name='删除标志')
    login_ip = models.CharField(max_length=128, blank=True, default='', verbose_name='最后登录IP')
    login_date = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
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

class UserRole(BaseModel):
    """用户角色关联模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles', verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles', verbose_name='角色')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户角色关联'
        verbose_name_plural = verbose_name
        db_table = 'sys_user_role'

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
        
class Menu(BaseModel):
    """系统菜单模型"""
    IS_FRAME_CHOICES = [
        (0, '是'),
        (1, '否'),
    ]
    IS_CACHE_CHOICES = [
        (0, '缓存'),
        (1, '不缓存'),
    ]
    MENU_TYPE_CHOICES = [
        ('M', '目录'),
        ('C', '菜单'),
        ('F', '按钮'),
    ]
    VISIBLE_CHOICES = [
        ('0', '显示'),
        ('1', '隐藏'),
    ]
    STATUS_CHOICES = [
        ('0', '正常'),
        ('1', '停用'),
    ]
    
    menu_name = models.CharField(max_length=50, verbose_name='菜单名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父菜单')
    order_num = models.IntegerField(default=0, verbose_name='显示顺序')
    path = models.CharField(max_length=200, default='', verbose_name='路由地址')
    redirect = models.CharField(max_length=200, null=True, blank=True, verbose_name='重定向地址')
    component = models.CharField(max_length=255, null=True, blank=True, verbose_name='组件路径')
    query = models.CharField(max_length=255, null=True, blank=True, verbose_name='路由参数')
    route_name = models.CharField(max_length=50, default='', verbose_name='路由名称')
    is_frame = models.IntegerField(default=1, choices=IS_FRAME_CHOICES, verbose_name='是否为外链')
    is_cache = models.IntegerField(default=0, choices=IS_CACHE_CHOICES, verbose_name='是否缓存')
    menu_type = models.CharField(max_length=1, default='', choices=MENU_TYPE_CHOICES, verbose_name='菜单类型')
    visible = models.CharField(max_length=1, default='0', choices=VISIBLE_CHOICES, verbose_name='菜单可见')
    status = models.CharField(max_length=1, default='0', choices=STATUS_CHOICES, verbose_name='菜单状态')
    perms = models.CharField(max_length=100, null=True, blank=True, verbose_name='权限标识')
    icon = models.CharField(max_length=100, default='#', verbose_name='菜单图标')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu_creator', verbose_name='创建者', null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu_updator', verbose_name='更新者', null=True)
    remark = models.CharField(max_length=500, default='', verbose_name='备注')

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        db_table = 'sys_menu'
        ordering = ['order_num']

    def __str__(self):
        return self.menu_name
    
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
        return f"{self.role.role_name} - {self.menu.menu_name}"

class SystemConfig(BaseModel):
    """系统配置模型"""
    CONFIG_TYPE_CHOICES = [
        ('Y', '是'),
        ('N', '否'),
    ]
    
    config_name = models.CharField(max_length=100, default='', verbose_name='参数名称')
    config_key = models.CharField(max_length=100, default='', verbose_name='参数键名')
    config_value = models.CharField(max_length=500, default='', verbose_name='参数键值')
    config_type = models.CharField(max_length=1, default='N', choices=CONFIG_TYPE_CHOICES, verbose_name='系统内置')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_configs', verbose_name='创建者', null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_configs', verbose_name='更新者', null=True)
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
        db_table = 'sys_config'

    def __str__(self):
        return f"{self.config_key}"


class SystemDictType(BaseModel):
    """系统字典模型"""
    STATUS_CHOICES = [
        ('0', '正常'),
        ('1', '停用'),
    ]
    
    dict_name = models.CharField(max_length=100, default='', verbose_name='字典名称')
    dict_type = models.CharField(max_length=100, default='', verbose_name='字典类型', unique=True)
    status = models.CharField(max_length=1, default='0', choices=STATUS_CHOICES, verbose_name='状态')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_dicts', verbose_name='创建者', null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_dicts', verbose_name='更新者', null=True)
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '字典类型'
        verbose_name_plural = verbose_name
        db_table = 'sys_dict_type'
        
    def __str__(self):
        return self.dict_name

class SystemDictData(BaseModel):
    """字典数据模型"""
    IS_DEFAULT_CHOICES = [
        ('Y', '是'),
        ('N', '否'),
    ]
    STATUS_CHOICES = [
        ('0', '正常'),
        ('1', '停用'),
    ]
    
    dict_sort = models.IntegerField(default=0, verbose_name='字典排序')
    dict_label = models.CharField(max_length=100, default='', verbose_name='字典标签')
    dict_value = models.CharField(max_length=100, default='', verbose_name='字典键值')
    dict_type = models.CharField(max_length=100, default='', verbose_name='字典类型')
    css_class = models.CharField(max_length=100, null=True, blank=True, verbose_name='样式属性（其他样式扩展）')
    list_class = models.CharField(max_length=100, null=True, blank=True, verbose_name='表格回显样式')
    is_default = models.CharField(max_length=1, default='N', choices=IS_DEFAULT_CHOICES, verbose_name='是否默认')
    status = models.CharField(max_length=1, default='0', choices=STATUS_CHOICES, verbose_name='状态')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_dict_datas', verbose_name='创建者', null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_dict_datas', verbose_name='更新者', null=True)
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '字典数据'
        verbose_name_plural = verbose_name
        db_table = 'sys_dict_data'

    def __str__(self):
        return self.dict_label

class BizBaseModel(BaseModel):
    """业务公共字段模型"""
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_creator', verbose_name='创建者', blank=True, null=True)
    updator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updator', verbose_name='更新者', blank=True, null=True)
    class Meta:
        abstract = True