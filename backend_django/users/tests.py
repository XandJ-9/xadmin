from django.test import TestCase
from users.models import User,Role

class UserModelTest(TestCase):
    def test_db_table_name(self):
        """测试User模型的数据库表名是否正确设置"""
        # 获取User模型的Meta类
        user_meta = User._meta
        print(user_meta.db_table)
