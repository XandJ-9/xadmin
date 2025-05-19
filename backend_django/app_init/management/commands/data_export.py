import logging,json
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from system.models import User, Role, Menu, RoleMenu
from datasource.models import DataSource

logger = logging.getLogger('django')

export_data_file = 'export_data.json'


class Command(BaseCommand):
    help = '数据迁移-导出系统配置数据'

    def __init__(self):
        self.data = {}
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新创建数据，即使数据已存在',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # force = options.get('force', False)
        self.stdout.write(self.style.NOTICE('开始导出系统配置数据...'))
        
        self._export_user()
        self._export_role()
        self._export_menu()

        with open(export_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        self.stdout.write(self.style.SUCCESS('系统数据初始化完成！'))

    def _export_user(self):
        # 导出用户数据
        self.stdout.write(self.style.NOTICE('开始导出用户数据...'))
        try:
            users = User.objects.all()
            for user in users:
                user_data = {
                    'username': user.username,
                    'password': user.password,
                    'nickname': user.nickname,
                    'avatar': user.avatar,
                    'is_active': user.is_active,
                    'role_id': user.role.id if user.role else None,
                }
                self.stdout.write(self.style.SUCCESS(f'导出用户数据: {user_data}'))
        except Exception as e:
            logger.error(f'导出用户数据失败: {e}')
            self.stdout.write(self.style.ERROR('导出用户数据失败'))

    def _export_role(self):
        # 导出角色数据
        self.stdout.write(self.style.NOTICE('开始导出角色数据...'))
        try:
            roles = Role.objects.all()
            for role in roles:
                role_data = {
                    'name': role.name,
                    'description': role.description,
                }
                self.stdout.write(self.style.SUCCESS(f'导出角色数据: {role_data}'))
        except Exception as e:
            logger.error(f'导出角色数据失败: {e}')
            self.stdout.write(self.style.ERROR('导出角色数据失败'))
    
    def _export_menu(self):
        # 导出菜单数据
        self.stdout.write(self.style.NOTICE('开始导出菜单数据...'))
        try:
            menus = Menu.objects.all()
            for menu in menus:
                menu_data = {
                    'name': menu.name,
                    'menu_type': menu.menu_type,
                    'path': menu.path,
                    'component': menu.component,
                    'component_name': menu.component_name,
                    'redirect': menu.redirect,
                    'meta_icon': menu.meta_icon,
                    'meta_title': menu.meta_title,
                    'name_code': menu.name_code,
                    'icon': menu.icon,
                    'sort': menu.sort,
                    'hidden': menu.hidden,
                    'meta_need_tagview': menu.meta_need_tagview,
                    'parent_id': menu.parent.id if menu.parent else None
                }
                self.stdout.write(self.style.SUCCESS(f'导出菜单数据: {menu_data}'))
                self.data.setdefault('menus', []).append(menu_data)
        except Exception as e:
            logger.error(f'导出菜单数据失败: {e}')
            self.stdout.write(self.style.ERROR('导出菜单数据失败'))