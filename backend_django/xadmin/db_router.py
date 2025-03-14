from django.conf import settings

class XAdminDBRouter:
    """数据库路由类，用于管理模型表的映射"""

    def db_for_read(self, model, **hints):
        """指定读操作的数据库"""
        return 'default'

    def db_for_write(self, model, **hints):
        """指定写操作的数据库"""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """是否允许关联操作"""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """是否允许迁移操作"""
        return True

    def get_table_name(self, model):
        """获取带前缀的表名"""
        if hasattr(model._meta, 'db_table'):
            # 如果模型已经指定了表名，则在表名前添加前缀
            return f"{settings.DATABASE_TABLE_PREFIX}{model._meta.db_table}"
        # 如果模型没有指定表名，则使用默认的表名规则并添加前缀
        return f"{settings.DATABASE_TABLE_PREFIX}{model._meta.app_label}_{model._meta.model_name}"
