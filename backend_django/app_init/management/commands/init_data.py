import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from system.models import User, Role, Menu, RoleMenu
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
        
        # 初始化菜单
        self._init_menus(force)
        
        # 初始化示例数据源
        self._init_sample_datasource(force)

        # 初始化角色关联菜单
        self._init_role_menu(force)


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
    
    def _init_menus(self, force):
        """初始化菜单数据"""
        self.stdout.write('初始化菜单数据...')
        
        # 获取管理员用户
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('管理员用户不存在，请先初始化管理员用户'))
            return
        
        # 定义菜单数据
        menu_data = [
            {
                'name': '首页',
                'path': '/dashboard',
                'component': 'Dashboard',
                'icon': 'HomeFilled',
                'sort': 1,
                'hidden': False,
                'parent': None
            },
            # 系统管理
            {
                'name': '系统管理',
                'path': 'system',
                'component': 'system/index',
                'icon': 'Setting',
                'sort': 2,
                'hidden': False,
                'parent': None
            },
            # 系统管理子菜单
            {
                'name': '角色管理',
                'path': 'system-role',
                'component': 'system/Roles',
                'icon': 'Setting',
                'sort': 1,
                'hidden': False,
                'parent_name': '系统管理'
            },
            {
                'name': '用户管理',
                'path': 'system-user',
                'component': 'system/Users',
                'icon': 'Setting',
                'sort': 2,
                'hidden': False,
                'parent_name': '系统管理'
            },
            {
                'name': '菜单管理',
                'path': 'system-menu',
                'component': 'system/Menu',
                'icon': 'Menu',
                'sort': 3,
                'hidden': False,
                'parent_name': '系统管理'
            },
            {
                'name': '系统配置',
                'path': 'system-config',
                'component': 'system/Config',
                'icon': 'Setting',
                'sort': 4,
                'hidden': False,
                'parent_name': '系统管理'
            },
            {
                'name': '系统日志',
                'path': 'system-log',
                'component': 'system/Log',
                'icon': 'Setting',
                'sort': 5,
                'hidden': False,
                'parent_name': '系统管理'
            },
            # 数据源管理
            {
                'name': '数据源管理',
                'path': 'datasources',
                'component': 'DataSources',
                'icon': 'Collection',
                'sort': 6,
                'hidden': False,
                'parent': None
            },
            # 数据开发
            {
                'name': '数据开发',
                'path': 'dataquery',
                'component': 'index',
                'icon': 'Edit',
                'sort': 7,
                'hidden': False,
                'parent': None
            },
            # 数据开发子菜单
            {
                'name': '数据查询',
                'path': 'index',
                'component': 'dataquery/index',
                'icon': 'Edit',
                'sort': 1,
                'hidden': False,
                'parent_name': '数据开发'
            },
            {
                'name': '查询日志',
                'path': 'querylog',
                'component': 'dataquery/QueryLog',
                'icon': 'Edit',
                'sort': 2,
                'hidden': False,
                'parent_name': '数据开发'
            },
            # 报表信息
            {
                'name': '报表信息',
                'path': 'reportinfo',
                'component': 'index',
                'icon': 'Edit',
                'sort': 5,
                'hidden': False,
                'parent': None
            },
            # 报表信息子菜单
            {
                'name': '报表设计',
                'path': 'report',
                'component': 'reportinfo/ReportManage',
                'icon': 'Edit',
                'sort': 3,
                'hidden': False,
                'parent_name': '报表信息'
            },
            {
                'name': '接口管理',
                'path': 'interface',
                'component': 'reportinfo/InterfaceManage',
                'icon': 'Edit',
                'sort': 4,
                'hidden': False,
                'parent_name': '报表信息'
            }
        ]
        
        # 创建父菜单字典，用于关联子菜单
        parent_menus = {}
        
        # 首先创建所有父菜单
        for item in menu_data:
            if item.get('parent') is None and not item.get('parent_name'):
                menu, created = Menu.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'path': item['path'],
                        'component': item['component'],
                        'icon': item['icon'],
                        'sort': item['sort'],
                        'hidden': item['hidden'],
                        'creator': admin_user
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'创建菜单: {menu.name}'))
                elif force:
                    menu.path = item['path']
                    menu.component = item['component']
                    menu.icon = item['icon']
                    menu.sort = item['sort']
                    menu.hidden = item['hidden']
                    menu.save()
                    self.stdout.write(self.style.WARNING(f'更新菜单: {menu.name}'))
                else:
                    self.stdout.write(f'菜单已存在: {menu.name}')
                
                # 将父菜单添加到字典中
                parent_menus[menu.name] = menu
        
        # 然后创建所有子菜单
        for item in menu_data:
            if item.get('parent_name'):
                parent = parent_menus.get(item['parent_name'])
                if not parent:
                    self.stdout.write(self.style.ERROR(f'父菜单不存在: {item["parent_name"]}，无法创建子菜单: {item["name"]}'))
                    continue
                
                menu, created = Menu.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'path': item['path'],
                        'component': item['component'],
                        'icon': item['icon'],
                        'sort': item['sort'],
                        'hidden': item['hidden'],
                        'parent': parent,
                        'creator': admin_user
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'创建子菜单: {menu.name}'))
                elif force:
                    menu.path = item['path']
                    menu.component = item['component']
                    menu.icon = item['icon']
                    menu.sort = item['sort']
                    menu.hidden = item['hidden']
                    menu.parent = parent
                    menu.save()
                    self.stdout.write(self.style.WARNING(f'更新子菜单: {menu.name}'))
                else:
                    self.stdout.write(f'子菜单已存在: {menu.name}')

    def _init_role_menu(self, force=False):
        """初始化角色菜单权限"""
        self.stdout.write('初始化角色菜单权限...')
        
        # 获取管理员角色和管理员用户
        try:
            admin_role = Role.objects.get(name='admin')
            admin_user = User.objects.get(username='admin')
        except (Role.DoesNotExist, User.DoesNotExist):
            self.stdout.write(self.style.ERROR('管理员角色或用户不存在，请先初始化角色和用户'))
            return
        
        # 获取所有菜单
        menus = Menu.objects.all()
        
        # 如果是强制更新，先删除已有的角色菜单关联
        if force:
            RoleMenu.objects.filter(role=admin_role).delete()
            self.stdout.write(self.style.WARNING(f'已删除角色 {admin_role.name} 的所有菜单权限'))
        
        # 批量创建角色菜单关联
        role_menus = []
        for menu in menus:
            # 检查是否已存在关联
            if not RoleMenu.objects.filter(role=admin_role, menu=menu).exists():
                role_menu = RoleMenu(
                    role=admin_role,
                    menu=menu,
                    creator=admin_user,
                    updator=admin_user
                )
                role_menus.append(role_menu)
                self.stdout.write(self.style.SUCCESS(f'为角色 {admin_role.name} 添加菜单权限: {menu.name}'))
        
        # 批量创建角色菜单关联记录
        if role_menus:
            RoleMenu.objects.bulk_create(role_menus)
            self.stdout.write(self.style.SUCCESS(f'成功创建 {len(role_menus)} 条角色菜单关联记录'))
        else:
            self.stdout.write('所有菜单权限已存在，无需创建')