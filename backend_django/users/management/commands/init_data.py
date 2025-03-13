import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from users.models import User, Role
from datasource.models import DataSource

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = '初始化系统数据，包括默认角色、管理员用户和示例数据源'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新创建数据，即使数据已存在',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options.get('force', False)
        self.stdout.write(self.style.NOTICE('开始初始化系统数据...'))
        
        # 初始化角色
        self._init_roles(force)
        
        # 初始化管理员用户
        self._init_admin_user(force)
        
        # 初始化示例数据源
        self._init_sample_datasource(force)
        
        self.stdout.write(self.style.SUCCESS('系统数据初始化完成！'))
    
    def _init_roles(self, force):
        """初始化角色数据"""
        self.stdout.write('初始化角色数据...')
        
        # 默认角色列表
        default_roles = [
            {'name': 'admin', 'description': '管理员'},
            {'name': 'user', 'description': '普通用户'},
        ]
        
        for role_data in default_roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建角色: {role.name}'))
            elif force:
                role.description = role_data['description']
                role.save()
                self.stdout.write(self.style.WARNING(f'更新角色: {role.name}'))
            else:
                self.stdout.write(f'角色已存在: {role.name}')
    
    def _init_admin_user(self, force):
        """初始化管理员用户"""
        self.stdout.write('初始化管理员用户...')
        
        # 获取管理员角色
        try:
            admin_role = Role.objects.get(name='admin')
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR('管理员角色不存在，请先初始化角色'))
            return
        
        # 默认管理员用户信息
        admin_data = {
            'username': 'admin',
            'password': 'admin123',  # 实际应用中应使用更复杂的密码
            'email': 'admin@example.com',
            'nickname': '系统管理员',
            'is_staff': True,
            'is_superuser': True,
        }
        
        # 创建或更新管理员用户
        admin_user, created = User.objects.get_or_create(
            username=admin_data['username'],
            defaults={
                'password': make_password(admin_data['password']),
                'email': admin_data['email'],
                'nickname': admin_data['nickname'],
                'is_staff': admin_data['is_staff'],
                'is_superuser': admin_data['is_superuser'],
                'role': admin_role,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'创建管理员用户: {admin_user.username}'))
        elif force:
            # 更新管理员用户信息（不更新密码）
            admin_user.email = admin_data['email']
            admin_user.nickname = admin_data['nickname']
            admin_user.is_staff = admin_data['is_staff']
            admin_user.is_superuser = admin_data['is_superuser']
            admin_user.role = admin_role
            admin_user.save()
            self.stdout.write(self.style.WARNING(f'更新管理员用户: {admin_user.username}'))
        else:
            self.stdout.write(f'管理员用户已存在: {admin_user.username}')
    
    def _init_sample_datasource(self, force):
        """初始化示例数据源"""
        self.stdout.write('初始化示例数据源...')
        
        # 获取管理员用户
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('管理员用户不存在，请先初始化管理员用户'))
            return
        
        # 示例数据源信息
        sample_datasource = {
            'name': '示例MySQL数据源',
            'type': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'database': 'sample_db',
            'username': 'root',
            'password': 'password',  # 实际应用中应使用更安全的密码管理方式
            'description': '这是一个示例MySQL数据源',
            'creator': admin_user,
        }
        
        # 创建或更新示例数据源
        datasource, created = DataSource.objects.get_or_create(
            name=sample_datasource['name'],
            defaults={
                'type': sample_datasource['type'],
                'host': sample_datasource['host'],
                'port': sample_datasource['port'],
                'database': sample_datasource['database'],
                'username': sample_datasource['username'],
                'password': sample_datasource['password'],
                'description': sample_datasource['description'],
                'creator': sample_datasource['creator'],
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'创建示例数据源: {datasource.name}'))
        elif force:
            # 更新示例数据源信息
            datasource.type = sample_datasource['type']
            datasource.host = sample_datasource['host']
            datasource.port = sample_datasource['port']
            datasource.database = sample_datasource['database']
            datasource.username = sample_datasource['username']
            datasource.password = sample_datasource['password']
            datasource.description = sample_datasource['description']
            datasource.save()
            self.stdout.write(self.style.WARNING(f'更新示例数据源: {datasource.name}'))
        else:
            self.stdout.write(f'示例数据源已存在: {datasource.name}')
